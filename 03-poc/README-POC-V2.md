# POC v2: Voice Assistant for Sonata Knowledge Assistant

## What This Is

A fully working voice assistant that answers Sonata functional questions:
- You speak a question
- Bot transcribes it (Whisper API)
- Bot retrieves answer from knowledge base
- Bot speaks the answer back (Web Speech API)
- Shows source citations below

## Cost: $0 (All Free Tiers)

- Whisper STT: Free (25K min/month)
- Web Speech TTS: Browser built-in (unlimited)
- Render backend: Free tier
- Vercel frontend: Free tier

## Quick Start

### Option A: Run Locally First

```bash
# 1. Install dependencies
cd 03-poc/agent
pip install -r requirements.txt

# 2. Set API key
export OPENAI_API_KEY=sk-your-key

# 3. Start backend
uvicorn main:app --host 0.0.0.0 --port 8000

# 4. Open browser
# Visit http://localhost:8000/api/health
```

### Option B: Deploy to Vercel + Render

See `DEPLOYMENT-POC-V2.md` for step-by-step guide.

## Files

| File | Purpose |
|------|---------|
| `agent/orchestrator_voice.py` | Whisper STT integration |
| `agent/main.py` | FastAPI backend endpoint |
| `ui/components/VoiceAssistant.jsx` | Frontend mic + audio |
| `DEPLOYMENT-POC-V2.md` | Deploy guide |
| `DEMO-SCRIPT-POC-V2.md` | Demo walkthrough |
| `TROUBLESHOOTING-POC-V2.md` | Common issues |

## API Endpoints

- `GET /` — Service info
- `GET /api/health` — Health check
- `POST /api/voice-ask` — Upload audio, get answer + citations
- `GET /api/text-ask?q=...` — Text-only test (no audio)

## Demo

See `DEMO-SCRIPT-POC-V2.md` for the 45-minute stakeholder demo.
