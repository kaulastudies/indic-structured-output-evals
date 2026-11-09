# Sarvam contribution record — checked 9 November 2026

| Contribution | Status | Local evidence already collected |
|---|---|---|
| [AI SDK PR #4](https://github.com/sarvam-ai/ai-sdk/pull/4): preserve final-chunk top-level token usage | OPEN, unmerged, no review comments at check | 12 tests pass, typecheck/build pass; 3 new cases failed before fix |
| [MCP PR #115](https://github.com/sarvamai/sarvam-mcp/pull/115): reject nonfinite/negative retry delays | OPEN, unmerged, no review comments at check | 116 tests pass; 4 new cases failed before fix; local handshake registered 38 tools |

Neither PR is a demonstrated fix for the playground formatting observations. No merge, maintainer approval or endorsement is claimed. SDK response-shape credit remains with @MeKaustubh07, who reported [issue #20](https://github.com/sarvamai/sarvam-ai-sdk/issues/20).

A current issue/PR scan found existing proposed fixes for cookbook validation coverage (#138/#144), BOM parsing (#183), model allowlist wiring (#184), MCP credential file permissions (#87/#100), base64 validation (#81/#101), batch STT builder docs (#82/#85), and TTS model parameters (#54). These were not duplicated. Prefer reproductions, focused review or new uncovered behavior over another overlapping PR.

Source repositories: [cookbook](https://github.com/sarvamai/sarvam-ai-cookbook), [active AI SDK](https://github.com/sarvam-ai/ai-sdk), [MCP](https://github.com/sarvamai/sarvam-mcp). Local evidence is distinct from hosted CI. This public kit supplies additional independently reusable evaluation work while upstream reviews remain pending.
