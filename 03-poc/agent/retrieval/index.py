"""
Minimal local vector index for the POC. Deliberately simple (TF-IDF + cosine, plus
a keyword substring boost) so the POC has zero new infra dependency — swap this for
your org's actual licensed vector store (see 01-architecture/system-design.md: "avoid
a new procurement cycle for the POC") once retrieval quality is validated and you're
scaling past one pilot feature in Phase 1.

Persistence: chunks are stored as JSON on disk under data/<namespace>.json — good
enough for a single small feature area; Phase 1 needs a real vector DB.
"""
import json
import os
from pathlib import Path
from typing import Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_DIR = Path(os.environ.get("SONATA_KB_DATA_DIR", "./data"))


class VectorIndex:
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.path = DATA_DIR / f"{namespace}.json"
        self._chunks: list[dict] = []
        self._vectorizer: Optional[TfidfVectorizer] = None
        self._matrix = None
        self._load()

    def _load(self):
        if self.path.exists():
            self._chunks = json.loads(self.path.read_text())
            self._fit()

    def _fit(self):
        if not self._chunks:
            return
        texts = [c["text"] for c in self._chunks]
        self._vectorizer = TfidfVectorizer(stop_words="english", max_features=20000)
        self._matrix = self._vectorizer.fit_transform(texts)

    def add(self, chunks: list[dict]):
        """chunks: [{text, metadata: {...}}, ...]. Replaces the namespace content.

        POC ingests rebuild a namespace from scratch (see ingestion/wiki_ingest.py),
        so this overwrites rather than appends — otherwise re-ingesting a page after
        a chunking change leaves stale duplicate chunks in the index.
        """
        self._chunks = list(chunks)
        self._fit()
        self._save()

    def _save(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._chunks, indent=2))

    def search(self, query: str, filters: Optional[dict] = None, top_k: int = 5) -> list[dict]:
        if not self._chunks or self._vectorizer is None:
            return []
        q_vec = self._vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self._matrix)[0]
        ranked = sorted(range(len(self._chunks)), key=lambda i: sims[i], reverse=True)
        results = []
        for i in ranked:
            chunk = self._chunks[i]
            if filters:
                if any(chunk["metadata"].get(k) != v for k, v in filters.items() if v):
                    continue
            if sims[i] <= 0:
                continue
            results.append({"text": chunk["text"], "metadata": chunk["metadata"], "score": float(sims[i])})
            if len(results) >= top_k:
                break
        return results
