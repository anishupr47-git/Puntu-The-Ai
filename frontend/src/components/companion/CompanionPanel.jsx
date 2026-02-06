import { useMemo, useState } from 'react'
import { motion } from 'framer-motion'
import Button from '../ui/Button'
import Card from '../ui/Card'
import { agentRoute, streamLLM } from '../../lib/api'

const modes = ['Ask', 'Decide', 'Plan', 'Create']

export default function CompanionPanel({ onClose }) {
  const [mode, setMode] = useState('Ask')
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('')
  const [structured, setStructured] = useState(null)
  const [loading, setLoading] = useState(false)

  const placeholder = useMemo(() => {
    if (mode === 'Decide') return 'Describe the decision and options...'
    if (mode === 'Plan') return 'What do you want to plan?'
    if (mode === 'Create') return 'Describe the vibe or prompt...'
    return 'Ask anything...'
  }, [mode])

  const handleSend = async () => {
    if (!input.trim()) return
    setLoading(true)
    setOutput('')
    setStructured(null)

    try {
      if (mode === 'Ask' || mode === 'Create') {
        const system = mode === 'Create'
          ? 'You are a creative assistant. If the user wants lyrics, include verse, pre-chorus, and chorus.'
          : 'You are PUNTU, a playful, confident assistant. Be concise and actionable.'
        await streamLLM({
          prompt: input,
          system,
          onChunk: (chunk) => setOutput((prev) => prev + chunk),
        })
      } else {
        const response = await agentRoute({ message: input, mode: mode.toLowerCase() })
        setStructured(response.result)
        if (typeof response.result === 'string') setOutput(response.result)
      }
    } catch (err) {
      setOutput('Something went wrong. Check the backend logs.')
    } finally {
      setLoading(false)
    }
  }

  const renderStructured = () => {
    if (!structured) return null
    if (structured.recommendation) {
      return (
        <div className="space-y-3 text-sm text-glacier">
          <div className="text-base font-semibold text-white">Recommendation</div>
          <div>Choice: {structured.recommendation.choice}</div>
          <ul className="space-y-1">
            {structured.recommendation.why.map((item) => (
              <li key={item}>- {item}</li>
            ))}
          </ul>
          <div className="text-base font-semibold text-white">Plan</div>
          <ul className="space-y-1">
            {structured.plan.map((item) => (
              <li key={item}>- {item}</li>
            ))}
          </ul>
        </div>
      )
    }

    if (structured.clarifying_questions) {
      return (
        <div className="space-y-2 text-sm text-glacier">
          <div className="text-base font-semibold text-white">Clarifying questions</div>
          {structured.clarifying_questions.map((q) => (
            <div key={q}>- {q}</div>
          ))}
        </div>
      )
    }

    if (structured.plan) {
      return (
        <div className="space-y-2 text-sm text-glacier">
          <div className="text-base font-semibold text-white">Plan</div>
          {structured.plan.map((item) => (
            <div key={item.day}>- {item.day}: {item.focus}</div>
          ))}
        </div>
      )
    }

    return null
  }

  return (
    <motion.div
      className="fixed bottom-4 left-4 right-4 z-50 md:bottom-6 md:left-auto md:right-6 md:max-w-xl"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
    >
      <Card className="space-y-4 safe-bottom min-h-[420px]">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-xl font-semibold font-display">PUNTU</div>
            <div className="text-xs text-mist">Local AI, playful guidance</div>
          </div>
          <Button variant="ghost" onClick={onClose}>Close</Button>
        </div>
        <div className="flex flex-wrap gap-2">
          {modes.map((item) => (
            <button
              key={item}
              className={`rounded-full px-3 py-1 text-xs ${item === mode ? 'bg-white text-ink' : 'bg-white/10 text-glacier'}`}
              onClick={() => setMode(item)}
            >
              {item}
            </button>
          ))}
        </div>
        <textarea
          className="h-28 w-full resize-none rounded-2xl bg-white/5 p-3 text-sm text-glacier outline-none"
          placeholder={placeholder}
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <div className="flex flex-wrap justify-between gap-3">
          <Button variant="outline" onClick={() => setInput('')}>Clear</Button>
          <Button onClick={handleSend} disabled={loading}>
            {loading ? 'Thinking...' : 'Send'}
          </Button>
        </div>
        <div className="max-h-80 overflow-y-auto text-sm text-glacier scrollbar-hide">
          {renderStructured()}
          {output && <div className="whitespace-pre-wrap">{output}</div>}
        </div>
      </Card>
    </motion.div>
  )
}
