import { motion } from 'framer-motion'
import { ReactNode } from 'react'

interface StatsCardProps {
  title: string
  value: string | number
  icon: ReactNode
  status: 'safe' | 'warning' | 'danger'
  subtitle?: string
}

export default function StatsCard({
  title,
  value,
  icon,
  status,
  subtitle,
}: StatsCardProps) {
  const statusColors = {
    safe: 'from-emerald-500/20 to-cyan-500/20 border-cyan-500/30',
    warning: 'from-amber-500/20 to-orange-500/20 border-amber-500/30',
    danger: 'from-rose-500/20 to-pink-500/20 border-pink-500/30',
  }

  const iconColors = {
    safe: 'text-cyber-accent',
    warning: 'text-cyber-warning',
    danger: 'text-cyber-danger',
  }

  return (
    <motion.div
      className={`glass-panel p-4 bg-gradient-to-br ${statusColors[status]} hover:scale-105 transition-transform`}
      whileHover={{ y: -5 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="flex items-start justify-between mb-2">
        <div className="flex-1">
          <p className="text-gray-400 text-sm font-medium">{title}</p>
          <motion.p
            className={`text-2xl font-bold mt-1 ${iconColors[status]}`}
            key={value}
            initial={{ scale: 1.2, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.3 }}
          >
            {value}
          </motion.p>
          {subtitle && (
            <p className="text-gray-500 text-xs mt-1">{subtitle}</p>
          )}
        </div>
        <div className={`${iconColors[status]} opacity-50`}>{icon}</div>
      </div>
    </motion.div>
  )
}
