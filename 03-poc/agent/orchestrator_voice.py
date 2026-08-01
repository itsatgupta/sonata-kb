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


def voice_ask(audio_bytes: bytes) -> dict:
    """Full pipeline: Audio -> Text -> Answer -> Return.

    Returns:
        {
            "question": str,     # transcribed question
            "answer": str,       # LLM answer with citations
            "citations": list,   # source citations
        }
    """
    # Step 1: Transcribe (Whisper STT)
    question = transcribe_audio(audio_bytes)
    print(f"[Voice] Transcribed: {question}")

    # Step 2: Answer using existing POC logic
    answer, citations = ask(question)
    print(f"[Voice] Answer: {answer[:100]}...")

    # Step 3: Return (frontend handles TTS via Web Speech API)
    return {
        "question": question,
        "answer": answer,
        "citations": citations,
    }


def voice_ask_simple(audio_bytes: bytes) -> dict:
    """Simplified version for quick testing.

    Usage:
        from orchestrator_voice import voice_ask_simple
        result = voice_ask_simple(audio_bytes)
        print(result["answer"])
    """
    return voice_ask(audio_bytes)
