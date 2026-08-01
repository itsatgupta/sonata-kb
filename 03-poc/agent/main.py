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
def text_endpoint(q: str):
    """Text-only endpoint for testing without audio.

    Usage: GET /api/text-ask?q=How does searchEmployer work?
    """
    from orchestrator import ask
    answer, citations = ask(q)
    return {"question": q, "answer": answer, "citations": citations}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
