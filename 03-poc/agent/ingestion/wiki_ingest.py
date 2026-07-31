"""
POC ingestion script: fetch the wiki page(s) for the pilot feature (see
03-poc/poc-candidate-selection.md) and index them into the local VectorIndex.

Usage:
    python ingestion/wiki_ingest.py --page-id 123456 --page-id 123789

Adjust `_fetch_page` for your actual wiki platform if not Confluence-compatible.
"""
import argparse
import os
import sys

import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.env import load_env  # loads 03-poc/agent/.env into os.environ

load_env()

from retrieval.chunking import chunk_markdown_by_heading
from retrieval.index import VectorIndex

WIKI_BASE_URL = os.environ.get("WIKI_BASE_URL", "").rstrip("/")
WIKI_API_TOKEN = os.environ.get("WIKI_API_TOKEN", "")


def _fetch_page(page_id: str) -> dict:
    resp = requests.get(
        f"{WIKI_BASE_URL}/rest/api/content/{page_id}",
        params={"expand": "body.storage,version,space"},
        headers={"Authorization": f"Bearer {WIKI_API_TOKEN}"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def _html_to_markdown(html: str) -> str:
    # POC-quality conversion. Swap for a proper HTML->MD converter (e.g. markdownify)
    # if formatting fidelity matters more before scaling to Phase 1's full corpus.
    try:
        from markdownify import markdownify
        return markdownify(html)
    except ImportError:
        import re
        text = re.sub(r"<[^>]+>", "", html)
        return text


def ingest_pages(page_ids: list[str], namespace: str = "wiki"):
    index = VectorIndex(namespace=namespace)
    all_chunks = []
    for pid in page_ids:
        page = _fetch_page(pid)
        title = page["title"]
        space = page.get("space", {}).get("key", "")
        last_modified = page.get("version", {}).get("when", "")
        url = f"{WIKI_BASE_URL}{page.get('_links', {}).get('webui', '')}"
        html = page.get("body", {}).get("storage", {}).get("value", "")
        md = _html_to_markdown(html)
        sections = chunk_markdown_by_heading(md)
        for s in sections:
            all_chunks.append(
                {
                    "text": s["text"],
                    "metadata": {
                        "page_title": title,
                        "section_heading": s["heading"],
                        "page_url": url,
                        "last_modified": last_modified,
                        "space": space,
                    },
                }
            )
        print(f"Ingested page {pid} ('{title}'): {len(sections)} sections")
    index.add(all_chunks)
    print(f"Total chunks indexed this run: {len(all_chunks)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--page-id", action="append", required=True, dest="page_ids")
    parser.add_argument("--namespace", default="wiki",
                        help="index namespace to write to (e.g. wiki, wiki_directupload)")
    args = parser.parse_args()
    ingest_pages(args.page_ids, namespace=args.namespace)
