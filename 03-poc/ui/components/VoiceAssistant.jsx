/**
 * POC v2: Voice Assistant Component for Sonata Knowledge Assistant.
 *
 * Features:
 * - Mic input (Web Audio API)
 * - Send audio to Render backend -> Whisper STT -> orchestrator -> answer
 * - Play answer via Web Speech API (100% free, browser built-in)
 * - Show citations below
 *
 * Usage:
 *   import VoiceAssistant from './components/VoiceAssistant';
 *   <VoiceAssistant backendUrl="https://sonata-kb.onrender.com" />
 *
 * Deploy frontend to Vercel (free tier).
 */

import { useState, useRef, useCallback } from 'react';

export default function VoiceAssistant({ backendUrl = '' }) {
  const [recording, setRecording] = useState(false);
  const [loading, setLoading] = useState(false);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [citations, setCitations] = useState(null);
  const [error, setError] = useState('');
  const [speaking, setSpeaking] = useState(false);
  const [textInput, setTextInput] = useState('');
  const [mode, setMode] = useState('openai'); // 'direct' | 'openai' | 'claude'

  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const synthRef = useRef(typeof window !== 'undefined' ? window.speechSynthesis : null);

  // ── Record audio ──────────────────────────────────
  const startRecording = useCallback(async () => {
    setError('');
    setQuestion('');
    setAnswer('');
    setCitations(null);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      mediaRecorder.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop());
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
        await sendToBackend(audioBlob);
      };

      mediaRecorder.start();
      setRecording(true);
    } catch (err) {
      setError('Microphone access denied. Please allow microphone and try again.');
    }
  }, []);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
    setRecording(false);
  }, []);

  // ── Send to backend ───────────────────────────────
  const sendToBackend = async (audioBlob) => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', audioBlob, 'audio.webm');

      const url = `${backendUrl}/api/voice-ask`;
      const res = await fetch(url, { method: 'POST', body: formData });

      if (!res.ok) throw new Error(`Backend error: ${res.status}`);

      const data = await res.json();
      if (data.error) throw new Error(data.error);

      setQuestion(data.question || '');
      setAnswer(data.answer || '');
      setCitations(data.citations || []);

      // Auto-speak the answer
      if (data.answer) speakAnswer(data.answer);
    } catch (err) {
      setError(`Failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // ── Text chat (typing) ────────────────────────────
  const sendText = async () => {
    if (!textInput.trim()) return;
    setError('');
    setLoading(true);
    setQuestion(textInput);
    setAnswer('');
    setCitations(null);

    try {
      const modeParam = mode === 'direct' ? '&direct=true' : '';
      const url = `${backendUrl}/api/text-ask?q=${encodeURIComponent(textInput)}${modeParam}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error(`Backend error: ${res.status}`);
      const data = await res.json();
      if (data.error) throw new Error(data.error);

      setAnswer(data.answer || '');
      setCitations(data.citations || []);
      setTextInput('');
    } catch (err) {
      setError(`Failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // ── TTS via Web Speech API (100% free) ────────────
  const speakAnswer = (text) => {
    if (!synthRef.current) return;
    synthRef.current.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;
    utterance.pitch = 1.0;
    utterance.lang = 'en-GB';

    // Prefer a natural voice if available
    const voices = synthRef.current.getVoices();
    const preferred = voices.find(
      (v) => v.lang.startsWith('en') && v.name.includes('Google')
    ) || voices.find((v) => v.lang.startsWith('en'));
    if (preferred) utterance.voice = preferred;

    utterance.onstart = () => setSpeaking(true);
    utterance.onend = () => setSpeaking(false);

    synthRef.current.speak(utterance);
  };

  const stopSpeaking = () => {
    if (synthRef.current) synthRef.current.cancel();
    setSpeaking(false);
  };

  // ── Render ────────────────────────────────────────
  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2 style={styles.title}>Sonata Voice Assistant</h2>
        <p style={styles.subtitle}>Ask a question about Sonata functionality</p>
      </div>

      {/* Text Input */}
      <div style={styles.textInputRow}>
        <input
          type="text"
          value={textInput}
          onChange={(e) => setTextInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendText()}
          placeholder="Type your question here..."
          disabled={loading}
          style={styles.textInput}
        />
        <button
          onClick={sendText}
          disabled={loading || !textInput.trim()}
          style={{ ...styles.btn, ...styles.btnPrimary }}
        >
          Send
        </button>
      </div>

      {/* Mode Toggle */}
      <div style={styles.modeToggle}>
        <span style={styles.toggleLabel}>Mode:</span>
        <button
          onClick={() => setMode('direct')}
          style={{ ...styles.modeBtn, ...(mode === 'direct' ? styles.modeBtnActive : {}) }}
        >
          Direct ($0)
        </button>
        <button
          onClick={() => setMode('openai')}
          style={{ ...styles.modeBtn, ...(mode === 'openai' ? styles.modeBtnActive : {}) }}
        >
          OpenAI (~$0.001)
        </button>
        <button
          onClick={() => setMode('claude')}
          style={{ ...styles.modeBtn, ...(mode === 'claude' ? styles.modeBtnActive : {}) }}
        >
          Claude (~$0.11)
        </button>
      </div>

      <p style={styles.divider}>— or use voice —</p>

      {/* Voice Controls */}
      <div style={styles.controls}>
        <button
          onClick={recording ? stopRecording : startRecording}
          disabled={loading}
          style={{
            ...styles.btn,
            ...(recording ? styles.btnRecording : styles.btnPrimary),
          }}
        >
          {recording ? 'Stop Recording' : 'Ask a Question'}
        </button>

        {answer && (
          <button
            onClick={speaking ? stopSpeaking : () => speakAnswer(answer)}
            style={{ ...styles.btn, ...(speaking ? styles.btnSpeaking : styles.btnSecondary) }}
          >
            {speaking ? 'Stop Audio' : 'Play Answer'}
          </button>
        )}
      </div>

      {/* Status */}
      {recording && <p style={styles.status}>Recording... speak now</p>}
      {loading && <p style={styles.status}>Thinking...</p>}
      {error && <p style={styles.error}>{error}</p>}

      {/* Results */}
      {question && (
        <div style={styles.result}>
          <div style={styles.resultSection}>
            <h3 style={styles.resultLabel}>Your question:</h3>
            <p style={styles.questionText}>{question}</p>
          </div>

          <div style={styles.resultSection}>
            <h3 style={styles.resultLabel}>Answer:</h3>
            <p style={styles.answerText}>{answer}</p>
          </div>

          {citations && citations.length > 0 && (
            <div style={styles.resultSection}>
              <h3 style={styles.resultLabel}>Sources:</h3>
              <ul style={styles.citationList}>
                {(Array.isArray(citations) ? citations : [citations]).map((c, i) => (
                  <li key={i} style={styles.citationItem}>
                    {typeof c === 'string' ? c : JSON.stringify(c)}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ── Styles ──────────────────────────────────────────
const styles = {
  container: {
    maxWidth: 640,
    margin: '0 auto',
    padding: '24px 20px',
    fontFamily: 'Calibri, Segoe UI, sans-serif',
    color: '#0B0B0B',
  },
  header: { marginBottom: 24 },
  title: { fontSize: 28, fontWeight: 700, color: '#104281', margin: 0 },
  subtitle: { fontSize: 14, color: '#52514E', marginTop: 4 },
  controls: { display: 'flex', gap: 12, marginBottom: 16 },
  btn: {
    padding: '12px 24px',
    border: 'none',
    borderRadius: 6,
    fontSize: 14,
    fontWeight: 600,
    cursor: 'pointer',
    transition: 'background 0.15s',
  },
  btnPrimary: { background: '#104281', color: '#fff' },
  btnRecording: { background: '#CC0000', color: '#fff' },
  btnSecondary: { background: '#E1E0D9', color: '#0B0B0B' },
  btnSpeaking: { background: '#1BAF7A', color: '#fff' },
  status: { fontSize: 13, color: '#52514E', fontStyle: 'italic' },
  error: { fontSize: 13, color: '#CC0000', fontWeight: 600 },
  result: {
    marginTop: 20,
    padding: 20,
    background: '#F2F3F5',
    borderRadius: 8,
  },
  resultSection: { marginBottom: 16 },
  resultLabel: { fontSize: 12, fontWeight: 700, color: '#104281', marginBottom: 4, textTransform: 'uppercase' },
  questionText: { fontSize: 14, color: '#0B0B0B' },
  answerText: { fontSize: 14, color: '#0B0B0B', lineHeight: 1.6 },
  citationList: { margin: 0, paddingLeft: 20 },
  citationItem: { fontSize: 12, color: '#52514E', marginBottom: 4 },
  modeToggle: { display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 },
  modeLabel: { fontSize: 12, fontWeight: 600, color: '#52514E' },
  modeBtn: {
    padding: '6px 12px',
    border: '1px solid #E1E0D9',
    borderRadius: 4,
    fontSize: 11,
    cursor: 'pointer',
    background: '#fff',
    color: '#52514E',
  },
  modeBtnActive: {
    background: '#104281',
    color: '#fff',
    borderColor: '#104281',
  },
};
