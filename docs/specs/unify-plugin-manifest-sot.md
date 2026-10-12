# Spec: Unify plugin manifest source of truth

**Repo:** `distilla-mcp`  
**Branch:** `lucio/unify-plugin-manifest-sot`  
**Status:** Implemented  

## Workflow

1. Edit [`manifest/core.json`](../../manifest/core.json) (shared identity, copy, URLs, version).
2. Run `python3 scripts/generate_manifests.py`.
3. Commit the SoT and regenerated platform JSON together.
4. CI runs `python3 scripts/generate_manifests.py --check` so drift fails the build.

Platform-only fields (Codex `extensions`, ChatGPT `tools` / test cases, Claude `$schema`) live in the generated files and are preserved on regenerate.

Plugin and app metadata is duplicated across:

| File | Role |
| --- | --- |
| `.mcp.json` | MCP client connect stub (`https://api.distilla.ai/mcp`) |
| `.claude-plugin/plugin.json` | Anthropic / Claude Code plugin |
| `.codex-plugin/plugin.json` | OpenAI Codex plugin (+ `com.openai` review block) |
| `chatgpt-app-submission.json` | ChatGPT Apps SDK submission |
| `server.json` | Official MCP Registry card (`ai.distilla/mcp`) — fully generated |

Shared fields (version, display name, short/long description, author, keywords, URLs) are hand-copied. They already drift (e.g. Claude `1.0.2` vs Codex `1.0.0`; ChatGPT display name `Distilla` vs Claude/Codex `Distilla Investment Research`).

Platform loaders need plain JSON at fixed paths. They will not resolve a shared `$ref` at install time.

## Goal

One editable source of truth for **shared** identity and copy. Platform JSON files are generated (or regenerated) projections, still committed so Claude / Codex / ChatGPT install flows keep working.

## Non-goals

- Changing the hosted MCP server or OAuth behavior
- Merging Claude, Codex, and ChatGPT into a single marketplace schema
- Generating tool annotations / OpenAI review test cases from the SoT in v1 (those stay platform-only overlays)
- Rewriting README marketing independently of this SoT (optional later: README pulls from SoT)

## Decision

**Generate from SoT + CI drift check.**

```text
manifest/core.json          ← edit shared fields here
scripts/generate_manifests.py
        │
        ▼
.mcp.json
.claude-plugin/plugin.json
.codex-plugin/plugin.json
chatgpt-app-submission.json
server.json                 ← Official MCP Registry (full file from SoT)
```

CI runs `python3 scripts/generate_manifests.py --check` (fails when outputs would change).

v1 does not use separate overlay files for Claude / Codex / ChatGPT; platform-only blobs stay in those committed targets and survive merge-style regenerate. **`server.json` has no overlay** — the entire file is projected from SoT.

## SoT schema (`manifest/core.json`)

Required fields:

| Field | Purpose |
| --- | --- |
| `id` | Plugin id (`distilla`) |
| `displayName` | Full product name for Claude / Codex |
| `chatgptDisplayName` | ChatGPT listing name (may be shorter) |
| `version` | Semver; single bump for all consumers |
| `subtitle` | Short tagline (Codex shortDescription / ChatGPT subtitle) |
| `descriptionShort` | One-paragraph plugin description (Claude / Codex `description`) |
| `descriptionShortClaudeSuffix` | Optional; if set, Claude description uses a Claude-specific first sentence variant — prefer **one** short description with no platform fork unless product insists |
| `descriptionLong` | Long blurb (Codex `interface.longDescription` / ChatGPT `app_info.description`) |
| `author.name` / `author.email` / `author.url` | Publisher |
| `urls.homepage` | `https://www.distilla.ai` |
| `urls.agents` | `https://agents.distilla.ai` |
| `urls.mcp` | `https://api.distilla.ai/mcp` |
| `urls.repository` | GitHub repo URL |
| `urls.support` | Support / contact |
| `urls.privacy` | Privacy policy |
| `urls.terms` | Terms |
| `license` | e.g. `MIT` |
| `keywords` | Array of strings |
| `category` | Codex / ChatGPT category mapping (`Finance` / `FINANCE`) |

Optional:

| Field | Purpose |
| --- | --- |
| `defaultEnabled` | Claude `defaultEnabled` |
| `defaultPrompts` | Codex / ChatGPT default prompts (if shared) |
| `registry.name` | Official Registry namespace (`ai.distilla/mcp`) |
| `registry.description` | Registry short description (≤100 chars) |
| `registry.iconUrl` | Public HTTPS icon for the registry card |
| `registry.iconSizes` | Icon sizes string (e.g. `64x64`) |

