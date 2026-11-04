# Distilla MCP plugin — website change reader (docs)

**Status:** README updated (ship after staging `agent2-mcp-shim` exposes `website_change`)  
**Owner:** Lucio Pagni  
**Branch:** `luciopagni/eng-770-mcp-website-change`  
**Linear:** ENG-770  
**Implementation SoT:** Distilla-AI/`pipeline-data`
`docs/company-website-tracking-mcp-website-change-spec.md`

---

## Goal

This repository is the **Claude / Codex plugin wrapper**. It does **not** host
the MCP server. When pipeline-data exposes gateway `website_change` through
`query_entity`, update **user-facing docs** here so installers know Distilla
can answer website-change questions.

---

## What changes here (after the server ships)

1. **README — “What you can do”**  
   Add a short bullet, e.g. company website changes (kept summaries when Distilla
   detects meaningful page updates).

2. **README — Tools table**  
   Do **not** invent a new tool name. Existing tools already cover it:

   - `list_queryable_entities` / `describe_queryable_entities` / `query_entity` /
     `aggregate_entity` gain a new entity named `website_change`.

   Optionally note under `query_entity` that queryable entities include website
   changes once listed by `list_queryable_entities`.

3. **Manifest copy** (`manifest/core.json` / generated plugin JSON)  
   Only if product wants marketing text to mention website changes. Prefer
   regenerating via `scripts/generate_manifests.py` after editing the SoT
   fields. Bump plugin version when shipping a user-visible description change.

---

## What does **not** change here

- No server code, OAuth, or tool handlers (not in this repo)
- No gateway or CWT infra
- No secrets

---

## Acceptance

- [ ] Pipeline-data MCP allowlist live and `website_change` queryable
- [ ] README bullet + tool wording match the hosted catalog
- [ ] Manifest regenerated / version bumped if description fields change

---

## Sequence

1. Land pipeline-data reader (`db_registry` + `MCP_ENTITY_ALLOWLIST`) and deploy
   `agent2_mcp_shim`.
2. Verify with a real MCP client: list → describe → query `website_change`.
3. Apply this repo’s doc / manifest updates on this branch and publish the plugin
   version.
