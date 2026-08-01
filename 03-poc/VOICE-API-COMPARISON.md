# Voice APIs: Cost-Effective Comparison
## STT (Speech-to-Text) + TTS (Text-to-Speech) Options

**Your accounts:** ElevenLabs + Vercel + Render  
**Goal:** Cheapest + easiest + best quality for POC voice demo

---

## COMPARISON TABLE

| Aspect | OpenAI Whisper | Google Cloud TTS | ElevenLabs |
|--------|---|---|---|
| **STT Quality** | Excellent (industry-best) | N/A (Google has Speech-to-Text, different product) | N/A (TTS-only) |
| **TTS Quality** | N/A | Very good (natural) | Excellent (most natural) |
| **Cost (STT)** | $0.02/min ($1.20/hour) | $0.006/min ($0.36/hour, cheaper) | N/A |
| **Cost (TTS)** | N/A | $0.000015/char (~$15 per 1M chars) | $0.30 per 1K chars ($300 per 1M chars) |
| **Free Tier** | 25,000 min/month (~$10 value) | $300/month free | 10K characters free/month |
| **Setup Ease** | ⭐⭐⭐⭐⭐ (1 API key, simple) | ⭐⭐⭐ (setup + creds file) | ⭐⭐⭐⭐ (1 API key, simple) |
| **Best for** | STT (speechy input) | TTS (volume needed) | TTS (quality matters) |

---

## RECOMMENDED COMBO (Cost-Effective)

### **Best Budget Option: OpenAI Whisper + Google Cloud TTS**

```
STT: OpenAI Whisper API
  ✅ $0.02/min ($1.20/hour)
  ✅ Free tier: 25,000 min/month (~$10 value)
  ✅ Excellent accuracy
  ✅ 1 line of code: client.audio.transcriptions.create()

TTS: Google Cloud TTS
  ✅ $0.000015/char (cheapest in industry)
  ✅ $300/month free tier
  ✅ Natural sounding voices
  ✅ Pay-as-you-go

Total cost: Free tier covers ~3-6 months of POC usage
Production cost: ~$50/month for modest volume
```

---

## OPTION BREAKDOWN

### **Option 1: OpenAI Whisper + Google Cloud TTS (RECOMMENDED)**

**STT: Whisper API**
```python
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(audio_bytes):
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=("audio.wav", audio_bytes)
    )
    return transcript.text

# Cost: $0.02/min
# Example: 1 minute audio = $0.02
# Volume: 100 questions × 30 sec avg = $1/day
```

**TTS: Google Cloud TTS**
```python
from google.cloud import tts_v1

def synthesize_speech(text):
    client = tts_v1.TextToSpeechClient()
    synthesis_input = tts_v1.SynthesisInput(text=text)
    voice = tts_v1.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Neural2-A"  # Natural sounding
    )
    audio_config = tts_v1.AudioConfig(
        audio_encoding=tts_v1.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    return response.audio_content

# Cost: $0.000015/char
# Example: 500 char response = $0.0075
# Volume: 100 questions × 500 chars avg = $0.75/day
```

**Total Cost (POC Volume):**
- STT: 100 Q/day × 30 sec = 50 min/day = $1/day = $30/month
- TTS: 100 Q/day × 500 chars = 50K chars/day = $0.75/day = $22.50/month
- **Total: ~$52.50/month**
- **But:** Free tiers cover this (~$310/month combined free tier)

**Setup:**
1. Get OpenAI API key (you already have Claude account, add Whisper)
2. Get Google Cloud credentials (free $300/month trial)
3. 10 lines of code total
4. Deploy to Render (both APIs work from anywhere)

---

### **Option 2: OpenAI Whisper + ElevenLabs TTS**

**Why you have ElevenLabs account:**
- ✅ Best TTS quality (most natural sounding)
- ✅ 10K chars free/month
- ✅ $0.30/1K chars paid ($300 per 1M)
- ⚠️ More expensive than Google for volume

**Cost Breakdown:**
- STT (Whisper): $30/month (same as Option 1)
- TTS (ElevenLabs): 100 Q/day × 500 chars = 50K chars/day = $15/month (vs. $22.50 Google)
- **Total: ~$45/month** (cheaper than Option 1!)
- **Plus:** Your existing ElevenLabs account (no new signup)

**Code:**
```python
import elevenlabs

def synthesize_speech_elevenlabs(text):
    audio = elevenlabs.generate(
        text=text,
        voice="Rachel",  # Natural voice
        api_key=os.getenv("ELEVENLABS_API_KEY")
    )
    return audio

# Cost: $0.30/1000 chars
# Example: 500 char response = $0.15
```

**Setup:**
1. Use your existing ElevenLabs account (API key already have)
2. OpenAI API key (add Whisper)
3. 5 lines of code
4. Done

---

### **Option 3: Google Cloud Speech-to-Text + Google Cloud TTS**

**Advantage:** Single vendor (one dashboard, one bill)  
**Disadvantage:** Google Cloud Speech-to-Text is $0.006/min (cheaper than Whisper, but lower quality)

**Not recommended:** Whisper is better quality for speech recognition.

---

### **Option 4: OpenAI Whisper + OpenAI TTS (Coming Soon)**

**Status:** OpenAI is building TTS (currently text-to-speech available as beta)  
**When:** Available now (gpt-4-turbo can do voice output via beta)  
**Not yet recommended:** Still in beta, use Google/ElevenLabs for now