### Field mapping (generator)

| SoT | `.mcp.json` | Claude | Codex | ChatGPT | `server.json` |
| --- | --- | --- | --- | --- | --- |
| `id` | `mcpServers` key | `name` | `name` | — | — |
| `displayName` | — | `displayName` | `interface.displayName` | — | — |
| `chatgptDisplayName` | — | — | — | `app_info.display_name` | `title` |
| `version` | — | `version` | `version` | if schema allows; else omit | `version` |
| `subtitle` | — | — | `interface.shortDescription` | `app_info.subtitle` | — |
| `descriptionShort` | — | `description` | `description` | — | — |
| `descriptionLong` | — | — | `interface.longDescription` | `app_info.description` | — |
| `urls.mcp` | `mcpServers.distilla.url` | — | — | — | `remotes[0].url` |
| `urls.homepage` | — | `homepage` | `homepage` | — | — |
| `urls.agents` | — | — | `interface.websiteURL` | — | `websiteUrl` |
| `urls.repository` | — | `repository` | `repository` | — | — |
| `urls.support` | — | — | `interface.supportURL` | if schema allows | — |
| `urls.privacy` | — | — | `interface.privacyPolicyURL` | if schema allows | — |
| `urls.terms` | — | — | `interface.termsOfServiceURL` | if schema allows | — |
| `author.*` | — | `author` | `author` | — | — |
| `keywords` | — | `keywords` | `keywords` | — | — |
| `license` | — | `license` | `license` | — | — |
| `registry.name` | — | — | — | — | `name` |
| `registry.description` | — | — | — | — | `description` |
| `registry.iconUrl` / `iconSizes` | — | — | — | — | `icons[0]` |

Platform-only content (not in SoT v1):

- Claude: `$schema`
- Codex: `extensions.com.openai` (test cases, commerce, release notes)
- ChatGPT: `tools` annotations/justifications, `test_cases`, `negative_test_cases`, `$schema`

**Overlay strategy (v1):** Generator reads current platform file (or `manifest/overlays/*.json`), replaces only mapped shared paths, leaves the rest intact. Safer than regenerating OpenAI review blocks from scratch.

On each generate, Claude `icon` and Codex `interface.composerIcon` / `interface.logo` are removed. A setting that points at a local image or font keeps the plugin held for review, because those files are not checked as code. The public logo stays on `registry.iconUrl` (`server.json` `icons[0].src`).

## Workflow

1. Edit `manifest/core.json` (version bump, copy, URLs).
2. Run `python3 scripts/generate_manifests.py` (or `make generate-manifests` if added).
3. Commit SoT + regenerated JSON together.
4. CI: validate JSON parse (existing) + `generate_manifests.py --check` (diff empty) + existing `claude plugin validate`.

## Acceptance criteria

1. Changing `version` in SoT and regenerating updates Claude and Codex versions to the same value.
2. `descriptionLong` in SoT matches Codex longDescription and ChatGPT description after generate.
3. `subtitle` matches Codex shortDescription and ChatGPT subtitle.
4. `.mcp.json` URL always equals `urls.mcp`.
5. Keywords and author match across Claude and Codex.
6. OpenAI review / ChatGPT tool annotation blocks survive regeneration unchanged unless overlays change.
7. CI fails if someone hand-edits a generated shared field without updating SoT + regenerating.
8. `claude plugin validate` still passes.
9. `server.json` `remotes[0].url` equals `urls.mcp`, `websiteUrl` equals `urls.agents` (with trailing `/`), `version` matches SoT, and `registry.description` is ≤100 chars.
10. Publishing to the Official Registry uses `mcp-publisher publish ./server.json` from this repo (not `mcp-api-web`).

## Out of scope (later)

- Auto-sync README “What you can do” from SoT
- Hosting `/.well-known/mcp.json` from this repo (that stays on agents.distilla.ai / `mcp-api-web`)
- Generating ChatGPT tool list from live MCP `tools/list`

## Resolved decisions

1. **Unified** `descriptionShort` to the Codex wording (“for AI agents”).
2. **Kept** ChatGPT short display name (`Distilla`); Claude/Codex use full `displayName`.
3. **Python 3** stdlib generator; CI uses `scripts/generate_manifests.py --check`.
