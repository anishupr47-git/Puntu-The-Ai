import ChatPage from '../components/chat/ChatPage'

export default function Fitness() {
  return (
    <ChatPage
      title="Fitness"
      subtitle="Strength, stamina, and recovery."
      placeholder="What’s your goal and current training level'"
      intro="I’ll build a plan based on your schedule and goal."
      useStream
      system="You are PUNTU, a fitness coach. Ask about goal, experience, and time, then propose a balanced weekly plan."
    />
  )
}
