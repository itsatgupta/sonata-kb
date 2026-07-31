"""
Jira tool — read-only search over Sonata epics/stories/defects.

`jira_version_range` is the single most important function in the POC/Phase-3 path:
it's the core primitive that makes "what changed between v_a and v_b" answerable.
Get this right before building anything else in Phase 3 (see CLAUDE.md).
"""
import os
import requests
from dataclasses import dataclass, asdict
from typing import Optional

JIRA_BASE_URL = os.environ.get("JIRA_BASE_URL", "")
JIRA_USER_EMAIL = os.environ.get("JIRA_USER_EMAIL", "")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN", "")
JIRA_PROJECT_KEY = os.environ.get("JIRA_PROJECT_KEY", "SONATA")

FIELDS = "summary,description,issuetype,customfield_22644,fixVersions,components,status,issuelinks"


@dataclass
class JiraIssue:
    key: str
    type: str
    summary: str
    description: str
    acceptance_criteria: str
    fix_versions: list
    components: list
    status: str
    linked_issues: list
    url: str
    citation: str


def _auth_mode() -> str:
    """'basic' (Jira Cloud: email + API token) or 'bearer' (Server/DC: PAT).

    Default is inferred from the host — *.atlassian.net is treated as Cloud,
    everything else as Server/Data Center. Override explicitly with
    JIRA_AUTH=basic|bearer in .env if the inference is wrong.
    """
    mode = os.environ.get("JIRA_AUTH", "").strip().lower()
    if mode in ("basic", "bearer"):
        return mode
    host = JIRA_BASE_URL.split("//")[-1].split("/")[0].lower()
    return "basic" if host.endswith("atlassian.net") else "bearer"


def _request_kwargs() -> dict:
    """requests kwargs (auth tuple or Authorization header) for the current mode."""
    mode = _auth_mode()
    if mode == "basic":
        return {"auth": (JIRA_USER_EMAIL, JIRA_API_TOKEN)}
    if not JIRA_API_TOKEN:
        raise RuntimeError(
            "JIRA_API_TOKEN is empty — required for bearer (Server/DC PAT) auth, "
            "see config/env.example.txt"
        )
    return {"headers": {"Authorization": f"Bearer {JIRA_API_TOKEN}"}}


def _default_api_version() -> str:
    """Jira Cloud uses api/3; Server/Data Center is commonly api/2. Infer from host."""
    host = JIRA_BASE_URL.split("//")[-1].split("/")[0].lower()
    return "3" if host.endswith("atlassian.net") else "2"


def _rest(path: str, params: Optional[dict] = None) -> requests.Response:
    """GET a Jira REST endpoint, tolerant of Cloud's api/3 vs Server/DC's api/2.

    Tries the inferred default api version (JIRA_API_VERSION env can override),
    then falls back to the other major version. A wrong api version is detected by
    404/405 OR a status-200 HTML body (Jira Server/DC serves a soft-404 HTML page
    with status 200 for unknown api versions, instead of a proper 404).
    """
    if not JIRA_BASE_URL:
        raise RuntimeError("JIRA_BASE_URL not configured — see config/env.example.txt")
    versions = [os.environ.get("JIRA_API_VERSION", "").strip() or _default_api_version()]
    versions += [v for v in ("3", "2") if v not in versions]
    last_status = None
    for ver in versions:
        url = f"{JIRA_BASE_URL}/rest/api/{ver}/{path}"
        resp = requests.get(url, params=params, timeout=20, **_request_kwargs())
        last_status = resp.status_code
        is_json = resp.headers.get("content-type", "").startswith("application/json")
        if resp.status_code in (404, 405) or (resp.status_code == 200 and not is_json):
            continue  # wrong api version for this instance — try next
        resp.raise_for_status()
        return resp
    raise RuntimeError(
        f"Jira REST API unreachable at {JIRA_BASE_URL}/rest/api/ "
        f"(tried versions {versions}, last status {last_status})"
    )


def _run_jql(jql: str, max_results: int = 50) -> list[dict]:
    params = {"jql": jql, "fields": FIELDS, "maxResults": max_results}
    try:
        resp = _rest("search", params=params)
        return resp.json().get("issues", [])
    except requests.exceptions.HTTPError as e:
        if e.response is None or e.response.status_code != 400 or "customfield" not in FIELDS:
            raise
        # FIELDS includes the template placeholder customfield_acceptance_criteria,
        # which won't exist on a real instance (each org's customfield ids differ).
        # Retry once with the safe field set rather than failing the whole query.
        params["fields"] = "summary,description,issuetype,customfield_22644,fixVersions,components,status,issuelinks"
        resp = _rest("search", params=params)
        return resp.json().get("issues", [])


