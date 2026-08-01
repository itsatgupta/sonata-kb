# POC v2 Voice: Deployment Guide

## Prerequisites

- OpenAI API key (for Whisper STT — free tier: 25K min/month)
- Vercel account (frontend hosting — free tier)
- Render account (backend hosting — free tier)
- Existing POC code (orchestrator.py + searchEmployer index)

## Step 1: Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy it (starts with `sk-...`)
4. Add to your environment:
   ```
   export OPENAI_API_KEY=sk-your-key-here
   ```

Free tier covers: 25,000 minutes/month of Whisper transcription.
POC usage: ~50 minutes/month (well within free tier).

## Step 2: Backend (Render)

### Files to deploy
```
03-poc/agent/
├── orchestrator.py          (existing POC)
├── orchestrator_voice.py    (NEW — voice integration)
├── main.py                  (NEW — FastAPI endpoint)
├── retrieval/               (existing POC)
├── tools/                   (existing POC)
├── config/                  (existing POC)
└── requirements.txt         (add: fastapi uvicorn python-multipart openai)
```

### Update requirements.txt
Add these lines:
```
fastapi>=0.100.0
uvicorn>=0.23.0
python-multipart>=0.0.6
openai>=1.0.0
```

### Deploy to Render
1. Go to https://dashboard.render.com
2. New > Web Service
3. Connect your GitHub repo
4. Settings:
   - Name: `sonata-voice-poc`
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - `OPENAI_API_KEY` = your key
   - `ANTHROPIC_API_KEY` = your Claude key (existing)
   - `CONFLUENCE_PAT` = your wiki PAT (existing)
   - `JIRA_PAT` = your Jira PAT (existing)
6. Deploy

Your backend URL will be: `https://sonata-voice-poc.onrender.com`

### Test backend
```bash
# Health check
curl https://sonata-voice-poc.onrender.com/api/health

# Text-only test (no audio needed)
curl "https://sonata-voice-poc.onrender.com/api/text-ask?q=How does searchEmployer work?"
```

## Step 3: Frontend (Vercel)

### Files to deploy
```
03-poc/ui/
├── components/
│   └── VoiceAssistant.jsx    (NEW — mic + Web Speech)
├── pages/
│   └── index.js              (render VoiceAssistant)
└── package.json
```

### Create pages/index.js
```jsx
import VoiceAssistant from '../components/VoiceAssistant';

export default function Home() {
  return (
    <main>
      <VoiceAssistant
        backendUrl="https://sonata-voice-poc.onrender.com"
      />
    </main>
  );
}
```

### Deploy to Vercel
1. Go to https://vercel.com/new
2. Import your GitHub repo
3. Framework: Next.js (auto-detected)
4. Deploy

Your frontend URL will be: `https://sonata-voice-poc.vercel.app`

### Test frontend
Open `https://sonata-voice-poc.vercel.app` in Chrome/Edge/Firefox.
Click "Ask a Question", speak, verify audio plays back.

## Step 4: Verify End-to-End

1. Open your Vercel URL
2. Click "Ask a Question"
3. Speak: "How does searchEmployer pagination work?"
4. Bot should:
   - Transcribe your speech (shows text on screen)
   - Answer with citation sources
   - Speak the answer back via browser audio
5. Check Render logs for any errors

## Troubleshooting

### "Microphone access denied"
- Use Chrome or Edge (best Web Audio API support)
- Allow microphone when browser prompts
- Check browser settings: Site Settings > Microphone

### "Backend error: 500"
- Check Render logs
- Ensure OPENAI_API_KEY is set in Render env vars
- Test /api/health endpoint

### "No audio playback"
- Web Speech API works best in Chrome
- Check browser audio isn't muted
- Try clicking "Play Answer" button manually

### "Whisper returned empty transcription"
- Speak clearly for 2-3 seconds minimum
- Check audio quality (no background noise)
- Try WAV format if WebM fails

## Cost Summary

| Service | Tier | Monthly Cost |
|---------|------|-------------|
| OpenAI Whisper | Free | $0 (25K min/month) |
| Web Speech API | Browser | $0 (unlimited) |
| Render | Free | $0 (750 dyno-hours) |
| Vercel | Free | $0 (100GB bandwidth) |
| **Total** | | **$0** |

## Next Steps After POC v2

Once voice demo is working:
1. Demo to stakeholders (45 min)
2. Get Phase 1 approval
3. Send data handoff template to Royal London
4. Begin 12-week Phase 1 execution
