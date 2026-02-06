import ChatPage from '../components/chat/ChatPage'

export default function Food() {
  return (
    <ChatPage
      title="Food"
      subtitle="Balanced meals with steady energy."
      placeholder="Tell me your goal and any restrictions..."
      intro="I can map out a simple meal plan for your week."
      useStream
      system="You are PUNTU, a practical meal planner. Ask about goals, budget, and restrictions, then propose a simple day or week plan."
      storageKey="puntu:food"
    />
  )
}
