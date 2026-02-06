import { useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import CompanionPanel from './CompanionPanel'

export default function CompanionOrb() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <motion.button
        className="fixed bottom-5 right-5 z-50 flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-accent to-accent2 text-ink shadow-2xl md:h-20 md:w-20"
        onClick={() => setOpen(true)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.98 }}
        aria-label="Open PUNTU"
      >
        <span className="text-2xl font-semibold md:text-3xl font-display">P</span>
      </motion.button>
      <AnimatePresence>
        {open && <CompanionPanel onClose={() => setOpen(false)} />}
      </AnimatePresence>
    </>
  )
}
