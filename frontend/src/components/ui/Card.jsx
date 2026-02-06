import { cx } from '../../lib/utils'

export default function Card({ children, className }) {
  return (
    <div className={cx('glass glow-ring rounded-3xl p-6', className)}>
      {children}
    </div>
  )
}
