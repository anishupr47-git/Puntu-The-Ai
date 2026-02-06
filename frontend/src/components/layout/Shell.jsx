import Background from './Background'
import Navbar from './Navbar'
import CompanionOrb from '../companion/CompanionOrb'

export default function Shell({ children }) {
  return (
    <div className="relative min-h-screen">
      <Background />
      <Navbar />
      <main className="mx-auto max-w-5xl px-6 py-10">
        {children}
      </main>
      <CompanionOrb />
    </div>
  )
}
