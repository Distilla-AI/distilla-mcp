# Distilla MCP plugin — Public Library WebsiteScrape reader (docs)

**Status:** Spec (docs not updated yet)  
**Owner:** Lucio Pagni  
**Branch:** `luciopagni/mcp-public-library-websitescrape-docs`  
**Implementation SoT:** Distilla-AI/`pipeline-data`
`docs/mcp-public-library-websitescrape-spec.md`  
(branch `luciopagni/mcp-public-library-websitescrape`)  
**Pattern:** [`mcp-public-library-newsletter-reader.md`](./mcp-public-library-newsletter-reader.md)

---

## Goal

This repository is the **Claude / Codex plugin wrapper**. It does **not** host
the MCP server. When pipeline-data adds `WebsiteScrape` to
`PUBLIC_LIBRARY_DOC_TYPES`, update **user-facing docs** here so installers know
Distilla’s Public Library search includes:

- research documents  
- investing podcasts  
- **YouTube** transcripts  
- **industry newsletters**  
- **industry / association website scrapes** (`WebsiteScrape`)

Today README + manifest already call out YouTube and newsletters. They do
**not** clearly offer WebsiteScrape.

---

## Naming caution

Do **not** reuse “company website changes” wording for this feature. Website
**changes** (kept summaries of company site diffs) are a different capability.
**WebsiteScrape** = Public Library Type for industry-release HTML/RSS pages
(SIA, press centers, etc.).

Preferred phrasing examples:

- “association and industry website releases”  
- “Public Library WebsiteScrape documents”  
- “industry web scrapes (press / association releases)”

Avoid implying every company homepage is scraped into the library.

---

## What changes here

1. **README — “What you can do”**  
   Expand the Research library bullet so it lists research, podcasts,
   YouTube, newsletters, **and** industry / association website scrapes,
   naming `search_public_library`.

2. **README — Example prompts**  
   Add one WebsiteScrape-oriented example (e.g. semiconductor association
   sales press / SIA-style query with `WebsiteScrape` in mind). Keep existing
   newsletter and research examples.

3. **Manifest copy** (`manifest/core.json` and generated plugin JSON)  
   Mention industry website scrapes / association releases in
   `descriptionShort`, `descriptionLong`, and any registry blurb that today
   ends at “newsletters”. Regenerate via `scripts/generate_manifests.py` (or
   the repo’s documented generate path).

4. **Optional:** `.codex-plugin/plugin.json` / `chatgpt-app-submission.json`
   if those storefront strings are still hand-synced with the manifest.

5. **Version:** Bump plugin version per distilla-mcp release practice when
   shipping the copy change (do not invent a version here — follow current
   SoT on `main`).

---

## What does **not** change here

- No server code (lives in pipeline-data `agent2_mcp_shim`)
- No new MCP tool name
- No secrets
- No claim that WebsiteScrape works until pipeline-data allowlist is deployed

---

## Acceptance

- [ ] Pipeline-data `PUBLIC_LIBRARY_DOC_TYPES` includes `WebsiteScrape` and
      shim is deployed
- [ ] README Research library bullet mentions YouTube, newsletters, **and**
      industry / association website scrapes
- [ ] At least one README example prompt for WebsiteScrape-style search
- [ ] Manifest regenerated; short/long descriptions include the new wording
- [ ] Copy does not conflate WebsiteScrape with “company website changes”

---

## Sequence

1. Land pipeline-data `luciopagni/mcp-public-library-websitescrape` and deploy
   `agent2_mcp_shim`.
2. Verify MCP: `search_public_library` with `doc_types=["WebsiteScrape"]`.
3. Merge this branch’s plugin docs / manifest updates.
4. Optional smoke: `doc_types=["YouTube"]`, `["Newsletter"]`,
   `["WebsiteScrape"]` each accepted.
