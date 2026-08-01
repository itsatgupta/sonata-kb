# POC Enhancement: Add Voice Demo Before Phase 1

**Context:** Current POC proved retrieval + Q&A (27/27 correct). Adding voice shows end-to-end system + demo value.

---

## Option 1: POC v2 (Current Path — Text Only)
- ✅ What we have: searchEmployer Q&A (27/27 correct)
- ✅ Demo to stakeholders: "Here's the bot answering questions"
- ⚠️ Limitation: Text only (less impressive, feels incomplete)
- Timeline: Deploy as-is (ready now)

---

## Option 2: POC v2 + Voice (Recommended)
- ✅ What we add: STT + TTS (Speech-to-Text + Text-to-Speech)
- ✅ Demo to stakeholders: "Here's the bot answering your questions by voice"
- ✅ Shows end-to-end working system
- ✅ More impressive + credible (not just a text chatbot)
- ✅ Uses your existing Vercel + Render accounts (no new infra)
- Timeline: +2 weeks beyond POC completion

---

## How to Add Voice to POC (2 Weeks)

### **Week 1: Backend (Voice Integration)**

**Add to existing orchestrator.py:**

```python
# New: STT pipeline (Whisper API)
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(audio_bytes):
    """Speech → Text (via Whisper)"""
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=("audio.wav", audio_bytes)
    )
    return transcript.text

# Existing: ask() function (already works)
answer, citations = ask(transcript.text)  # Same logic

# New: TTS pipeline (Google Cloud TTS or ElevenLabs)
from google.cloud import tts_v1

def synthesize_speech(text):
    """Text → Speech"""
    client = tts_v1.TextToSpeechClient()
    synthesis_input = tts_v1.SynthesisInput(text=text)
    voice = tts_v1.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Neural2-A"
    )
    audio_config = tts_v1.AudioConfig(audio_encoding=tts_v1.AudioEncoding.MP3)
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content  # MP3 bytes

# Pipeline: Audio → Text → Answer → Audio
def voice_ask(audio_bytes):
    text = transcribe_audio(audio_bytes)
    answer, citations = ask(text)
    audio = synthesize_speech(answer)
    return audio, citations
```

**Effort:** 
- Whisper integration: 2 hours (free, simple API)
- TTS integration: 2 hours (Google/ElevenLabs, ~$0.50/1000 chars)
- Testing: 2 hours
- **Total: ~6 hours backend work**

---

### **Week 2: Frontend (UI + Deploy)**

**New Next.js component (React):**

```jsx
import { useState } from 'react';

export default function VoiceDemo() {
  const [recording, setRecording] = useState(false);
  const [answer, setAnswer] = useState('');
  const [playing, setPlaying] = useState(false);

  const startRecording = async () => {
    setRecording(true);
    const mediaRecorder = new MediaRecorder(await navigator.mediaDevices.getUserMedia({ audio: true }));
    let chunks = [];
    
    mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
    mediaRecorder.onstop = async () => {
      const audio = new Blob(chunks, { type: 'audio/wav' });
      const formData = new FormData();
      formData.append('audio', audio);
      
      // Send to Render backend
      const res = await fetch('/api/voice-ask', { method: 'POST', body: formData });
      const { audio: responseAudio, citations } = await res.json();
      
      setAnswer(`${responseAudio} | Sources: ${citations}`);
      playAudio(responseAudio);
    };
    
    mediaRecorder.start();
  };

  const stopRecording = () => {
    setRecording(false);
    // Stop media recorder
  };

  const playAudio = (audioData) => {
    const audio = new Audio(`data:audio/mp3;base64,${audioData}`);
    audio.play();
    setPlaying(true);
  };

  return (
    <div className="voice-demo">
      <h2>🎙️ Sonata Voice Assistant</h2>
      <button onClick={startRecording} disabled={recording}>
        {recording ? '🔴 Recording...' : '🎤 Ask a Question'}
      </button>
      <button onClick={stopRecording} disabled={!recording}>Stop</button>
      {answer && (
        <div>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}
```

**Deploy:**
- Frontend: `vercel deploy` (your Vercel account)
- Backend: `render deploy` (your Render account)
- Total deployment time: 1 hour

**Effort:**
- Frontend UI: 4 hours
- Testing: 2 hours
- Deployment: 1 hour
- **Total: ~7 hours frontend work**

---

## What You Demonstrate (Week 3)

