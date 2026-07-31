"""
X-ray tool — Phase 2 scope. Not required for POC. Stubbed so the orchestrator can
register the schema now without breaking when the tool is called before Phase 2
ingestion exists.
"""
from typing import Optional


def xray_search(story_key: Optional[str] = None, module: Optional[str] = None) -> list[dict]:
    # TODO Phase 2: implement via X-ray API (Jira plugin API or standalone, depending
    # on your instance — see 04-data-sources/xray.md).
    return []


TOOL_SCHEMAS = [
    {
        "name": "xray_search",
        "description": (
            "[Phase 2 — stubbed, returns empty] Search X-ray test cases linked to a "
            "Jira story or module, with pass/fail execution history."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "story_key": {"type": "string"},
                "module": {"type": "string"},
            },
        },
    },
]

DISPATCH = {"xray_search": xray_search}
