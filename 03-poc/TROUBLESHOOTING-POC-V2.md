# POC v2 Voice: Troubleshooting

## Common Issues

### 1. "Microphone access denied"

**Cause:** Browser blocked microphone permission.

**Fix:**
- Use Chrome or Edge (best Web Audio API support)
- Click the microphone icon in the address bar > Allow
- Or: Settings > Privacy > Site Settings > Microphone > Allow your Vercel URL
- Test: Open https://mictests.com to verify mic works

### 2. Backend returns 500 error

**Cause:** Missing environment variable or import error.

**Fix:**
- Check Render logs (Dashboard > sonata-voice-poc > Logs)
- Verify `OPENAI_API_KEY` is set in Render env vars
- Verify `ANTHROPIC_API_KEY` is set (existing POC key)
- Test health endpoint: `curl https://your-app.onrender.com/api/health`

### 3. Whisper returns empty transcription

**Cause:** Audio quality too low or too short.

**Fix:**
- Speak clearly for 2-3 seconds minimum
- Reduce background noise
- Try speaking closer to the microphone
- Check: Does mic work on other sites? (Google Meet, Zoom)

### 4. No audio playback (answer not spoken)

**Cause:** Web Speech API not working or audio muted.

**Fix:**
- Use Chrome (best TTS support)
- Click "Play Answer" button manually
- Check browser isn't muted (system volume)
- Check: Open chrome://settings/content/sounds

### 5. CORS error in browser console

**Cause:** Backend doesn't allow your frontend domain.

**Fix:**
- In `main.py`, the CORS middleware allows all origins (`"*"`)
- For production: change to `allow_origins=["https://sonata-voice-poc.vercel.app"]`
- Redeploy backend after change

### 6. "Failed to fetch" in browser console

**Cause:** Backend URL wrong or backend is sleeping.

**Fix:**
- Render free tier sleeps after 15 min inactivity
- First request wakes it up (takes ~30 sec)
- Check backend URL matches your Render deployment
- Test: `curl https://your-app.onrender.com/api/health`

### 7. Audio sounds robotic (Web Speech TTS)

**Cause:** Browser using default system voice.

**Fix:**
- This is expected for Web Speech API (free, built-in)
- For production: use ElevenLabs or Google Cloud TTS
- POC: robotic voice is fine — it proves the architecture works

### 8. Build fails on Render

**Cause:** Missing dependency or Python version mismatch.

**Fix:**
- Ensure `requirements.txt` has: fastapi, uvicorn, python-multipart, openai
- Set Python version in Render: Runtime > Python 3.11+
- Check build logs for specific error

## Testing Checklist

Before demo, verify:
- [ ] Microphone works (test on mictests.com)
- [ ] Backend health endpoint returns OK
- [ ] Text-only endpoint works (`/api/text-ask?q=test`)
- [ ] Voice recording works (click Ask, speak, see transcription)
- [ ] Answer appears with citations
- [ ] Audio plays back (click Play Answer)
- [ ] Works in Chrome (primary) and Edge (backup)

## Quick Diagnostic Commands

```bash
# Test backend health
curl https://your-app.onrender.com/api/health

# Test text endpoint
curl "https://your-app.onrender.com/api/text-ask?q=How does searchEmployer work?"

# Test voice endpoint with a sample audio file
curl -X POST https://your-app.onrender.com/api/voice-ask \
  -F "file=@test-audio.wav"
```

## Still Stuck?

1. Check Render logs for backend errors
2. Check browser console (F12 > Console) for frontend errors
3. Test text-only endpoint first (rules out audio issues)
4. Test locally before deploying (avoids network issues)
