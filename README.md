# Distilla

Distilla is a Claude plugin for fundamental equity research. It connects Claude to the hosted Distilla MCP server at `https://api.distilla.ai/mcp`.

The hosted backend is proprietary. It is not in this repository. This repository contains the plugin manifest, the MCP connection file, and these documents. It does not contain secrets or private application code.

The MIT license applies to the files in this repository. It does not apply to the hosted Distilla service.

## Requirements

- Claude Code, or Claude Cowork
- A Distilla account that can use the hosted server

## Install for a local test

Clone this repository and load the plugin directory:

```bash
git clone https://github.com/Distilla-AI/distilla-mcp.git
cd distilla-mcp
claude --plugin-dir .
```

`--plugin-dir` loads the plugin for that session. It does not publish the plugin.

## Install from the plugin directory

> **Not available yet.** Anthropic has not listed Distilla in the community marketplace. The commands in this section do not work until Anthropic lists the plugin. Until then, use [Install for a local test](#install-for-a-local-test).

After Anthropic lists this plugin, add the community marketplace and install Distilla:

```text
/plugin marketplace add anthropics/claude-plugins-community
/plugin install distilla@claude-community
```

## Enable and sign in

The plugin stays off until you enable it. For a local `--plugin-dir` session, enable `distilla` in `/plugin` if Claude shows it as off.

After Anthropic lists the plugin, you can also run:

```bash
claude plugin enable distilla@claude-community
```

The server uses OAuth 2.0 with PKCE. When Claude connects, the server asks you to sign in. In Claude Code, run `/mcp`, select `distilla`, and complete the Distilla sign-in in your browser. This repository does not store credentials. Do not add tokens or keys to these files.

## Example prompts

Ask Claude in plain language after the server is connected. The tools you can call depend on your Distilla account.

1. Summarize NVIDIA's recorded price moves over the past three months, explain the stated reasons, and identify recurring patterns.
2. Among NVIDIA, Apple, and Microsoft, which cited AI-driven cost savings as a guidance or margin lever in their last four earnings periods?
3. Count non-delisted US-headquartered companies by sector, and show the 15 largest sector groups.
4. Find public-library research from the past year on NVIDIA AI data-center demand. Summarize common and conflicting views, and list the source documents.

## Permissions

The plugin opens one remote MCP connection. It does not run local software, hooks, or commands.

| Server | Transport | URL | Authentication |
| --- | --- | --- | --- |
| `distilla` | HTTPS (Streamable HTTP) | `https://api.distilla.ai/mcp` | OAuth 2.0 with PKCE (S256) through Clerk at `https://clerk.distilla.ai`. Scopes: `profile`, `email`, `offline_access`. |

The server also accepts a Distilla API key (`ak_...`) as a Bearer token. The plugin does not use or store an API key.

### Tools

No tool changes your Distilla account, your watchlists, or Distilla research data. Each call except `ping` also adds one usage record. See [Privacy and data handling](#privacy-and-data-handling).

| Tool | Access | What the call sends to Distilla |
| --- | --- | --- |
| `ping` | Read only | A test message |
| `list_queryable_entities` | Read only | No arguments |
| `describe_queryable_entities` | Read only | Entity names |
| `query_entity` | Read only | Entity name, fields, filters, sort, joins, and row limit |
| `aggregate_entity` | Read only | Entity name, aggregate functions, group-by fields, filters, and row limit |
| `screen_drivers` | Creates a screen job | Screen criteria text, company ids or region codes, and `top_n` |
| `screen_earnings` | Creates a screen job | Screen criteria text, company ids or region codes, periods, and `top_n` |
| `get_screen_job` | Read only | A `job_id` from your own screen |
| `search_public_library` | Read only | Search query text, and optional document types, tickers, date range, and brokers |
| `get_library_document` | Read only | A document id |

A screen job is a record that the server writes for your account. It holds the screen inputs and, when the job ends, the result. Only your account can read it with `get_screen_job`.

Review each tool call in Claude before you approve it.

## Privacy and data handling

Read the [Distilla Privacy Policy](https://www.distilla.ai/privacy-policy) and the [Distilla Terms and Conditions](https://www.distilla.ai/terms-conditions). Those documents apply to your use of this plugin.

### What goes to Distilla

- **Tool arguments.** Claude sends the arguments of each tool call to `https://api.distilla.ai/mcp` over HTTPS. The tables above list the arguments.
- **Your account identity.** The server checks your OAuth token with Clerk and gets your Distilla user id. The server uses that id to scope screen jobs and to count usage.
- **Nothing else from Claude.** The server does not read your Claude conversation, Claude memory, chat history, or your files. It gets only the arguments that Claude puts in a tool call.

### What Distilla stores

- **Usage records.** For each tool call except `ping`, the server writes one usage record. The record holds your Distilla user id, the tool name, the time, the outcome (`ok` or `error`), the error class, and the sign-in type (OAuth or API key). It also holds the call arguments. The server cuts each text argument to 500 characters and each list to 20 items. For `company_ids`, it stores only the count. The record holds a short result summary, such as a row count. It does not hold result rows or document text.
- **Screen jobs.** `screen_drivers` and `screen_earnings` store the full screen inputs and the screen result for your account.
- **Retention.** The Distilla Privacy Policy states that Distilla keeps personal information no longer than three months after your account ends.

### Who else processes the data

- **Google Cloud.** Distilla runs the server on Google Cloud. `search_public_library`, `screen_drivers`, and `screen_earnings` send your query or criteria text to Google Gemini on Vertex AI to plan the search or to score companies.
- **Clerk.** Clerk runs Distilla sign-in and checks each access token.

### Your choices

- To stop all data flow, disable the plugin in `/plugin` or remove the `distilla` server in `/mcp`.
- To ask for a copy of your data or to delete it, email [support@distilla.ai](mailto:support@distilla.ai) or use [https://www.distilla.ai/contact-us](https://www.distilla.ai/contact-us).

## Validate

Run the validator before you submit a commit or tag a release:

```bash
claude plugin validate .
```

The `Validate plugin` GitHub workflow runs the same command on each pull request and on each push to `main`. To submit the plugin, use the Claude.ai or Console plugin form. See [Submitting your plugin](https://claude.com/docs/plugins/submit).

## Version

The plugin version is `1.0.0` in `.claude-plugin/plugin.json`. Bump that field when you want installed copies to receive a change.

## Security

Report a vulnerability as described in [SECURITY.md](SECURITY.md).

## Maintainer

Distilla, Inc.

- Website: [https://www.distilla.ai](https://www.distilla.ai)
- Email: [support@distilla.ai](mailto:support@distilla.ai)
- Repository: [https://github.com/Distilla-AI/distilla-mcp](https://github.com/Distilla-AI/distilla-mcp)

