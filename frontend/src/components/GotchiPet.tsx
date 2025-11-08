import { motion, AnimatePresence } from 'framer-motion'
import { Heart, Shield, Skull, Wifi } from 'lucide-react'

interface GotchiPetProps {
  isAttack: boolean
  state: string
  anomalyScore: number
  connected: boolean
}

export default function GotchiPet({
  isAttack,
  state,
  anomalyScore,
  connected,
}: GotchiPetProps) {
  const getHealth = () => {
    if (!connected) return 0
    if (isAttack) return Math.max(10, 100 - anomalyScore * 100)
    return 100 - anomalyScore * 50
  }

  const getMood = () => {
    if (!connected) return 'disconnected'
    if (isAttack) return 'under_attack'
    if (anomalyScore > 0.5) return 'stressed'
    if (anomalyScore > 0.3) return 'alert'
    return 'happy'
  }

  const health = getHealth()
  const mood = getMood()

  const moodEmojis = {
    happy: '😊',
    alert: '😐',
    stressed: '😰',
    under_attack: '😱',
    disconnected: '💀',
  }

  const moodColors = {
    happy: 'from-green-500 to-emerald-500',
    alert: 'from-blue-500 to-cyan-500',
    stressed: 'from-yellow-500 to-orange-500',
    under_attack: 'from-red-500 to-pink-500',
    disconnected: 'from-gray-500 to-gray-700',
  }

  const moodMessages = {
    happy: 'Everything looks great! 🎉',
    alert: 'Staying vigilant... 👀',
    stressed: 'Network activity increasing! 📈',
    under_attack: 'UNDER ATTACK! HELP! 🚨',
    disconnected: 'Connection lost... 💔',
  }

  return (
    <div className="glass-panel p-6 h-full sticky top-6">
      <div className="text-center">
        <h3 className="text-lg font-bold mb-4 flex items-center justify-center gap-2">
          <Heart className="w-5 h-5 text-red-500" />
          Network Guardian
        </h3>

        {/* Pet Character */}
        <motion.div
          className="relative mb-6"
          animate={
            isAttack
              ? {
                  scale: [1, 1.1, 0.9, 1.1, 1],
                  rotate: [0, -5, 5, -5, 0],
                }
              : connected
              ? { y: [0, -10, 0] }
              : {}
          }
          transition={{
            duration: isAttack ? 0.5 : 3,
            repeat: Infinity,
            repeatType: 'loop',
          }}
        >
          <div
            className={`text-9xl mb-4 filter drop-shadow-2xl ${
              !connected ? 'grayscale' : ''
            }`}
          >
            {moodEmojis[mood as keyof typeof moodEmojis]}
          </div>

          {/* Glow effect */}
          <motion.div
            className={`absolute inset-0 blur-3xl opacity-50 bg-gradient-to-r ${
              moodColors[mood as keyof typeof moodColors]
            }`}
            animate={{ opacity: [0.3, 0.6, 0.3] }}
            transition={{ duration: 2, repeat: Infinity }}
          />
        </motion.div>

        {/* Status Message */}
        <AnimatePresence mode="wait">
          <motion.p
            key={mood}
            className="text-lg font-medium mb-6 text-gray-300"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3 }}
          >
            {moodMessages[mood as keyof typeof moodMessages]}
          </motion.p>
        </AnimatePresence>

        {/* Health Bar */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-400 flex items-center gap-2">
              <Heart className="w-4 h-4" />
              Health
            </span>
            <span className="text-sm font-bold">{health.toFixed(0)}%</span>
          </div>

          <div className="h-4 bg-gray-700 rounded-full overflow-hidden">
            <motion.div
              className={`h-full bg-gradient-to-r ${
                health > 70
                  ? 'from-green-500 to-emerald-500'
                  : health > 30
                  ? 'from-yellow-500 to-orange-500'
                  : 'from-red-500 to-pink-500'
              }`}
              initial={{ width: 0 }}
              animate={{ width: `${health}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="glass-panel p-4">
            <Shield className="w-6 h-6 mx-auto mb-2 text-cyber-primary" />
            <p className="text-xs text-gray-400">Protection</p>
            <p className="text-lg font-bold text-cyber-accent">
              {connected ? 'Active' : 'Offline'}
            </p>
          </div>

          <div className="glass-panel p-4">
            <Wifi className="w-6 h-6 mx-auto mb-2 text-cyber-secondary" />
            <p className="text-xs text-gray-400">Network</p>
            <p className="text-lg font-bold text-cyber-primary">{state}</p>
          </div>
        </div>

        {/* Attack Alert */}
        {isAttack && (
          <motion.div
            className="bg-red-500/20 border-2 border-red-500 rounded-lg p-4 mb-4"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            <Skull className="w-8 h-8 mx-auto mb-2 text-red-500 animate-pulse" />
            <p className="text-sm font-bold text-red-400">
              ACTIVE ATTACK DETECTED!
            </p>
            <p className="text-xs text-gray-300 mt-1">
              Defending your network...
            </p>
          </motion.div>
        )}

        {/* Mood Badge */}
        <div
          className={`inline-block px-4 py-2 rounded-full text-sm font-bold bg-gradient-to-r ${
            moodColors[mood as keyof typeof moodColors]
          } text-white uppercase tracking-wide`}
        >
          {mood.replace('_', ' ')}
        </div>
      </div>
    </div>
  )
}