def _to_issue(raw: dict) -> dict:
    f = raw["fields"]
    key = raw["key"]
    issue = JiraIssue(
        key=key,
        type=f.get("issuetype", {}).get("name", ""),
        summary=f.get("summary", ""),
        description=str(f.get("description", "") or ""),
        acceptance_criteria=str(f.get("customfield_acceptance_criteria", "") or ""),
        fix_versions=[v["name"] for v in f.get("fixVersions", [])],
        components=[c["name"] for c in f.get("components", [])],
        status=f.get("status", {}).get("name", ""),
        linked_issues=[
            l.get("outwardIssue", l.get("inwardIssue", {})).get("key")
            for l in f.get("issuelinks", [])
            if l.get("outwardIssue") or l.get("inwardIssue")
        ],
        url=f"{JIRA_BASE_URL}/browse/{key}",
        citation=f"Jira: {key} \u2014 {f.get('summary', '')}",
    )
    return asdict(issue)


def jira_search(
    jql: Optional[str] = None,
    query: Optional[str] = None,
    fix_version: Optional[str] = None,
    component: Optional[str] = None,
    project: Optional[str] = None,
    max_results: int = 20,
) -> list[dict]:
    """Search Jira issues. Pass raw `jql` for structured queries (e.g. `key = BASE-123`),
    or `query` for a free-text search over summary/description.

    The project scope is OPTIONAL: a single default project (e.g. SON) would silently
    hide tickets filed under other projects (this pilot's searchEmployer work is in
    BASE/FEAT), so we only scope to `project` when the caller passes it.
    """
    if not jql:
        clauses = []
        if project:
            clauses.append(f"project = {project}")
        if query:
            clauses.append(f'(summary ~ "{query}" OR description ~ "{query}")')
        if fix_version:
            clauses.append(f'fixVersion = "{fix_version}"')
        if component:
            clauses.append(f'component = "{component}"')
        jql = " AND ".join(clauses)
    raw_issues = _run_jql(jql, max_results=max_results)
    return [_to_issue(r) for r in raw_issues]


def jira_version_range(from_version: str, to_version: str, component: Optional[str] = None) -> list[dict]:
    """
    Resolve every Jira issue delivered in the trunk releases strictly after
    `from_version` up to and including `to_version`.

    IMPORTANT (see 04-data-sources/jira.md open questions): this assumes fixVersion
    naming is consistent and sortable (e.g. "v11.4", "v11.5", ...). If your Jira
    project's fixVersion hygiene is inconsistent, this function's output should be
    treated as provisional and cross-checked against release notes — flag this to
    the user rather than silently trusting it.
    """
    versions_in_range = _resolve_trunk_versions_between(from_version, to_version)
    if not versions_in_range:
        return []
    version_clause = " ,".join(f'"{v}"' for v in versions_in_range)
    clauses = [
        f"project = {JIRA_PROJECT_KEY}",
        f"fixVersion in ({version_clause})",
    ]
    if component:
        clauses.append(f'component = "{component}"')
    jql = " AND ".join(clauses)
    raw_issues = _run_jql(jql, max_results=200)
    return [_to_issue(r) for r in raw_issues]


def _resolve_trunk_versions_between(from_version: str, to_version: str) -> list[str]:
    """
    TODO (Phase 3 prerequisite): replace this with a real lookup against the
    validated fixVersion -> trunk-release mapping described in
    04-data-sources/jira.md. For the POC, this can call Jira's
    /rest/api/3/project/{key}/versions endpoint and sort by release date.
    Do NOT assume string-sort order of version numbers is correct
    (e.g. "v9" vs "v10") — sort by the Jira version's actual release date field.
    """
    resp = _rest(f"project/{JIRA_PROJECT_KEY}/versions")
    versions = resp.json()
    versions_sorted = sorted(
        [v for v in versions if v.get("releaseDate")],
        key=lambda v: v["releaseDate"],
    )
    names = [v["name"] for v in versions_sorted]
    try:
        i_from = names.index(from_version)
        i_to = names.index(to_version)
    except ValueError:
        return []
    return names[i_from + 1 : i_to + 1]


TOOL_SCHEMAS = [
    {
        "name": "jira_search",
        "description": (
            "Search Sonata Jira issues (epics/stories/defects) by free text, JQL, "
            "fixVersion, component, or project. Use for functional Q&A grounded in "
            "acceptance criteria and defect history. To look up a SPECIFIC issue, "
            "always pass jql like 'key = BASE-123' — the free-text query searches "
            "summary/description and cannot match an issue key."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "jql": {"type": "string", "description": "Raw JQL, for advanced/structured queries"},
                "query": {"type": "string", "description": "Free-text search over summary/description"},
                "fix_version": {"type": "string"},
                "component": {"type": "string"},
                "project": {"type": "string", "description": "Optional project key to scope the search (e.g. SON, BASE)"},
                "max_results": {"type": "integer", "default": 20},
            },
        },
    },
    {
        "name": "jira_version_range",
        "description": (
            "Resolve all Jira issues delivered between two Sonata trunk versions "
            "(exclusive of from_version, inclusive of to_version). This is the core "
            "tool for 'what changed between v_a and v_b' and upgrade impact questions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "from_version": {"type": "string"},
                "to_version": {"type": "string"},
                "component": {"type": "string"},
            },
            "required": ["from_version", "to_version"],
        },
    },
]

DISPATCH = {"jira_search": jira_search, "jira_version_range": jira_version_range}
