import ChatPage from '../components/chat/ChatPage'

export default function Study() {
  return (
    <ChatPage
      title="Study"
      subtitle="Build a focused, sustainable study plan."
      placeholder="What are you studying and for when'"
      intro="Tell me your subject, deadline, and availability."
      useStream
      system="You are PUNTU, a study coach. Ask about timeline and availability, then propose a weekly plan with clear blocks."
    />
  )
}
