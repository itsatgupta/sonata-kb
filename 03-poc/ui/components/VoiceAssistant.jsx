/**
 * POC v2: Sonata Knowledge Assistant — Voice + Text Chat
 *
 * A polished, production-ready UI with:
 * - Text chat input with mode selector (Direct / OpenAI / Claude)
 * - Voice input with real-time transcription display
 * - Web Speech TTS playback
 * - Citation display with source links
 * - Responsive, card-based layout
 */

import { useState, useRef, useCallback, useEffect } from 'react';

export default function VoiceAssistant({ backendUrl = '' }) {
  const [recording, setRecording] = useState(false);
  const [loading, setLoading] = useState(false);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [citations, setCitations] = useState(null);
  const [error, setError] = useState('');
  const [speaking, setSpeaking] = useState(false);
  const [textInput, setTextInput] = useState('');
  const [mode, setMode] = useState('openai');
  const [history, setHistory] = useState([]);
  const [modeInfo, setModeInfo] = useState('');

  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const synthRef = useRef(typeof window !== 'undefined' ? window.speechSynthesis : null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (inputRef.current) inputRef.current.focus();
  }, []);

  const modeDescriptions = {
    direct: 'Raw retrieval — free, instant, no AI synthesis',
    openai: 'GPT-3.5-turbo — fast, cheap (~$0.001), good quality',
    claude: 'Claude — best quality, ~$0.11 per query',
  };

  // ── Record audio ──────────────────────────────────
  const startRecording = useCallback(async () => {
    setError('');
    setModeInfo('Recording... speak now');
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
      setModeInfo('');
    }
  }, []);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
    setRecording(false);
    setModeInfo('Processing...');
  }, []);

  // ── Send audio to backend ─────────────────────────
  const sendToBackend = async (audioBlob) => {
    setLoading(true);
    setModeInfo('Thinking...');
    try {
      const formData = new FormData();
      formData.append('file', audioBlob, 'audio.webm');
      const url = `${backendUrl}/api/voice-ask`;
      const res = await fetch(url, { method: 'POST', body: formData });
      if (!res.ok) throw new Error(`Backend error: ${res.status}`);
      const data = await res.json();
      if (data.error) throw new Error(data.error);

      const entry = {
        question: data.question || '',
        answer: data.answer || '',
        citations: data.citations || [],
        mode: data.mode || 'voice',
        time: new Date().toLocaleTimeString(),
      };
      setHistory((prev) => [entry, ...prev]);
      setQuestion(entry.question);
      setAnswer(entry.answer);
      setCitations(entry.citations);
      setModeInfo('');
      if (entry.answer) speakAnswer(entry.answer);
    } catch (err) {
      setError(`Failed: ${err.message}`);
      setModeInfo('');
    } finally {
      setLoading(false);
    }
  };

  // ── Send text query ───────────────────────────────
  const sendText = async () => {
    if (!textInput.trim()) return;
    setError('');
    setLoading(true);
    setModeInfo('Thinking...');
    const q = textInput;
    setTextInput('');

    try {
      const modeParam = mode === 'direct' ? '&direct=true' : '';
      const url = `${backendUrl}/api/text-ask?q=${encodeURIComponent(q)}${modeParam}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error(`Backend error: ${res.status}`);
      const data = await res.json();
      if (data.error) throw new Error(data.error);

      const entry = {
        question: q,
        answer: data.answer || '',
        citations: data.citations || [],
        mode: data.mode || mode,
        time: new Date().toLocaleTimeString(),
      };
      setHistory((prev) => [entry, ...prev]);
      setQuestion(entry.question);
      setAnswer(entry.answer);
      setCitations(entry.citations);
      setModeInfo('');
    } catch (err) {
      setError(`Failed: ${err.message}`);
      setModeInfo('');
    } finally {
      setLoading(false);
    }
  };

  // ── TTS ───────────────────────────────────────────
  const speakAnswer = (text) => {
    if (!synthRef.current) return;
    synthRef.current.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;
    utterance.pitch = 1.0;
    utterance.lang = 'en-GB';
    const voices = synthRef.current.getVoices();
    const preferred = voices.find((v) => v.lang.startsWith('en') && v.name.includes('Google'))
      || voices.find((v) => v.lang.startsWith('en'));
    if (preferred) utterance.voice = preferred;
    utterance.onstart = () => setSpeaking(true);
    utterance.onend = () => setSpeaking(false);
    synthRef.current.speak(utterance);
  };

  const stopSpeaking = () => {
    if (synthRef.current) synthRef.current.cancel();
    setSpeaking(false);
  };

  // ── Format citation for display ───────────────────
  const formatCitation = (c) => {
    if (typeof c === 'string') return c;
    if (c.page) return `${c.page} — ${c.section || ''}`.trim();
    return JSON.stringify(c);
  };

  // ── Render ────────────────────────────────────────
  return (
    <div style={s.page}>
      {/* Header */}
      <div style={s.header}>
        <div style={s.headerInner}>
          <div style={s.logo}>
            <span style={s.logoIcon}>S</span>
            <div>
              <h1 style={s.title}>Sonata Knowledge Assistant</h1>
              <p style={s.subtitle}>Ask anything about Sonata functionality</p>
            </div>
          </div>
          <div style={s.badge}>POC v2</div>
        </div>
      </div>

      <div style={s.main}>
        {/* Input Card */}
        <div style={s.card}>
          {/* Chat Bot Section */}
          <div style={s.sectionHeader}>
            <span style={s.sectionIcon}>💬</span>
            <span style={s.sectionTitle}>Chat Bot</span>
            <span style={s.sectionSubtitle}>Type your question</span>
          </div>

          {/* Mode Selector */}
          <div style={s.modeBar}>
            <span style={s.modeLabel}>Mode:</span>
            {[
              { key: 'direct', label: 'Direct', tip: 'Raw retrieval — returns exact wiki chunks. Free, instant, no AI rewriting. Best for quick lookups.' },
              { key: 'openai', label: 'OpenAI', tip: 'GPT-3.5-turbo synthesizes a natural answer from retrieved chunks. Fast, ~$0.001/query, good quality.' },
              { key: 'claude', label: 'Claude', tip: 'Claude AI generates the best quality answer. More thorough but costs ~$0.11/query.' },
            ].map((m) => (
              <button
                key={m.key}
                onClick={() => { setMode(m.key); setModeInfo(''); }}
                title={m.tip}
                style={{
                  ...s.modeBtn,
                  ...(mode === m.key ? s.modeBtnActive : {}),
                }}
              >
                {m.label}
              </button>
            ))}
            <span style={s.modeHint}>{modeDescriptions[mode]}</span>
          </div>

          {/* Text Input */}
          <div style={s.inputRow}>
            <input
              ref={inputRef}
              type="text"
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !loading && sendText()}
              placeholder="Type your question..."
              disabled={loading}
              style={s.textInput}
            />
            <button
              onClick={sendText}
              disabled={loading || !textInput.trim()}
              style={{ ...s.btn, ...s.btnSend, ...(loading || !textInput.trim() ? s.btnDisabled : {}) }}
            >
              {loading ? '...' : 'Send'}
            </button>
          </div>

          {/* Voice Bot Section */}
          <div style={{ ...s.sectionHeader, marginTop: 18 }}>
            <span style={s.sectionIcon}>🎤</span>
            <span style={s.sectionTitle}>Voice Bot</span>
            <span style={s.sectionSubtitle}>Speak your question</span>
          </div>

          {/* Voice Button */}
          <div style={s.voiceRow}>
            <button
              onClick={recording ? stopRecording : startRecording}
              disabled={loading}
              title="Click to start recording. Speak your question clearly. Click Stop when done. Audio is transcribed via Whisper, answered, then spoken back."
              style={{
                ...s.btn,
                ...(recording ? s.btnMicActive : s.btnMic),
              }}
            >
              <span style={s.micDot(recording)} />
              {recording ? 'Stop Recording' : 'Start Voice'}
            </button>

            {answer && (
              <button
                onClick={speaking ? stopSpeaking : () => speakAnswer(answer)}
                title="Play the last answer again using browser text-to-speech (free, built-in)."
                style={{ ...s.btn, ...(speaking ? s.btnSpeakerActive : s.btnSpeaker) }}
              >
                {speaking ? 'Stop Audio' : '🔊 Play Answer'}
              </button>
            )}
          </div>

          {/* Status */}
          {(modeInfo || loading) && (
            <div style={s.statusBar}>
              <span style={s.spinner} />
              <span>{modeInfo || 'Thinking...'}</span>
            </div>
          )}
          {error && <div style={s.errorBar}>{error}</div>}
        </div>

        {/* Answer Card */}
        {answer && (
          <div style={s.answerCard}>
            <div style={s.answerHeader}>
              <span style={s.answerIcon}>A</span>
              <span style={s.answerLabel}>Answer</span>
              <span style={s.answerTime}>{history[0]?.time}</span>
            </div>
            <div style={s.answerBody}>
              <p style={s.answerText}>{answer}</p>
            </div>

            {citations && citations.length > 0 && (
              <div style={s.citationSection}>
                <span style={s.citationLabel}>Sources</span>
                <div style={s.citationList}>
                  {(Array.isArray(citations) ? citations : [citations]).map((c, i) => (
                    <span key={i} style={s.citationTag}>
                      {formatCitation(c)}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* History */}
        {history.length > 1 && (
          <div style={s.historyCard}>
            <span style={s.historyLabel}>Recent Queries</span>
            {history.slice(1, 6).map((h, i) => (
              <div
                key={i}
                style={s.historyItem}
                onClick={() => {
                  setQuestion(h.question);
                  setAnswer(h.answer);
                  setCitations(h.citations);
                }}
              >
                <span style={s.historyQ}>{h.question}</span>
                <span style={s.historyMeta}>{h.mode} · {h.time}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// ── Styles ──────────────────────────────────────────
const s = {
  page: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #f5f7fa 0%, #e4e9f2 100%)',
    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif',
  },
  header: {
    background: 'linear-gradient(135deg, #104281 0%, #1a5cc7 100%)',
    padding: '20px 24px',
    boxShadow: '0 2px 12px rgba(16,66,129,0.3)',
  },
  headerInner: {
    maxWidth: 720,
    margin: '0 auto',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  logo: { display: 'flex', alignItems: 'center', gap: 14 },
  logoIcon: {
    width: 42,
    height: 42,
    borderRadius: 10,
    background: 'rgba(255,255,255,0.15)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 20,
    fontWeight: 800,
    color: '#fff',
    letterSpacing: -1,
  },
  title: { fontSize: 20, fontWeight: 700, color: '#fff', margin: 0 },
  subtitle: { fontSize: 12, color: 'rgba(255,255,255,0.7)', margin: 0, marginTop: 2 },
  badge: {
    background: 'rgba(255,255,255,0.15)',
    color: '#fff',
    fontSize: 11,
    fontWeight: 600,
    padding: '4px 10px',
    borderRadius: 20,
    letterSpacing: 0.5,
  },
  main: { maxWidth: 720, margin: '0 auto', padding: '24px 16px' },

  // Cards
  card: {
    background: '#fff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 16,
    boxShadow: '0 1px 4px rgba(0,0,0,0.06)',
    border: '1px solid #e8eaed',
  },

  // Mode bar
  modeBar: { display: 'flex', alignItems: 'center', gap: 6, marginBottom: 14, flexWrap: 'wrap' },
  modeLabel: { fontSize: 12, fontWeight: 600, color: '#5f6368', marginRight: 4 },
  modeBtn: {
    padding: '5px 12px',
    border: '1px solid #dadce0',
    borderRadius: 16,
    fontSize: 12,
    fontWeight: 500,
    cursor: 'pointer',
    background: '#fff',
    color: '#5f6368',
    transition: 'all 0.15s',
  },
  modeBtnActive: {
    background: '#104281',
    color: '#fff',
    borderColor: '#104281',
  },
  modeHint: { fontSize: 11, color: '#9aa0a6', marginLeft: 8 },

  // Input
  inputRow: { display: 'flex', gap: 8, marginBottom: 10 },
  textInput: {
    flex: 1,
    padding: '11px 14px',
    border: '1px solid #dadce0',
    borderRadius: 8,
    fontSize: 14,
    outline: 'none',
    transition: 'border-color 0.15s',
    fontFamily: 'inherit',
  },

  // Voice
  voiceRow: { display: 'flex', gap: 8 },
  micDot: (active) => ({
    display: 'inline-block',
    width: 8,
    height: 8,
    borderRadius: '50%',
    background: active ? '#fff' : '#ea4335',
    marginRight: 6,
    animation: active ? 'pulse 1s infinite' : 'none',
  }),

  // Buttons
  btn: {
    padding: '10px 20px',
    border: 'none',
    borderRadius: 8,
    fontSize: 13,
    fontWeight: 600,
    cursor: 'pointer',
    transition: 'all 0.15s',
    display: 'flex',
    alignItems: 'center',
    gap: 4,
  },
  btnSend: { background: '#104281', color: '#fff' },
  btnMic: { background: '#ea4335', color: '#fff', flex: 1 },
  btnMicActive: { background: '#c5221f', color: '#fff', flex: 1, boxShadow: '0 0 0 3px rgba(234,67,53,0.3)' },
  btnSpeaker: { background: '#e8eaed', color: '#5f6368' },
  btnSpeakerActive: { background: '#1ba672', color: '#fff', boxShadow: '0 0 0 3px rgba(27,175,114,0.3)' },
  btnDisabled: { opacity: 0.5, cursor: 'not-allowed' },

  // Status
  statusBar: {
    display: 'flex',
    alignItems: 'center',
    gap: 8,
    marginTop: 12,
    padding: '8px 12px',
    background: '#f0f4ff',
    borderRadius: 6,
    fontSize: 12,
    color: '#104281',
  },
  spinner: {
    width: 14,
    height: 14,
    border: '2px solid #c8d6f0',
    borderTopColor: '#104281',
    borderRadius: '50%',
    animation: 'spin 0.8s linear infinite',
  },
  errorBar: {
    marginTop: 12,
    padding: '8px 12px',
    background: '#fef0f0',
    borderRadius: 6,
    fontSize: 12,
    color: '#c5221f',
    fontWeight: 500,
  },

  // Answer card
  answerCard: {
    background: '#fff',
    borderRadius: 12,
    marginBottom: 16,
    boxShadow: '0 1px 4px rgba(0,0,0,0.06)',
    border: '1px solid #e8eaed',
    overflow: 'hidden',
  },
  answerHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: 8,
    padding: '12px 20px',
    background: '#f8f9fa',
    borderBottom: '1px solid #e8eaed',
  },
  answerIcon: {
    width: 26,
    height: 26,
    borderRadius: 6,
    background: '#104281',
    color: '#fff',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 13,
    fontWeight: 700,
  },
  answerLabel: { fontSize: 13, fontWeight: 600, color: '#202124' },
  answerTime: { marginLeft: 'auto', fontSize: 11, color: '#9aa0a6' },
  answerBody: { padding: '16px 20px' },
  answerText: { fontSize: 14, color: '#202124', lineHeight: 1.7, margin: 0, whiteSpace: 'pre-wrap' },

  // Citations
  citationSection: {
    padding: '12px 20px',
    borderTop: '1px solid #e8eaed',
    background: '#f8f9fa',
  },
  citationLabel: { fontSize: 11, fontWeight: 600, color: '#5f6368', textTransform: 'uppercase', letterSpacing: 0.5 },
  citationList: { display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 8 },
  citationTag: {
    fontSize: 11,
    padding: '4px 10px',
    background: '#e8f0fe',
    color: '#104281',
    borderRadius: 12,
    fontWeight: 500,
  },

  // History
  historyCard: {
    background: '#fff',
    borderRadius: 12,
    padding: 16,
    boxShadow: '0 1px 4px rgba(0,0,0,0.06)',
    border: '1px solid #e8eaed',
  },
  historyLabel: { fontSize: 11, fontWeight: 600, color: '#9aa0a6', textTransform: 'uppercase', letterSpacing: 0.5 },
  historyItem: {
    padding: '10px 0',
    borderBottom: '1px solid #f1f3f4',
    cursor: 'pointer',
    transition: 'background 0.1s',
  },
  historyQ: { fontSize: 13, color: '#202124', fontWeight: 500, display: 'block' },
  historyMeta: { fontSize: 11, color: '#9aa0a6', marginTop: 2, display: 'block' },

  // Section headers
  sectionHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: 8,
    marginBottom: 12,
    paddingBottom: 8,
    borderBottom: '1px solid #f1f3f4',
  },
  sectionIcon: { fontSize: 16 },
  sectionTitle: { fontSize: 14, fontWeight: 700, color: '#202124' },
  sectionSubtitle: { fontSize: 11, color: '#9aa0a6' },
};
