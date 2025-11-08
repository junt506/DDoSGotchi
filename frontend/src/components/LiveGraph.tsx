import { useState, useEffect } from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Area,
  AreaChart,
} from 'recharts'
import { motion } from 'framer-motion'
import { RealtimeData } from '../hooks/useWebSocket'
import { TrendingUp } from 'lucide-react'

interface LiveGraphProps {
  data: RealtimeData
}

interface DataPoint {
  time: string
  latency: number
  packet_loss: number
  anomaly_score: number
}

export default function LiveGraph({ data }: LiveGraphProps) {
  const [history, setHistory] = useState<DataPoint[]>([])
  const maxPoints = 60 // Keep last 60 data points (1 minute at 1s intervals)

  useEffect(() => {
    const timestamp = new Date(data.timestamp)
    const timeStr = timestamp.toLocaleTimeString()

    const newPoint: DataPoint = {
      time: timeStr,
      latency: data.stats.latency,
      packet_loss: data.stats.packet_loss,
      anomaly_score: data.stats.anomaly_score * 100, // Scale to 0-100
    }

    setHistory((prev) => {
      const updated = [...prev, newPoint]
      return updated.slice(-maxPoints)
    })
  }, [data])

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="glass-panel p-3 border border-cyber-primary/50">
          <p className="text-sm text-gray-400 mb-2">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm font-medium" style={{ color: entry.color }}>
              {entry.name}: {entry.value.toFixed(2)}
              {entry.name === 'Latency' ? 'ms' : entry.name === 'Packet Loss' ? '%' : ''}
            </p>
          ))}
        </div>
      )
    }
    return null
  }

  return (
    <div className="glass-panel p-6">
      <div className="flex items-center gap-2 mb-6">
        <TrendingUp className="w-5 h-5 text-cyber-primary" />
        <h3 className="text-lg font-bold">Real-time Network Metrics</h3>
      </div>

      {/* Latency & Packet Loss Chart */}
      <motion.div
        className="mb-8"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <h4 className="text-sm text-gray-400 mb-3 font-medium">
          Latency & Packet Loss
        </h4>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={history}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis
              dataKey="time"
              stroke="#64748b"
              style={{ fontSize: '12px' }}
              tick={{ fill: '#94a3b8' }}
            />
            <YAxis
              stroke="#64748b"
              style={{ fontSize: '12px' }}
              tick={{ fill: '#94a3b8' }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              wrapperStyle={{ fontSize: '12px' }}
              iconType="circle"
            />
            <Line
              type="monotone"
              dataKey="latency"
              name="Latency"
              stroke="#00f0ff"
              strokeWidth={2}
              dot={false}
              animationDuration={300}
            />
            <Line
              type="monotone"
              dataKey="packet_loss"
              name="Packet Loss"
              stroke="#ff00aa"
              strokeWidth={2}
              dot={false}
              animationDuration={300}
            />
          </LineChart>
        </ResponsiveContainer>
      </motion.div>

      {/* Anomaly Score Chart */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <h4 className="text-sm text-gray-400 mb-3 font-medium">
          Anomaly Detection Score
        </h4>
        <ResponsiveContainer width="100%" height={200}>
          <AreaChart data={history}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis
              dataKey="time"
              stroke="#64748b"
              style={{ fontSize: '12px' }}
              tick={{ fill: '#94a3b8' }}
            />
            <YAxis
              stroke="#64748b"
              style={{ fontSize: '12px' }}
              tick={{ fill: '#94a3b8' }}
              domain={[0, 100]}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              wrapperStyle={{ fontSize: '12px' }}
              iconType="circle"
            />
            <Area
              type="monotone"
              dataKey="anomaly_score"
              name="Anomaly Score"
              stroke="#00ff88"
              fill="#00ff88"
              fillOpacity={0.3}
              strokeWidth={2}
              animationDuration={300}
            />
          </AreaChart>
        </ResponsiveContainer>
      </motion.div>

      {/* Threshold indicators */}
      <div className="flex gap-4 mt-4 text-xs">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-green-500" />
          <span className="text-gray-400">Normal (&lt; 30)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-yellow-500" />
          <span className="text-gray-400">Warning (30-60)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-red-500" />
          <span className="text-gray-400">Critical (&gt; 60)</span>
        </div>
      </div>
    </div>
  )
}