```
Demo flow:
1. Click "🎤 Ask"
2. Speak: "How does searchEmployer work?"
3. Bot hears (Whisper transcription shows on screen)
4. Bot answers: "searchEmployer is a feature that allows..."
5. Bot speaks the answer (TTS audio plays)
6. Sources shown below: Wiki link, Jira key, timestamp

Live demo in 45 seconds. Highly impressive.
Stakeholders see: End-to-end working product, not a prototype.
```

---

## Cost Analysis: POC v2 + Voice

| Item | Cost | Notes |
|---|---|---|
| **Backend** | | |
| Render (Standard tier) | $20/month | Already have account |
| Whisper API | Free | 50,000 min/month free tier |
| TTS (Google Cloud) | ~$50/month | ~$0.50 per 1000 chars |
| Claude API | Already budgeted | Same as POC |
| **Frontend** | | |
| Vercel | Free | Already have account |
| **Total** | ~$70/month | Minimal cost |
| **One-time effort** | ~13 hours | 6h backend + 7h frontend |

---

## Architecture: POC v2 + Voice

```
┌────────────────────────────────────────────────────────┐
│ Vercel Frontend (Next.js)                              │
│  ├─ Mic input (Web Audio API)                         │
│  ├─ Send audio to backend                             │
│  ├─ Receive MP3 response + text                       │
│  ├─ Play audio (speaker output)                       │
│  └─ Display citations                                 │
└────────────────┬─────────────────────────────────────┘
                 │ REST API (fetch)
                 ↓
┌────────────────────────────────────────────────────────┐
│ Render Backend (FastAPI Python)                        │
│  ├─ /api/voice-ask (POST)                            │
│  │  ├─ Receive audio bytes                           │
│  │  ├─ STT: Whisper API (audio → text)               │
│  │  ├─ LLM: orchestrator.ask(text)                   │
│  │  ├─ TTS: Google Cloud TTS (text → audio)          │
│  │  └─ Return audio + citations                      │
│  └─ PostgreSQL + pgvector (existing index)           │
└────────────────────────────────────────────────────────┘
```

---

## Timeline: POC v2 + Voice

| Phase | Weeks | Work |
|---|---|---|
| **Current POC** | ✅ Done | searchEmployer Q&A (27/27 correct) |
| **POC v2: Voice** | 2 | Backend (STT+TTS) + Frontend (UI) |
| **Testing + Polish** | 1 | Demo-ready + bug fixes |
| **Go-live** | Week 3 | Full voice demo to stakeholders |
| **Then: Phase 1** | Week 4+ | Royal London (UAR/ISA), text+voice ready |

---

## Why This Matters

**Current situation:**
- "We built a chatbot that answers questions correctly (27/27)"
- Stakeholders think: "Cool. Is it production-ready?"

**With voice:**
- "We built a voice assistant that answers your questions by voice"
- Stakeholders think: "Wow. This is a real product. Let's scale it."

Voice demo = credibility multiplier. Same accuracy + retrieval, but 5x more impressive to see + hear working end-to-end.

---

## Decision: POC v2 or POC v2 + Voice?

**Recommendation: POC v2 + Voice**

**Why:**
- ✅ Only 2 additional weeks (minimal delay)
- ✅ Uses your existing Vercel + Render accounts (no new infra)
- ✅ Demonstrates end-to-end working system (not just text)
- ✅ 5x more impressive demo = easier Phase 1 buy-in
- ✅ Phase 4 (voice interface) already partly proven = Phase 1-3 can inherit voice scaffold
- ✅ Low cost (~$70/month for APIs)

**Go forward with:**
1. ✅ Finish current POC (searchEmployer, 27/27)
2. ✅ Add voice (2 weeks)
3. ✅ Demo to stakeholders (week 3)
4. ✅ Royal London Phase 1 kickoff (week 4)
5. ✅ By then, Phase 1 can launch with text + voice (demo proves both work)

---

## What You Need to Provide (New)

For POC v2 + Voice:
- [ ] Confirm Vercel account access (deploy frontend)
- [ ] Confirm Render account access (deploy backend)
- [ ] OpenAI API key (for Whisper — free tier) or budget $50/month for TTS
- [ ] Google Cloud TTS key or ElevenLabs API key (~$50/month budget)

**Or:**
- [ ] If you want to avoid APIs: use browser-based Web Speech API (free, works offline, lower quality)

---

## Final Call

**Do you want to:**
1. **A) Deploy POC v2 (text only) immediately**
   - Timeline: Ready now
   - Impact: "We built a chatbot"
   
2. **B) POC v2 + Voice (recommended)**
   - Timeline: +2 weeks
   - Impact: "We built a voice assistant" (10x more impressive)
   - Cost: ~$70/month
   - Uses: Your Vercel + Render accounts

**Which?**
