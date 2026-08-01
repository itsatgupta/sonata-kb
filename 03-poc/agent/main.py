"""POC v2: FastAPI backend for voice assistant.

Adds a /api/voice-ask endpoint that receives audio,
transcribes via Whisper, answers via orchestrator, returns text.
Frontend handles TTS via Web Speech API (zero cost).

Run with:
    cd 03-poc/agent
    pip install fastapi uvicorn python-multipart openai
    uvicorn main:app --host 0.0.0.0 --port 8000

Or deploy to Render (see DEPLOYMENT.md).
"""

import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from orchestrator_voice import voice_ask

app = FastAPI(
    title="Sonata Voice Assistant POC",
    version="0.2.0",
    description="Voice-enabled Q&A for Sonata functional questions",
)

# CORS: Allow frontend (Vercel) to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten for production: list your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Sonata Voice Assistant POC v2",
        "version": "0.2.0",
        "endpoints": {
            "voice_ask": "POST /api/voice-ask (upload audio file)",
            "health": "GET /api/health",
        },
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "whisper": "configured" if os.getenv("OPENAI_API_KEY") else "missing key",
        "orchestrator": "loaded",
    }


@app.post("/api/voice-ask")
async def voice_endpoint(file: UploadFile = File(...)):
    """Receive audio, transcribe, answer, return text + citations.

    Request: multipart/form-data with 'file' field (audio/wav)
    Response: JSON with question, answer, citations

    The frontend then uses Web Speech API to speak the answer (zero cost).
    """
    # Read audio bytes from upload
    audio_bytes = await file.read()

    if len(audio_bytes) == 0:
        return {"error": "Empty audio file received"}

    # Run voice pipeline: audio -> text -> answer -> return
    try:
        result = voice_ask(audio_bytes)
        return result
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/text-ask")
def text_endpoint(q: str, direct: bool = False):
    """Text-only endpoint for testing without audio.

    Usage:
        GET /api/text-ask?q=How does searchEmployer work?
        GET /api/text-ask?q=How does searchEmployer work?&direct=true  (skip Claude, free)

    direct=true returns raw retrieved chunks without calling Claude API.
    Faster, free, but less polished answers.
    """
    if direct:
        # Direct mode: retrieve chunks only, no LLM call
        from retrieval.hybrid_search import hybrid_search
        results = hybrid_search(q, namespace="wiki", max_results=5)

        if not results:
            return {"question": q, "answer": "No results found.", "citations": []}

        # Format chunks as answer
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
        return {"question": q, "answer": answer, "citations": citations, "mode": "direct"}
    else:
        # Check if OpenAI key is available (100x cheaper than Claude)
        import os
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            return _ask_openai(q, openai_key)
        else:
            # Fallback to Claude
            from orchestrator import ask
            answer, citations = ask(q)
            return {"question": q, "answer": answer, "citations": citations, "mode": "claude"}


def _ask_openai(q: str, api_key: str):
    """Use OpenAI GPT-3.5-turbo (100x cheaper than Claude)."""
    from retrieval.hybrid_search import hybrid_search
    from openai import OpenAI

    # Retrieve relevant chunks
    results = hybrid_search(q, namespace="wiki", max_results=5)

    if not results:
        return {"question": q, "answer": "No results found.", "citations": [], "mode": "openai"}

    # Build context from chunks
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

    # Call GPT-3.5-turbo (cost: ~$0.001 per query)
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Answer the question based ONLY on the provided context. Cite sources where possible. Be concise and accurate."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {q}"}
        ],
        max_tokens=500,
        temperature=0.3,
    )

    answer = response.choices[0].message.content
    return {"question": q, "answer": answer, "citations": citations, "mode": "openai"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
