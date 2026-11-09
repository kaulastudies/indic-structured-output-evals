"""Offline, fail-closed replay of multilingual structured-response evidence."""
import argparse
import hashlib
import json
import sys
from pathlib import Path


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def _nonfinite(value):
    raise ValueError('nonfinite JSON constant')


def parse(text):
    value = json.loads(text, object_pairs_hook=_unique, parse_constant=_nonfinite)
    json.dumps(value, allow_nan=False)  # Reject exponent overflow such as 1e999.
    return value


def digest(value):
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)
    return hashlib.sha256(data.encode()).hexdigest()


def grade(text, expected):
    try:
        value = parse(text)
    except (ValueError, TypeError):
        return {'status': 'FAIL', 'reason': 'invalid_json'}
    # Canonical representation distinguishes false/0, numeric/string and extra fields.
    return {'status': 'PASS', 'reason': 'exact_match'} if digest(value) == digest(expected) else {'status': 'FAIL', 'reason': 'value_or_shape_mismatch'}


def replay(cases, evidence):
    if not isinstance(cases, list) or not cases:
        raise ValueError('nonempty case inventory required')
    index = {}
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError('case must be an object')
        for field in ('case_id', 'version', 'language', 'behavior', 'prompt', 'review_status'):
            if not isinstance(case.get(field), str) or not case[field].strip():
                raise ValueError('invalid case field: ' + field)
        if not isinstance(case.get('expected_json'), dict):
            raise ValueError('expected_json must be an object')
        if case['case_id'] in index:
            raise ValueError('duplicate case ID')
        digest(case)  # Also rejects nonfinite expected data.
        index[case['case_id']] = case
    if not isinstance(evidence, dict) or evidence.get('source') not in ('synthetic_fixture', 'web_playground_copy', 'api_response'):
        raise ValueError('explicit supported evidence source required')
    if not isinstance(evidence.get('model'), str) or not evidence['model'].strip():
        raise ValueError('model label required')
    observations = evidence.get('observations')
    if not isinstance(observations, list):
        raise ValueError('observations must be a list')
    seen = set()
    rows = []
    for item in observations:
        if not isinstance(item, dict):
            raise ValueError('observation must be an object')
        cid = item['case_id']
        if cid not in index or cid in seen:
            raise ValueError('unknown or duplicate observation case ID')
        seen.add(cid)
        case = index[cid]
        if item.get('case_digest') != digest(case):
            raise ValueError('case digest mismatch')
        if not isinstance(item.get('response'), str):
            raise ValueError('response must be text')
        rows.append({'case_id': cid, 'language': case['language'], 'behavior': case['behavior'],
                     'case_digest': digest(case), 'response_digest': hashlib.sha256(item['response'].encode()).hexdigest(),
                     'review_status': case['review_status'], **grade(item['response'], case['expected_json'])})
    rows.extend({'case_id': cid, 'language': c['language'], 'behavior': c['behavior'],
                 'case_digest': digest(c), 'review_status': c['review_status'],
                 'status': 'NOT_RUN', 'reason': 'missing_observation'} for cid, c in index.items() if cid not in seen)
    counts = {state: sum(r['status'] == state for r in rows) for state in ('PASS', 'FAIL', 'NOT_RUN')}
    return {'schema_version': '1.0', 'source': evidence['source'], 'model': evidence['model'],
            'inventory_digest': digest(cases), 'evidence_digest': digest(evidence), 'counts': counts,
            'release_decision': 'HOLD' if counts['FAIL'] or counts['NOT_RUN'] or any(c['review_status'] != 'APPROVED' for c in cases) else 'PASS',
            'scope': 'Exact JSON replay only; no semantic, safety or production reliability verdict', 'results': rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', type=Path, default=Path('data/cases.json'))
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        report = replay(parse(args.cases.read_text(encoding='utf-8')), parse(args.evidence.read_text(encoding='utf-8')))
    except (ValueError, TypeError, KeyError, OSError) as exc:
        # Do not echo inputs: callers may accidentally provide private data.
        print('Invalid input: ' + type(exc).__name__, file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'counts': report['counts'], 'release_decision': report['release_decision']}))
    return 0 if report['release_decision'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
