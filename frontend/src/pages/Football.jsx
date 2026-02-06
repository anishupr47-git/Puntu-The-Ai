import ChatPage from '../components/chat/ChatPage'

export default function Football() {
  return (
    <ChatPage
      title="Football"
      subtitle="Predict outcomes and likely scorelines."
      placeholder="Try: Arsenal vs Chelsea"
      intro="Give me a home and away team. I'll run a quick Poisson baseline."
      skill="football_predictor"
    />
  )
}
