"""Listing-repo contract tests for declared MCP tools.

These tests prove the public listing contract that MCP trust scanners
(e.g. M8ven) score: each declared tool is named here and stays consistent
with chatgpt-app-submission.json and the README Tools table.

They do not call the hosted Distilla MCP server. Handler correctness stays
in pipeline-data agent2_mcp_shim tests.

ChatGPT positive test_cases currently omit ping and screen_earnings; that
gap is out of band for this suite (see docs/specs/m8ven-declared-tool-tests.md).
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Every name must appear as a string literal so scanners can attribute
# coverage to this file.
DECLARED_TOOLS = (
    "ping",
    "list_queryable_entities",
    "describe_queryable_entities",
    "query_entity",
    "aggregate_entity",
    "screen_drivers",
    "screen_earnings",
    "get_screen_job",
    "search_public_library",
    "get_library_document",
)


def _load_chatgpt() -> dict:
    path = ROOT / "chatgpt-app-submission.json"
    return json.loads(path.read_text(encoding="utf-8"))


class DeclaredToolsContractTest(unittest.TestCase):
    def test_chatgpt_tools_match_declared_set(self) -> None:
        tools = _load_chatgpt()["tools"]
        self.assertEqual(set(tools), set(DECLARED_TOOLS))

    def test_each_tool_has_annotations_and_justifications(self) -> None:
        tools = _load_chatgpt()["tools"]
        for name in DECLARED_TOOLS:
            with self.subTest(tool=name):
                entry = tools[name]
                self.assertIn("annotations", entry)
                self.assertIn("justifications", entry)
                self.assertIsInstance(entry["annotations"], dict)
                self.assertIsInstance(entry["justifications"], dict)

    def test_each_tool_is_named_in_readme(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for name in DECLARED_TOOLS:
            with self.subTest(tool=name):
                self.assertIn(f"`{name}`", readme)


if __name__ == "__main__":
    unittest.main()
