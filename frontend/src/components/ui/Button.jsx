import { cx } from '../../lib/utils'

export default function Button({ children, variant = 'primary', className, ...props }) {
  const base = 'inline-flex items-center justify-center rounded-full px-5 py-2.5 text-sm font-medium transition'
  const styles = {
    primary: 'bg-white text-ink hover:bg-glacier',
    ghost: 'bg-white/10 text-white hover:bg-white/20',
    outline: 'border border-white/30 text-white hover:bg-white/10',
  }
  return (
    <button className={cx(base, styles[variant], className)} {...props}>
      {children}
    </button>
  )
}
