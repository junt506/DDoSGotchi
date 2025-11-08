import { motion, AnimatePresence } from 'framer-motion'
import { AttackInfo } from '../hooks/useWebSocket'
import { Shield, AlertTriangle, AlertOctagon, Zap } from 'lucide-react'

interface AttackPanelProps {
  attackInfo: AttackInfo
}

export default function AttackPanel({ attackInfo }: AttackPanelProps) {
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'from-red-500 to-pink-500'
      case 'high':
        return 'from-orange-500 to-red-500'
      case 'medium':
        return 'from-yellow-500 to-orange-500'
      case 'low':
        return 'from-blue-500 to-cyan-500'
      default:
        return 'from-green-500 to-emerald-500'
    }
  }

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <AlertOctagon className="w-8 h-8" />
      case 'high':
        return <AlertTriangle className="w-8 h-8" />
      case 'medium':
        return <Zap className="w-8 h-8" />
      default:
        return <Shield className="w-8 h-8" />
    }
  }

  return (
    <AnimatePresence mode="wait">
      {attackInfo.is_attack ? (
        <motion.div
          key="attack"
          className="glass-panel p-6 border-2 border-red-500/50 bg-gradient-to-br from-red-500/10 to-pink-500/10 animated-border"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          transition={{ duration: 0.3 }}
        >
          <div className="flex items-start gap-4">
            <motion.div
              className="text-red-500"
              animate={{ rotate: [0, 10, -10, 0] }}
              transition={{ duration: 0.5, repeat: Infinity }}
            >
              {getSeverityIcon(attackInfo.severity)}
            </motion.div>

            <div className="flex-1">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-xl font-bold text-red-400">
                  ⚠️ ATTACK DETECTED
                </h3>
                <span
                  className={`px-3 py-1 rounded-full text-xs font-bold bg-gradient-to-r ${getSeverityColor(
                    attackInfo.severity
                  )} text-white uppercase`}
                >
                  {attackInfo.severity}
                </span>
              </div>

              <p className="text-2xl font-bold text-white mb-2">
                {attackInfo.attack_type}
              </p>

              <div className="grid grid-cols-2 gap-4 mt-4">
                <div className="bg-black/30 p-3 rounded-lg">
                  <p className="text-gray-400 text-sm">Confidence</p>
                  <div className="flex items-center gap-2 mt-1">
                    <div className="flex-1 h-2 bg-gray-700 rounded-full overflow-hidden">
                      <motion.div
                        className="h-full bg-gradient-to-r from-red-500 to-pink-500"
                        initial={{ width: 0 }}
                        animate={{ width: `${attackInfo.confidence * 100}%` }}
                        transition={{ duration: 0.5 }}
                      />
                    </div>
                    <span className="text-sm font-bold">
                      {(attackInfo.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>

                <div className="bg-black/30 p-3 rounded-lg">
                  <p className="text-gray-400 text-sm">Anomaly Score</p>
                  <p className="text-xl font-bold text-red-400 mt-1">
                    {attackInfo.anomaly_score.toFixed(2)}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      ) : (
        <motion.div
          key="safe"
          className="glass-panel p-6 border-2 border-green-500/30 bg-gradient-to-br from-green-500/5 to-cyan-500/5"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          transition={{ duration: 0.3 }}
        >
          <div className="flex items-center gap-4">
            <Shield className="w-8 h-8 text-green-500" />
            <div>
              <h3 className="text-xl font-bold text-green-400">
                ✅ Network Secure
              </h3>
              <p className="text-gray-400">
                No malicious activity detected
              </p>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
