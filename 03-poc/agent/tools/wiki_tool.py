"""
Wiki tool — read-only search/fetch over ingested wiki content.

POC note: this module assumes wiki pages have already been fetched and indexed
into the local vector store (see retrieval/index.py). Swap `_fetch_from_wiki_api`
for your actual wiki platform's API (Confluence REST API is the common case —
adjust WIKI_BASE_URL/token handling accordingly).
"""
import os
import requests
from dataclasses import dataclass, asdict
from typing import Optional

from retrieval.index import VectorIndex

WIKI_BASE_URL = os.environ.get("WIKI_BASE_URL", "").rstrip("/")
WIKI_API_TOKEN = os.environ.get("WIKI_API_TOKEN", "")

_index = VectorIndex(namespace=os.environ.get("WIKI_NAMESPACE", "wiki"))


@dataclass
class WikiChunk:
    page_title: str
    section_heading: str
    text: str
    page_url: str
    last_modified: str
    citation: str


def wiki_search(query: str, space: Optional[str] = None, max_results: int = 5) -> list[dict]:
    """Hybrid (keyword + vector) search over indexed wiki chunks. Read-only."""
    hits = _index.search(query, filters={"space": space} if space else None, top_k=max_results)
    results = []
    for h in hits:
        chunk = WikiChunk(
            page_title=h["metadata"]["page_title"],
            section_heading=h["metadata"].get("section_heading", ""),
            text=h["text"],
            page_url=h["metadata"]["page_url"],
            last_modified=h["metadata"]["last_modified"],
            citation=f"Wiki: {h['metadata']['page_title']} \u00a7 "
                     f"{h['metadata'].get('section_heading', '(page)')} "
                     f"(updated {h['metadata']['last_modified']})",
        )
        results.append(asdict(chunk))
    return results


def wiki_get_page(page_id: str) -> dict:
    """Fetch a full page (all sections) by id — used for follow-up context."""
    return _fetch_from_wiki_api(f"/rest/api/content/{page_id}?expand=body.storage,version")


def _fetch_from_wiki_api(path: str) -> dict:
    """Direct call to the wiki REST API — used only for wiki_get_page (single-page
    fetch), NOT for search. Ingestion pipeline (separate script, see
    ingestion/wiki_ingest.py, TODO) is what populates the vector index in bulk.
    """
    if not WIKI_BASE_URL:
        raise RuntimeError("WIKI_BASE_URL not configured — see config/env.example.txt")
    resp = requests.get(
        f"{WIKI_BASE_URL}{path}",
        headers={"Authorization": f"Bearer {WIKI_API_TOKEN}"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


# --- Claude tool-use schema (imported by orchestrator.py) ---
TOOL_SCHEMAS = [
    {
        "name": "wiki_search",
        "description": (
            "Search Sonata wiki (design/arch/tech specs and release notes) for content "
            "relevant to a functional or technical question. Always cite results by "
            "page title and section — never answer from memory without this tool."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "space": {"type": "string", "description": "Optional wiki space filter"},
                "max_results": {"type": "integer", "default": 5},
            },
            "required": ["query"],
        },
    },
    {
        "name": "wiki_get_page",
        "description": "Fetch a full wiki page by id when surrounding context beyond a single chunk is needed.",
        "input_schema": {
            "type": "object",
            "properties": {"page_id": {"type": "string"}},
            "required": ["page_id"],
        },
    },
]

DISPATCH = {"wiki_search": wiki_search, "wiki_get_page": wiki_get_page}
