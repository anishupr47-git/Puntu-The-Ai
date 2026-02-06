import ChatPage from '../components/chat/ChatPage'

export default function Movies() {
  return (
    <ChatPage
      title="Movies"
      subtitle="Describe the mood and I will find a match."
      placeholder="Try: moody noir, 2020s mystery, cozy drama..."
      intro="Tell me what you feel like watching and I will suggest options."
      skill="movie_suggester"
      storageKey="puntu:movies"
    />
  )
}
