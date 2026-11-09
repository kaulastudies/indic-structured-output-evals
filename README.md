# Indic Structured Output Evals

An offline regression gate for applications that require machine-readable responses in English, Hindi and Telugu. Built by **Rama Chandra M — AI Evaluation Lab**. Independent project; no Sarvam affiliation or endorsement.

A correct-sounding answer can still break a parser. This kit freezes the requested output, binds observations to case hashes, and reports failures without silently stripping prose or Markdown.

## Try it — Python 3.10+, no dependencies or API key

```bash
python -m unittest discover -s tests -v
python evalkit.py --evidence data/playground-observations.json --output evidence/playground-replay.json
```

The replay command deliberately exits **1**: the included three observed playground responses fail exact JSON, 15 cases have no observations, and language review is pending. Exit 0 means all cases passed and were marked approved; exit 2 means invalid inputs. This is an evaluation workflow recommendation, not enforcement of a deployed release boundary.

| Evidence | Current result | What it establishes |
|---|---|---|
| Original synthetic inventory | 18 cases, 3 languages, 6 behaviors | Starter coverage; independent language review pending |
| Actual Sarvam 105B playground observations | 3 copied responses, 0 exact matches | Prompt-only UI format findings; not raw API behavior |
| Offline checker tests | 15 tests pass | Good/bad controls, stale evidence rejection, missing coverage, type distinctions |
| Automated API execution | Not run here | No key accessed and no live API result claimed |

## What is checked

- Exact JSON values and fields, with JSON key order ignored.
- Markdown/prose, duplicate keys, nonfinite numbers, wrong boolean types and extra fields fail.
- Amounts, order identifiers, date strings, unsupported action claims, missing context and instruction boundaries are represented in the cases. These exact-output checks do not establish semantic safety.
- Case digests prevent accidental replay against edited prompts or labels. Evidence source and model are retained. Hashes detect changes; they do not authenticate who collected the evidence.
- Unobserved cases stay `NOT_RUN`; unreviewed cases keep the release recommendation at `HOLD`.

## Add evidence

Use the structure in `data/playground-observations.json`. Each observation needs `case_id`, `case_digest` (from `evalkit.digest(case)`) and response text. Set source to `synthetic_fixture`, `web_playground_copy`, or `api_response` truthfully and retain the original full record privately. The source label is supplied by the collector, not cryptographically verified. Do not put real customer data, keys, headers or private logs in this public repository.

For API collection, configure credentials outside this repository and obtain explicit permission before accessing saved credentials. This kit performs **no network calls**, retries or automatic spending. Never replace a baseline response with a repaired response; store new observations as a separate experiment.

Read [method and limitations](docs/METHOD.md), [pilot scope](docs/PILOT.md), and [contribution status](docs/CONTRIBUTIONS.md).

## License and credit

Apache-2.0. The 18 synthetic cases originated in AI Evaluation Lab's private evaluation-operations work and are released here by the project owner. The checker is an independent implementation. Sarvam product names identify the integration under evaluation. No upstream Sarvam implementation is vendored.
