const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function agentRoute(payload) {
  const res = await fetch(`${API_BASE}/api/agent/route`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) {
    throw new Error('Agent request failed')
  }
  return res.json()
}

export async function streamLLM({ prompt, system, temperature = 0.6, onChunk }) {
  const res = await fetch(`${API_BASE}/api/llm/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt, system, temperature }),
  })
  if (!res.ok || !res.body) {
    throw new Error('Streaming failed')
  }
  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  while (true) {
    const { value, done } = await reader.read()
    if (done) break
    const chunk = decoder.decode(value, { stream: true })
    if (chunk) onChunk(chunk)
  }
}

export async function fetchSongs() {
  const res = await fetch(`${API_BASE}/api/modules/songs`)
  if (!res.ok) throw new Error('Failed to load songs')
  return res.json()
}

export async function fetchMovies() {
  const res = await fetch(`${API_BASE}/api/modules/movies`)
  if (!res.ok) throw new Error('Failed to load movies')
  return res.json()
}

export async function predictFootball(homeTeam, awayTeam) {
  const res = await fetch(`${API_BASE}/api/football/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ home_team: homeTeam, away_team: awayTeam }),
  })
  if (!res.ok) throw new Error('Prediction failed')
  return res.json()
}

export async function fetchFootballTeams() {
  const res = await fetch(`${API_BASE}/api/football/teams`)
  if (!res.ok) throw new Error('Failed to load teams')
  return res.json()
}

export async function analyzeImage({ file, prompt }) {
  const formData = new FormData()
  formData.append('file', file)
  if (prompt) formData.append('prompt', prompt)
  const res = await fetch(`${API_BASE}/api/vision/analyze`, {
    method: 'POST',
    body: formData,
  })
  if (!res.ok) {
    throw new Error('Image analysis failed')
  }
  return res.json()
}
