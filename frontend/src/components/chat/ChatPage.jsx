import { useEffect, useMemo, useRef, useState } from 'react'
import { agentRoute, analyzeImage, streamLLM } from '../../lib/api'
import Button from '../ui/Button'
import Card from '../ui/Card'

function normalizeResult(result) {
  if (typeof result === 'string') {
    return { kind: 'text', content: result }
  }
  if (Array.isArray(result)) {
    if (result.length && result[0].artist) {
      return { kind: 'songs', items: result }
    }
    if (result.length && result[0].year) {
      return { kind: 'movies', items: result }
    }
    return { kind: 'list', items: result }
  }
  if (result?.outcome_probabilities) {
    return { kind: 'football', data: result }
  }
  if (
    result?.recommendation ||
    result?.clarifying_questions ||
    result?.plan ||
    result?.schedule ||
    result?.morning ||
    result?.breakfast
  ) {
    return { kind: 'structured', data: result }
  }
  return { kind: 'text', content: JSON.stringify(result, null, 2) }
}

function MessageBubble({ role, children }) {
  const isUser = role === 'user'
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[85%] rounded-3xl px-5 py-4 text-base ${
          isUser
            ? 'bg-gradient-to-br from-accent/80 to-accent2/80 text-ink shadow-xl'
            : 'bg-white/10 text-white'
        }`}
      >
        {children}
      </div>
    </div>
  )
}

function StructuredBlock({ data }) {
  return (
    <div className="space-y-3 text-sm text-glacier">
      {data.clarifying_questions && (
        <div className="space-y-2">
          <div className="text-white font-semibold">Clarifying questions</div>
          {data.clarifying_questions.map((q) => (
            <div key={q}>- {q}</div>
          ))}
        </div>
      )}

      {data.recommendation && (
        <div className="space-y-2">
          <div className="text-white font-semibold">Recommendation</div>
          <div>Choice: {data.recommendation.choice}</div>
          {data.recommendation.why && (
            <div>
              {data.recommendation.why.map((item) => (
                <div key={item}>- {item}</div>
              ))}
            </div>
          )}
          {data.recommendation.tradeoffs && (
            <div>
              {data.recommendation.tradeoffs.map((item) => (
                <div key={item}>- {item}</div>
              ))}
            </div>
          )}
        </div>
      )}

      {data.plan && (
        <div className="space-y-2">
          <div className="text-white font-semibold">Plan</div>
          {data.plan.map((item) => (
            <div key={item.day || item}>- {item.day ? `${item.day}: ${item.focus}` : item}</div>
          ))}
        </div>
      )}

      {data.schedule && (
        <div className="space-y-2">
          <div className="text-white font-semibold">Schedule</div>
          {data.schedule.map((item) => (
            <div key={item.day}>- {item.day}: {item.focus} ({item.duration_min} min)</div>
          ))}
        </div>
      )}

      {data.tips && (
        <div className="space-y-1">
          <div className="text-white font-semibold">Tips</div>
          {data.tips.map((item) => (
            <div key={item}>- {item}</div>
          ))}
        </div>
      )}

      {(data.morning || data.night) && (
        <div className="space-y-2">
          <div className="text-white font-semibold">Routine</div>
          {data.morning && (
            <div>
              <div className="text-white/80">Morning</div>
              {data.morning.map((item) => (
                <div key={item}>- {item}</div>
              ))}
            </div>
          )}
          {data.night && (
            <div>
              <div className="text-white/80">Night</div>
              {data.night.map((item) => (
                <div key={item}>- {item}</div>
              ))}
            </div>
          )}
        </div>
      )}

      {data.breakfast && (
        <div className="space-y-1">
          <div className="text-white font-semibold">Meal plan</div>
          <div>Breakfast: {data.breakfast}</div>
          <div>Lunch: {data.lunch}</div>
          <div>Dinner: {data.dinner}</div>
          {data.snacks && data.snacks.map((item) => (
            <div key={item}>- {item}</div>
          ))}
        </div>
      )}

      {(data.target_bed_time || data.target_wake_time) && (
        <div className="space-y-1">
          <div className="text-white font-semibold">Sleep targets</div>
          <div>Wake: {data.target_wake_time}</div>
          <div>Bed: {data.target_bed_time}</div>
          {data.wind_down && data.wind_down.map((item) => (
            <div key={item}>- {item}</div>
          ))}
        </div>
      )}
    </div>
  )
}

function SongList({ items }) {
  return (
    <div className="space-y-3">
      {items.map((song) => (
        <div key={song.id} className="rounded-2xl bg-white/10 p-3">
          <div className="font-semibold text-white">{song.title}</div>
          <div className="text-xs text-mist">{song.artist}</div>
          <div className="mt-1 text-xs text-glacier">{song.genre} ? {song.mood} ? {song.era}</div>
          <div className="mt-2 flex flex-wrap gap-2">
            {song.tags.map((tag) => (
              <span key={tag} className="rounded-full bg-white/10 px-2 py-1 text-[10px]">{tag}</span>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

function MovieList({ items }) {
  return (
    <div className="space-y-3">
      {items.map((movie) => (
        <div key={movie.id} className="rounded-2xl bg-white/10 p-3">
          <div className="font-semibold text-white">{movie.title}</div>
          <div className="text-xs text-mist">{movie.year} ? {movie.genre}</div>
          <div className="mt-1 text-xs text-glacier">{movie.mood} ? {movie.era}</div>
          <div className="mt-2 text-sm text-glacier">{movie.synopsis}</div>
        </div>
      ))}
    </div>
  )
}

function FootballResult({ data }) {
  return (
    <div className="space-y-2 text-sm text-glacier">
      {data.guardrail && <div>{data.guardrail}</div>}
      {data.outcome_probabilities && (
        <div>
          W/D/L: {data.outcome_probabilities.home_win} / {data.outcome_probabilities.draw} / {data.outcome_probabilities.away_win}
        </div>
      )}
      {data.top_scorelines && (
        <div className="space-y-1">
          <div className="text-white font-semibold">Top scorelines</div>
          {data.top_scorelines.map((s) => (
            <div key={s.score}>- {s.score} ({s.probability})</div>
          ))}
        </div>
      )}
    </div>
  )
}

function ImageBubble({ src, caption }) {
  return (
    <div className="space-y-2">
      <img src={src} alt="User upload" className="max-h-48 rounded-2xl object-cover" />
      {caption && <div className="text-sm">{caption}</div>}
    </div>
  )
}

export default function ChatPage({
  title,
  subtitle,
  placeholder,
  intro,
  skill,
  mode,
  system,
  useStream = false,
  variants,
}) {
  const [messages, setMessages] = useState(
    intro ? [{ role: 'assistant', kind: 'text', content: intro }] : []
  )
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [activeVariant, setActiveVariant] = useState(variants?.[0] || null)
  const [imageFile, setImageFile] = useState(null)
  const [imagePreview, setImagePreview] = useState('')
  const endRef = useRef(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const active = useMemo(() => {
    if (activeVariant) return activeVariant
    return { skill, mode, system, useStream }
  }, [activeVariant, skill, mode, system, useStream])

  const handleSend = async () => {
    if (!input.trim() && !imageFile) return
    setLoading(true)

    if (imageFile && imagePreview) {
      setMessages((prev) => [
        ...prev,
        { role: 'user', kind: 'image', content: imagePreview, caption: input.trim() },
      ])
    } else if (input.trim()) {
      setMessages((prev) => [...prev, { role: 'user', kind: 'text', content: input }])
    }

    try {
      if (imageFile) {
        const response = await analyzeImage({
          file: imageFile,
          prompt: input.trim() || 'Describe and summarize this image.',
        })
        setMessages((prev) => [
          ...prev,
          { role: 'assistant', kind: 'text', content: response.summary || '' },
        ])
      } else if (active.useStream) {
        let assistantIndex = null
        setMessages((prev) => {
          assistantIndex = prev.length
          return [...prev, { role: 'assistant', kind: 'text', content: '' }]
        })
        await streamLLM({
          prompt: input,
          system: active.system,
          onChunk: (chunk) => {
            setMessages((prev) => {
              const next = [...prev]
              const current = next[assistantIndex]
              next[assistantIndex] = {
                ...current,
                content: (current?.content || '') + chunk,
              }
              return next
            })
          },
        })
      } else {
        const response = await agentRoute({
          message: input,
          skill: active.skill,
          mode: active.mode,
        })
        const normalized = normalizeResult(response.result)
        setMessages((prev) => [...prev, { role: 'assistant', ...normalized }])
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', kind: 'text', content: 'Something went wrong. Check backend logs.' },
      ])
    } finally {
      setLoading(false)
      setInput('')
      setImageFile(null)
      setImagePreview('')
    }
  }

  const handleImageChange = (event) => {
    const file = event.target.files?.[0]
    if (!file) return
    setImageFile(file)
    const reader = new FileReader()
    reader.onload = () => {
      setImagePreview(reader.result ? String(reader.result) : '')
    }
    reader.readAsDataURL(file)
  }

  return (
    <div className="space-y-6">
      <div>
        <div className="text-3xl font-semibold font-display">{title}</div>
        <div className="text-mist">{subtitle}</div>
      </div>
      <Card className="p-0 overflow-hidden">
        <div className="flex flex-col min-h-[70vh]">
          <div className="flex-1 space-y-5 overflow-y-auto p-6">
            {messages.length === 0 && (
              <div className="text-mist">Start the conversation below.</div>
            )}
            {messages.map((msg, idx) => (
              <MessageBubble key={idx} role={msg.role}>
                {msg.kind === 'songs' && <SongList items={msg.items} />}
                {msg.kind === 'movies' && <MovieList items={msg.items} />}
                {msg.kind === 'football' && <FootballResult data={msg.data} />}
                {msg.kind === 'structured' && <StructuredBlock data={msg.data} />}
                {msg.kind === 'image' && <ImageBubble src={msg.content} caption={msg.caption} />}
                {msg.kind === 'list' && (
                  <div className="space-y-1">
                    {msg.items.map((item, i) => (
                      <div key={`${item}-${i}`}>- {String(item)}</div>
                    ))}
                  </div>
                )}
                {msg.kind === 'text' && (
                  <div className="whitespace-pre-wrap">{msg.content}</div>
                )}
              </MessageBubble>
            ))}
            <div ref={endRef} />
          </div>
          <div className="border-t border-white/10 p-4 space-y-3">
            {variants && (
              <div className="flex flex-wrap gap-2">
                {variants.map((variant) => (
                  <button
                    key={variant.label}
                    className={`rounded-full px-3 py-1 text-xs ${
                      activeVariant?.label === variant.label
                        ? 'bg-white text-ink'
                        : 'bg-white/10 text-glacier'
                    }`}
                    onClick={() => setActiveVariant(variant)}
                  >
                    {variant.label}
                  </button>
                ))}
              </div>
            )}
            {imagePreview && (
              <div className="flex items-center gap-3">
                <img src={imagePreview} alt="preview" className="h-16 w-16 rounded-2xl object-cover" />
                <button
                  className="text-xs text-white/70 underline"
                  onClick={() => {
                    setImageFile(null)
                    setImagePreview('')
                  }}
                >
                  Remove image
                </button>
              </div>
            )}
            <textarea
              className="h-28 w-full resize-none rounded-2xl bg-white/5 p-4 text-base text-glacier outline-none"
              placeholder={placeholder}
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <label className="rounded-full bg-white/10 px-3 py-2 text-xs text-white cursor-pointer">
                  Add photo
                  <input
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={handleImageChange}
                  />
                </label>
                <Button variant="outline" onClick={() => setInput('')}>Clear</Button>
              </div>
              <Button onClick={handleSend} disabled={loading}>
                {loading ? 'Thinking...' : 'Send'}
              </Button>
            </div>
          </div>
        </div>
      </Card>
    </div>
  )
}
