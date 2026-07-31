"""
Bitbucket tool — Phase 2 scope. Stubbed in the POC: returns real PR metadata if
credentials are configured, but module-mapping is intentionally left "UNMAPPED"
until the path->module lookup table (see 04-data-sources/bitbucket.md) is built
with engineering input. Never guess a module mapping.
"""
import os
import requests
from dataclasses import dataclass, asdict
from typing import Optional

BITBUCKET_WORKSPACE = os.environ.get("BITBUCKET_WORKSPACE", "")
BITBUCKET_APP_PASSWORD = os.environ.get("BITBUCKET_APP_PASSWORD", "")


@dataclass
class PullRequest:
    pr_id: str
    title: str
    merged_date: str
    target_branch: str
    linked_jira_key: Optional[str]
    files_changed: list
    modules_touched: list
    url: str
    citation: str


def bitbucket_search(
    jira_key: Optional[str] = None, module: Optional[str] = None, since: Optional[str] = None
) -> list[dict]:
    if not BITBUCKET_WORKSPACE:
        return []  # not configured — POC can run without this tool
    # TODO Phase 2: implement real search via Bitbucket REST API
    # (GET /2.0/repositories/{workspace}/{repo}/pullrequests, filter by merge date/
    # jira key parsed from title/branch per your team's convention — see
    # 04-data-sources/bitbucket.md open questions before trusting the parse).
    raise NotImplementedError(
        "bitbucket_search: Phase 2 scope — see sonata-kb/02-phases/phase-2-code-and-test-layer.md"
    )


TOOL_SCHEMAS = [
    {
        "name": "bitbucket_search",
        "description": (
            "[Phase 2 — not yet implemented] Search Bitbucket PRs by linked Jira key, "
            "module, or date. Returns files/modules touched."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "jira_key": {"type": "string"},
                "module": {"type": "string"},
                "since": {"type": "string"},
            },
        },
    },
]

DISPATCH = {"bitbucket_search": bitbucket_search}
