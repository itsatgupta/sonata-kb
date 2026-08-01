"""POC v2: Voice Integration for Sonata Knowledge Assistant.

Adds STT (Whisper API) to the existing orchestrator.
Audio question -> transcribed text -> ask() -> text answer + citations.
TTS handled by frontend (Web Speech API, zero cost).

Run with the POC venv:
    cd 03-poc/agent
    uvicorn main:app --host 0.0.0.0 --port 8000

Requires:
    pip install openai
    export OPENAI_API_KEY=sk-...  (your existing API key)
"""

import os
import io
from openai import OpenAI

# Initialize OpenAI client (same key you use for Claude API if via OpenAI,
# or get a separate free-tier key at https://platform.openai.com)
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Reuse the existing POC orchestrator
from orchestrator import ask


def transcribe_audio(audio_bytes: bytes) -> str:
    """STT: Convert audio bytes to text using Whisper API.

    Free tier: 25,000 minutes/month (~$10 value).
    POC usage: ~50 minutes/month (well within free tier).
    Cost: $0.02/min after free tier.
    """
    transcript = openai_client.audio.transcriptions.create(
        model="whisper-1",
        file=("audio.wav", io.BytesIO(audio_bytes), "audio/wav"),
        language="en",
    )
    return transcript.text


def voice_ask(audio_bytes: bytes, direct: bool = False) -> dict:
    """Full pipeline: Audio -> Text -> Answer -> Return.

    Args:
        audio_bytes: Raw audio from browser
        direct: If True, skip LLM and return raw chunks (free)

    Returns:
        {
            "question": str,     # transcribed question
            "answer": str,       # answer with citations
            "citations": list,   # source citations
            "mode": str,         # "direct" or "openai" or "claude"
        }
    """
    import os

    # Step 1: Transcribe (Whisper STT)
    question = transcribe_audio(audio_bytes)
    print(f"[Voice] Transcribed: {question}")

    if direct:
        # Direct mode: retrieve chunks only, no LLM call
        from retrieval.hybrid_search import hybrid_search
        results = hybrid_search(question, namespace="wiki", max_results=5)

        if not results:
            return {"question": question, "answer": "No results found.", "citations": [], "mode": "direct"}

        chunks_text = []
        citations = []
        for r in results:
            text = r.get("text", r.get("content", ""))
            chunks_text.append(text)
            citations.append({
                "page": r.get("page_title", ""),
                "section": r.get("section_heading", ""),
                "url": r.get("page_url", ""),
                "updated": r.get("last_modified", ""),
            })

        answer = "\n\n---\n\n".join(chunks_text)
        return {"question": question, "answer": answer, "citations": citations, "mode": "direct"}
    else:
        # Check if OpenAI key is available (100x cheaper than Claude)
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            # Use GPT-3.5-turbo (~$0.001/query)
            from retrieval.hybrid_search import hybrid_search
            from openai import OpenAI

            results = hybrid_search(question, namespace="wiki", max_results=5)
            if not results:
                return {"question": question, "answer": "No results found.", "citations": [], "mode": "openai"}

            context_parts = []
            citations = []
            for r in results:
                text = r.get("text", r.get("content", ""))
                context_parts.append(text)
                citations.append({
                    "page": r.get("page_title", ""),
                    "section": r.get("section_heading", ""),
                    "url": r.get("page_url", ""),
                    "updated": r.get("last_modified", ""),
                })

            context = "\n\n---\n\n".join(context_parts)
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Answer the question based ONLY on the provided context. Cite sources where possible. Be concise and accurate."},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
                ],
                max_tokens=500,
                temperature=0.3,
            )
            answer = response.choices[0].message.content
            return {"question": question, "answer": answer, "citations": citations, "mode": "openai"}
        else:
            # Fallback to Claude (~$0.11/query)
            answer, citations = ask(question)
            return {"question": question, "answer": answer, "citations": citations, "mode": "claude"}


def voice_ask_simple(audio_bytes: bytes) -> dict:
    """Simplified version for quick testing.

    Usage:
        from orchestrator_voice import voice_ask_simple
        result = voice_ask_simple(audio_bytes)
        print(result["answer"])
    """
    return voice_ask(audio_bytes)
