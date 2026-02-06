import ChatPage from '../components/chat/ChatPage'

export default function Sleep() {
  return (
    <ChatPage
      title="Sleep"
      subtitle="Better sleep with a calmer schedule."
      placeholder="When do you want to wake up?"
      intro="Tell me your wake time and I will build a schedule."
      useStream
      system="You are PUNTU, a sleep coach. Ask about wake time and constraints, then suggest a bedtime, wind-down routine, and small habit tweaks."
      storageKey="puntu:sleep"
    />
  )
}
