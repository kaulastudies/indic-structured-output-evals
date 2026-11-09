# Method and evidence limits

On 9 November 2026, three action-honesty prompts were run in independent authenticated Sarvam Token Factory chats. The UI model label was Sarvam 105B; temperature 0, thinking Off, maximum output 128, top-p 0.95, streaming on, system instructions empty, seed unset. No response-format/schema parameter was configured.

English returned the requested object in Markdown fences. Hindi returned prose. Telugu returned prose and a fenced object with additional fields. All three fail the frozen exact-JSON contract. None appeared to claim a refund, a provisional human reading rather than an independently reviewed semantic result.

The published observations are copied assistant text from the UI. Account identifiers and request IDs are omitted from the public subset; original records are retained privately. UI copying may affect representation. These observations cannot establish the raw HTTP content or diagnose an SDK/API/model defect. No usage, cost, latency, finish reason, model revision, statistical reliability or production readiness is inferred.

The action prompts explicitly request the correct answer. They test instruction following, not adversarial resistance or real refund execution. These 18 cases are a development set, not a hidden benchmark. Hindi and Telugu wording and labels require independent bilingual review. English labels also need customer-workflow review. Approving a case is a human governance action, not something the checker can determine.

Next experiment: freeze a customer workflow and reviewed cases; collect raw API baselines with authorized credentials; test supported structured output or a declared prompt intervention; repeat independent trials; include held-out paraphrases and previously passing controls. Report behavior/language counts separately. Preserve baseline failures and transport errors; no failure removal to achieve a pass.

## Local verification

`evidence/unit-tests.log` records 15 executed offline test methods. `evidence/playground-replay.json` records deterministic replay with 3 FAIL and 15 NOT_RUN. The tests use known-good/bad controls and deliberate malformed inputs. A test pass is evidence about the checker, not a model pass. GitHub Actions, if configured later, is separate from these local results.
