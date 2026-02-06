import ChatPage from '../components/chat/ChatPage'

export default function Decision() {
  return (
    <ChatPage
      title="Decision"
      subtitle="Clear tradeoffs and a simple next step."
      placeholder="Describe the decision and options..."
      intro="Tell me the options and what matters most. I'll help you choose."
      useStream
      system="You are PUNTU, a decisive yet empathetic assistant. Ask 1-2 clarifying questions if needed, then give a clear recommendation with a short plan."
      storageKey="puntu:decision"
    />
  )
}
