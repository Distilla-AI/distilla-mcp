#!/usr/bin/env python3
"""Project shared plugin metadata from manifest/core.json into platform JSON files.

Edit manifest/core.json, then run:

  python3 scripts/generate_manifests.py

CI uses --check to fail when committed outputs drift from the SoT.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CORE_PATH = ROOT / "manifest" / "core.json"

TARGETS = {
    "mcp": ROOT / ".mcp.json",
    "claude": ROOT / ".claude-plugin" / "plugin.json",
    "codex": ROOT / ".codex-plugin" / "plugin.json",
    "chatgpt": ROOT / "chatgpt-app-submission.json",
    "registry": ROOT / "server.json",
}

REGISTRY_SCHEMA = (
    "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json"
)
REGISTRY_DESCRIPTION_MAX = 100


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def load_or_empty(path: Path) -> dict[str, Any]:
    if path.is_file():
        return load_json(path)
    return {}


def project_mcp(core: dict[str, Any], existing: dict[str, Any]) -> dict[str, Any]:
    plugin_id = core["id"]
    out = dict(existing) if existing else {}
    servers = dict(out.get("mcpServers") or {})
    entry = dict(servers.get(plugin_id) or {})
    entry["type"] = "http"
    entry["url"] = core["urls"]["mcp"]
    servers[plugin_id] = entry
    out["mcpServers"] = servers
    return out


def project_claude(core: dict[str, Any], existing: dict[str, Any]) -> dict[str, Any]:
    out = dict(existing) if existing else {}
    if "$schema" not in out:
        out["$schema"] = "https://json.schemastore.org/claude-code-plugin-manifest.json"
    out["name"] = core["id"]
    out["displayName"] = core["displayName"]
    out["version"] = core["version"]
    out["description"] = core["descriptionShort"]
    out["icon"] = core["icon"]
    out["author"] = dict(core["author"])
    out["homepage"] = core["urls"]["homepage"]
    out["repository"] = core["urls"]["repository"]
    out["license"] = core["license"]
    out["keywords"] = list(core["keywords"])
    out["defaultEnabled"] = core["defaultEnabled"]
    return out


def project_codex(core: dict[str, Any], existing: dict[str, Any]) -> dict[str, Any]:
    out = dict(existing) if existing else {}
    out["name"] = core["id"]
    out["version"] = core["version"]
    out["description"] = core["descriptionShort"]
    out["author"] = dict(core["author"])
    out["homepage"] = core["urls"]["homepage"]
    out["repository"] = core["urls"]["repository"]
    out["license"] = core["license"]
    out["keywords"] = list(core["keywords"])
    out["mcpServers"] = "./.mcp.json"

    interface = dict(out.get("interface") or {})
    interface["displayName"] = core["displayName"]
    interface["shortDescription"] = core["subtitle"]
    interface["longDescription"] = core["descriptionLong"]
    interface["developerName"] = core["author"]["name"]
    interface["category"] = core["category"]["codex"]
    interface["websiteURL"] = core["urls"]["agents"]
    interface["supportURL"] = core["urls"]["support"]
    interface["privacyPolicyURL"] = core["urls"]["privacy"]
    interface["termsOfServiceURL"] = core["urls"]["terms"]
    out["interface"] = interface
    return out


def project_chatgpt(core: dict[str, Any], existing: dict[str, Any]) -> dict[str, Any]:
    out = dict(existing) if existing else {}
    app_info = dict(out.get("app_info") or {})
    app_info["display_name"] = core["chatgptDisplayName"]
    app_info["subtitle"] = core["subtitle"]
    app_info["description"] = core["descriptionLong"]
    app_info["category"] = core["category"]["chatgpt"]
    out["app_info"] = app_info
    return out


def project_registry(core: dict[str, Any], existing: dict[str, Any]) -> dict[str, Any]:
    """Official MCP Registry server.json (full file from SoT; no platform overlay)."""
    del existing  # entire file is generated
    registry = core["registry"]
    description = registry["description"]
    if len(description) > REGISTRY_DESCRIPTION_MAX:
        raise ValueError(
            f"registry.description must be ≤{REGISTRY_DESCRIPTION_MAX} chars "
            f"(got {len(description)})"
        )
    agents = core["urls"]["agents"].rstrip("/") + "/"
    return {
        "$schema": REGISTRY_SCHEMA,
        "name": registry["name"],
        "title": core["chatgptDisplayName"],
        "description": description,
        "version": core["version"],
        "websiteUrl": agents,
        "icons": [
            {
                "src": registry["iconUrl"],
                "mimeType": "image/png",
                "sizes": [registry["iconSizes"]],
            }
        ],
        "remotes": [
            {
                "type": "streamable-http",
                "url": core["urls"]["mcp"],
            }
        ],
    }


PROJECTORS = {
    "mcp": project_mcp,
    "claude": project_claude,
    "codex": project_codex,
    "chatgpt": project_chatgpt,
    "registry": project_registry,
}


def build_all(core: dict[str, Any]) -> dict[str, str]:
    rendered: dict[str, str] = {}
    for key, path in TARGETS.items():
        projected = PROJECTORS[key](core, load_or_empty(path))
        rendered[key] = dump_json(projected)
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if any target would change (do not write).",
    )
    args = parser.parse_args()

    if not CORE_PATH.is_file():
        print(f"missing SoT: {CORE_PATH}", file=sys.stderr)
        return 1

    core = load_json(CORE_PATH)
    rendered = build_all(core)

    if args.check:
        drifted: list[str] = []
        for key, path in TARGETS.items():
            on_disk = path.read_text(encoding="utf-8") if path.is_file() else ""
            if on_disk != rendered[key]:
                drifted.append(str(path.relative_to(ROOT)))
        if drifted:
            print("manifests drift from manifest/core.json:", file=sys.stderr)
            for rel in drifted:
                print(f"  - {rel}", file=sys.stderr)
            print(
                "Run: python3 scripts/generate_manifests.py",
                file=sys.stderr,
            )
            return 1
        print("OK: platform manifests match manifest/core.json")
        return 0

    for key, path in TARGETS.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered[key], encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
