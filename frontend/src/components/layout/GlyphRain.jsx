import { useEffect, useRef } from 'react'

const GLYPHS = ['🤖','Hello I Am Puntu','Your Companion','Who Understands And Feels You','Always There To Assist You']

export default function GlyphRain() {
  const canvasRef = useRef(null)
  const rafRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const resize = () => {
      const { innerWidth, innerHeight } = window
      canvas.width = innerWidth * window.devicePixelRatio
      canvas.height = innerHeight * window.devicePixelRatio
      canvas.style.width = `${innerWidth}px`
      canvas.style.height = `${innerHeight}px`
      ctx.setTransform(window.devicePixelRatio, 0, 0, window.devicePixelRatio, 0, 0)
    }

    resize()
    window.addEventListener('resize', resize)

    const count = 42
    const minDist = 38
    const items = Array.from({ length: count }).map((_, idx) => {
      const size = 12 + (idx % 6) * 2
      return {
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        vy: 0.4 + Math.random() * 0.8,
        vx: (Math.random() - 0.5) * 0.3,
        size,
        glyph: GLYPHS[idx % GLYPHS.length],
        opacity: 0.25 + Math.random() * 0.35,
      }
    })

    const step = () => {
      ctx.clearRect(0, 0, window.innerWidth, window.innerHeight)

      for (let i = 0; i < items.length; i++) {
        const a = items[i]
        for (let j = i + 1; j < items.length; j++) {
          const b = items[j]
          const dx = b.x - a.x
          const dy = b.y - a.y
          const dist = Math.sqrt(dx * dx + dy * dy)
          if (dist > 0 && dist < minDist) {
            const force = (minDist - dist) / minDist * 0.08
            const fx = (dx / dist) * force
            const fy = (dy / dist) * force
            a.vx -= fx
            a.vy -= fy
            b.vx += fx
            b.vy += fy
          }
        }
      }

      for (const item of items) {
        item.y += item.vy
        item.x += item.vx
        item.vx *= 0.99
        item.vy = Math.min(item.vy + 0.002, 1.4)

        if (item.y > window.innerHeight + 20) {
          item.y = -20
          item.x = Math.random() * window.innerWidth
          item.vy = 0.4 + Math.random() * 0.8
          item.vx = (Math.random() - 0.5) * 0.3
        }
        if (item.x < -20) item.x = window.innerWidth + 20
        if (item.x > window.innerWidth + 20) item.x = -20

        ctx.font = `${item.size}px 'Space Grotesk', sans-serif`
        ctx.fillStyle = `rgba(220, 235, 255, ${item.opacity})`
        ctx.fillText(item.glyph, item.x, item.y)
      }

      rafRef.current = requestAnimationFrame(step)
    }

    rafRef.current = requestAnimationFrame(step)

    return () => {
      window.removeEventListener('resize', resize)
      if (rafRef.current) cancelAnimationFrame(rafRef.current)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="pointer-events-none fixed inset-0 z-[-1]"
      aria-hidden="true"
    />
  )
}
