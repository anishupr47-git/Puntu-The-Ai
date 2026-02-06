import ChatPage from '../components/chat/ChatPage'

export default function Songs() {
  return (
    <ChatPage
      title="Songs"
      subtitle="Tell me the vibe - I'll recommend or write."
      placeholder="Try: dreamy, neon night drive, 2010s synth..."
      intro="Describe the mood, energy, or genre. I'll match it."
      variants={[
        {
          label: 'Recommend',
          skill: 'song_recommender',
        },
        {
          label: 'Write lyrics',
          useStream: true,
          system: 'You are PUNTU, a songwriter. Write a short verse, pre-chorus, and chorus. Keep it original and vivid.',
        },
      ]}
    />
  )
}
