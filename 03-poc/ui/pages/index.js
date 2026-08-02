import VoiceAssistant from '../components/VoiceAssistant';

export default function Home() {
  return (
    <>
      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.4; }
        }
        * { box-sizing: border-box; }
        body { margin: 0; }
      `}</style>
      <VoiceAssistant backendUrl="https://sonata-kb.onrender.com" />
    </>
  );
}
