# Distilla MCP plugin — Public Library newsletter reader (docs)

**Status:** README + manifest copy updated (v1.0.4; ship after pipeline-data
exposes `Newsletter` in `PUBLIC_LIBRARY_DOC_TYPES`)  
**Owner:** Lucio Pagni  
**Branch:** `luciopagni/eng-770-mcp-website-change-manifest-copy`  
**Implementation SoT:** Distilla-AI/`pipeline-data`
`docs/mcp-public-library-newsletter-spec.md`

---

## Goal

This repository is the **Claude / Codex plugin wrapper**. It does **not** host
the MCP server. When pipeline-data adds `Newsletter` to
`PUBLIC_LIBRARY_DOC_TYPES`, update **user-facing docs** here so installers know
Distilla can search industry newsletters in the Public Library.

---

## What changes here

1. **README — “What you can do”**  
   Expand the Research library bullet to mention newsletters (and YouTube),
   naming `search_public_library`.

2. **README — Example prompts**  
   Add one newsletter search example.

3. **Manifest copy** (`manifest/core.json` / generated plugin JSON)  
   Mention newsletters in short/long / registry descriptions. Regenerate via
   `scripts/generate_manifests.py`. Version already bumped to **1.0.4** on this
   branch for website-change marketing; keep the same version for this doc
   follow-up while the PR is open.

---

## What does **not** change here

- No server code (lives in pipeline-data `agent2_mcp_shim`)
- No new MCP tool name
- No secrets

---

## Acceptance

- [ ] Pipeline-data `PUBLIC_LIBRARY_DOC_TYPES` includes `Newsletter` and shim is
      deployed
- [x] README Research library bullet mentions newsletters
- [x] Manifest regenerated with newsletter wording

---

## Sequence

1. Land pipeline-data `luciopagni/mcp-public-library-newsletter` and deploy
   `agent2_mcp_shim`.
2. Verify MCP: `search_public_library` with `doc_types=["Newsletter"]`.
3. Merge this branch’s plugin docs / manifest updates.
