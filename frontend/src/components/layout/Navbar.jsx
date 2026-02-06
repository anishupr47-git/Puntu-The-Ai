import { NavLink } from 'react-router-dom'
import { modules } from '../../data/modules'
import { AnimatePresence, motion } from 'framer-motion'
import { useState } from 'react'

export default function Navbar() {
  const [open, setOpen] = useState(false)

  return (
    <div className="sticky top-0 z-40 backdrop-blur-xl">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <div className="text-2xl font-semibold tracking-wide font-display">PUNTU</div>
        <nav className="hidden gap-3 md:flex">
          {modules.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `relative rounded-full px-3 py-1 text-sm transition ${
                  isActive ? 'text-white' : 'text-mist'
                }`
              }
            >
              {({ isActive }) => (
                <span className="relative">
                  {item.label}
                  {isActive && (
                    <motion.span
                      layoutId="nav-pill"
                      className="absolute -inset-x-2 -inset-y-1 rounded-full bg-white/10"
                      transition={{ type: 'spring', stiffness: 380, damping: 30 }}
                    />
                  )}
                </span>
              )}
            </NavLink>
          ))}
        </nav>
        <button
          className="md:hidden rounded-full bg-white/10 px-3 py-1 text-xs"
          onClick={() => setOpen(true)}
        >
          Menu
        </button>
      </div>
      <AnimatePresence>
        {open && (
          <motion.div
            className="fixed inset-0 z-50 bg-black/60"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setOpen(false)}
          >
            <motion.div
              className="glass absolute right-4 top-4 w-[calc(100%-2rem)] rounded-2xl p-4"
              initial={{ y: -10, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: -10, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
            >
              <div className="mb-3 text-sm text-mist">Navigate</div>
              <div className="grid gap-2">
                {modules.map((item) => (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    onClick={() => setOpen(false)}
                    className={({ isActive }) =>
                      `rounded-xl px-3 py-2 text-sm ${
                        isActive ? 'bg-white text-ink' : 'bg-white/10 text-white'
                      }`
                    }
                  >
                    {item.label}
                  </NavLink>
                ))}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
