# Spec: Declared-tool tests for MCP registry scoring

**Repo:** `distilla-mcp`  
**Branch:** `lucio/m8ven-declared-tool-tests`  
**Status:** Implemented  
**Related:** [M8ven listing](https://m8ven.ai/mcp/distilla-ai-distilla-mcp-id7p9g?s=readme) (C 74/100 @ `d91a15d`)

## Why this exists

MCP directories and trust scorers (M8ven today; Smithery, the Official MCP Registry, and OpenAI review surfaces similarly) treat the **GitHub repo behind the listing** as the audit surface. They do not open Distilla’s private `pipeline-data` shim.

Their trust pyramid is roughly:

1. **Code** — open source, license, no exfil patterns
2. **Verification depth** — tests, tool hints, live scan, sandbox
3. **Reputation** — stars, age, adoption (new projects often **capped at C**)

M8ven’s current quality suggestion on this repo is:

> Tests exist — No test files found — Add tests that exercise each declared tool.

The follow-on form of that check is usually **“X/Y tools referenced in tests”**: each declared tool **name** must appear in real test files (`tests/`, `test_*.py`, and similar). ChatGPT `test_cases` JSON and Codex review prompts **do not** count.

So for Distilla, listing-repo tests:

- Clear an explicit M8ven quality deduction on the public card
- Show every declared tool is intentional and checked under CI
- Align the listing repo with how registries judge “serious” MCP servers
- Are **complementary** to handler tests in `pipeline-data` (correctness) vs listing-repo tests (discoverability / trust score)

They will **not** by themselves lift the grade above the adoption cap (still C until reputation moves). They deepen the score **within** that band and remove a visible “no tests” finding.

## Goal

Add a small, CI-run test suite in `distilla-mcp` that:

1. Is discoverable as real test files (not JSON review cases)
2. **References each declared tool by name** so coverage can report **10/10**
3. Asserts useful contract facts about the listing artifacts this repo owns

## Non-goals

- Re-implementing or calling the hosted MCP server in this repo
- Moving `agent2_mcp_shim` tests into `distilla-mcp`
- Raising M8ven above C via adoption (out of scope)
- Generating ChatGPT `test_cases` from the SoT (separate; optional hygiene)
- Adding `idempotentHint` (separate OpenAI / M8ven hints finding; optional follow-up)

## Declared tools (source for this check)

Source of names for v1: keys of [`chatgpt-app-submission.json`](../../chatgpt-app-submission.json) → `tools` (must stay in sync with the README Tools table):

| Tool | In ChatGPT positive `test_cases` today? |
| --- | --- |
| `ping` | No |
| `list_queryable_entities` | Yes |
| `describe_queryable_entities` | Yes |
| `query_entity` | Yes |
| `aggregate_entity` | Yes |
| `screen_drivers` | Yes |
| `screen_earnings` | No |
| `get_screen_job` | Yes |
| `search_public_library` | Yes |
| `get_library_document` | Yes |

## Decision

**Contract tests in-repo + CI step.**

```text
chatgpt-app-submission.json  (declared tools + annotations)
README.md                    (human tool table)
tests/test_declared_tools.py ← NEW: name every tool; assert contracts
.github/workflows/validate.yml ← NEW step: run unittest
```

Use stdlib `unittest` only. Keep this listing repo zero third-party test deps.

## Requirements

1. [`tests/test_declared_tools.py`](../../tests/test_declared_tools.py) (or equivalent) must contain each of the 10 tool names as string literals used in assertions (a loop over a tuple is fine if every name appears in the file).
2. Assert `set(chatgpt tools) == DECLARED_TOOLS`.
3. For each tool: annotations and justifications are present (as today).
4. For each tool: README documents the name (for example `` `tool` `` in the Tools table).
5. Recommended: fail if a non-`ping` tool is missing from positive ChatGPT `tools_triggered` (surfaces the `screen_earnings` gap).
6. CI: after SoT `--check`, run `python3 -m unittest discover -s tests -v`.
7. Do not call `https://api.distilla.ai/mcp` in default CI (no secrets, no flaky live dependency).

## Out of band (same PR or follow-up)

| Item | Why |
| --- | --- |
| ChatGPT case for `screen_earnings` (and optional `ping`) | OpenAI review coverage, not M8ven’s file scan |
| `idempotentHint` on all tools | Four-hint completeness for directories |
| Short README note that listing-repo tests are contract / registry checks | Avoid implying local server execution |

## Explicit non-claim

These tests **do not** prove live tool behavior. Handler correctness remains owned by `pipeline-data/tests/shims/agent2_mcp_shim/`. This suite proves the **listing contract** that scanners score.

## Acceptance

- [ ] Branch from current `main`; PR into `Distilla-AI/distilla-mcp`
- [x] `python3 -m unittest discover -s tests -v` passes locally
- [x] `validate.yml` runs the suite on PR / push to `main`
- [ ] After merge and M8ven re-verify: quality suggestion is no longer “No test files found”; tool reference coverage is **10/10** (or equivalent)
- [ ] Grade may stay C; the “no tests” finding should be gone
