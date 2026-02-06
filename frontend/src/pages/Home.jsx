import ChatPage from '../components/chat/ChatPage'

export default function Home() {
  return (
    <ChatPage
      title="PUNTU"
      subtitle="Your Playful Companion"
      placeholder="Ask anything..."
      intro="Hey, I'm PUNTU. What do you want to explore today?"
      useStream
      system="You are PUNTU, a playful, confident assistant. Keep it clear, helpful, and upbeat."
    />
  )
}
