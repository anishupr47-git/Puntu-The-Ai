import ChatPage from '../components/chat/ChatPage'

export default function Hygiene() {
  return (
    <ChatPage
      title="Hygiene"
      subtitle="Simple routines that actually stick."
      placeholder="Tell me your skin type or goals..."
      intro="I can build a clean morning and night routine for you."
      useStream
      system="You are PUNTU, a hygiene and skincare assistant. Ask about skin type and constraints, then suggest a simple AM/PM routine."
    />
  )
}
