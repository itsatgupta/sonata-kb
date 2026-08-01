import VoiceAssistant from '../components/VoiceAssistant';

export default function Home() {
  return (
    <main style={{ minHeight: '100vh', background: '#FCFCFB' }}>
      <VoiceAssistant
        backendUrl="https://sonata-kb.onrender.com"
      />
    </main>
  );
}