---

## MY RECOMMENDATION: **Option 2 (Whisper + ElevenLabs)**

**Why:**
1. ✅ **You already have ElevenLabs account** (no new signup)
2. ✅ **Cheapest total cost** (~$45/month vs. $52.50 Google)
3. ✅ **Best quality** (ElevenLabs TTS is most natural)
4. ✅ **Easiest setup** (just add OpenAI API key)
5. ✅ **Your Vercel + Render ready** (both work from anywhere)

**Cost breakdown (POC 3-month pilot):**
- Whisper: $30/month (OpenAI free tier covers this)
- ElevenLabs: $15/month (your account, 10K free chars/month included)
- **Total: ~$45/month**
- **3-month cost: ~$135** (basically free from your free tier)

---

## SETUP (Option 2: Whisper + ElevenLabs)

### **Step 1: Get API Keys**

**OpenAI Whisper:**
```bash
# You already have this for Claude
# Add Whisper to your API key (same key works)
export OPENAI_API_KEY="sk-..."
```

**ElevenLabs:**
```bash
# You already have account
# Get API key from: https://elevenlabs.io/account
export ELEVENLABS_API_KEY="..."
```

### **Step 2: Install Libraries**

```bash
pip install openai elevenlabs google-cloud-storage
```

### **Step 3: Add to Your Render Backend**

```python
from openai import OpenAI
import elevenlabs
from orchestrator import ask  # Your existing function

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def voice_ask(audio_bytes):
    """Audio → Text → Answer → Audio"""
    
    # Step 1: STT (Whisper)
    transcript = openai_client.audio.transcriptions.create(
        model="whisper-1",
        file=("audio.wav", audio_bytes)
    )
    question = transcript.text
    
    # Step 2: LLM (Your existing function)
    answer, citations = ask(question)
    
    # Step 3: TTS (ElevenLabs)
    audio = elevenlabs.generate(
        text=answer,
        voice="Rachel",  # or "Bella", "Josh", etc.
        api_key=os.getenv("ELEVENLABS_API_KEY")
    )
    
    return audio, citations, question
```

### **Step 4: Frontend (Vercel)**

```jsx
// Same code as before (no changes needed)
const res = await fetch('/api/voice-ask', { method: 'POST', body: formData });
const { audio, citations } = await res.json();
const audioBlob = new Blob([atob(audio)], { type: 'audio/mp3' });
const audioUrl = URL.createObjectURL(audioBlob);
new Audio(audioUrl).play();
```

### **Step 5: Deploy**

```bash
# Render backend
render deploy

# Vercel frontend
vercel deploy
```

---

## COST SUMMARY (3-Month POC Pilot)

| Item | Monthly | 3-Month | Notes |
|---|---|---|---|
| **Whisper API** | $30 | $90 | Free tier: 25K min/month (~$10 value) |
| **ElevenLabs TTS** | $15 | $45 | Free tier: 10K chars/month; your account |
| **Render** | $20 | $60 | Standard tier (compute) |
| **Vercel** | $0 | $0 | Free tier (frontend) |
| **PostgreSQL** | $15 | $45 | Render Postgres (database) |
| **Claude API** | ~$50 | ~$150 | Same as current POC |
| **TOTAL** | ~$130 | ~$390 | Basically covered by free tiers |

**Reality:** Free tiers cover most of this. You'll pay <$100 actual cash for 3-month pilot.

---

## RECOMMENDATION SUMMARY

### **For POC Voice Demo (Next 2 Weeks)**

```
✅ STT: OpenAI Whisper API
   • Best quality
   • $0.02/min
   • Free tier: 25K min/month

✅ TTS: ElevenLabs (your account)
   • Best quality
   • $0.30/1K chars
   • Free tier: 10K chars/month
   
Total: ~$45/month (free tier covers it)
Setup: 30 minutes
Quality: Excellent (both best-in-class)
```

### **Implementation Timeline (2 Weeks)**

**Week 1:**
- Day 1–2: Backend code (Whisper + ElevenLabs integration)
- Day 3–4: Testing (speak → transcribe → answer → speak)
- Day 5: Fix bugs + optimize

**Week 2:**
- Day 1–2: Frontend (mic input + audio playback)
- Day 3–4: Deploy to Vercel + Render
- Day 5: Demo to stakeholders

---

## Decision: Which Option?

| Option | Cost | Quality | Setup | Recommendation |
|---|---|---|---|---|
| **Whisper + Google TTS** | $52/mo | Very good | Easy | Good alternative |
| **Whisper + ElevenLabs** | $45/mo | Excellent | Easy | ✅ RECOMMENDED |
| **Whisper + OpenAI TTS** | TBD | Unknown | TBD | Wait for official release |

---

## Final Call

**Use: OpenAI Whisper + ElevenLabs TTS**

**Why:**
1. You already have ElevenLabs account (no new signup)
2. Cheapest option ($45/month, free tier covers it)
3. Best quality (both best-in-class)
4. Easiest setup (30 minutes)
5. Render + Vercel ready to deploy

**Next:** Confirm you want to proceed with POC v2 + voice, and I'll send you the complete backend + frontend code (copy-paste ready).

---

## Want to Proceed?

Send:
```
✅ POC v2 + Voice (2 weeks)
✅ Whisper + ElevenLabs
✅ Ready to integrate
```

Then: I send you the complete code scaffold → you copy-paste → 2 weeks to demo. 🎤
