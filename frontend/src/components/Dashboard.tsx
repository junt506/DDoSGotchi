import { motion } from 'framer-motion'
import { RealtimeData } from '../hooks/useWebSocket'
import StatsCard from './StatsCard'
import LiveGraph from './LiveGraph'
import GotchiPet from './GotchiPet'
import AttackPanel from './AttackPanel'
import {
  Activity,
  Wifi,
  Clock,
  AlertTriangle,
  TrendingUp,
  Network,
} from 'lucide-react'

interface DashboardProps {
  data: RealtimeData
}

export default function Dashboard({ data }: DashboardProps) {
  const { stats, attack_info, state } = data

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
      {/* Left Column - Stats Cards */}
      <motion.div
        className="lg:col-span-8 space-y-6"
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5 }}
      >
        {/* Top Stats Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
          <StatsCard
            title="Connection"
            value={stats.connected ? 'Connected' : 'Disconnected'}
            icon={<Wifi />}
            status={stats.connected ? 'safe' : 'danger'}
            subtitle={stats.ssid || 'No network'}
          />

          <StatsCard
            title="Latency"
            value={`${stats.latency.toFixed(1)}ms`}
            icon={<Clock />}
            status={
              stats.latency < 50
                ? 'safe'
                : stats.latency < 100
                ? 'warning'
                : 'danger'
            }
            subtitle={`Avg: ${stats.latency.toFixed(0)}ms`}
          />

          <StatsCard
            title="Packet Loss"
            value={`${stats.packet_loss.toFixed(1)}%`}
            icon={<TrendingUp />}
            status={
              stats.packet_loss < 1
                ? 'safe'
                : stats.packet_loss < 5
                ? 'warning'
                : 'danger'
            }
            subtitle={stats.packet_loss < 1 ? 'Excellent' : 'High Loss'}
          />

          <StatsCard
            title="Anomaly Score"
            value={stats.anomaly_score.toFixed(2)}
            icon={<Activity />}
            status={
              stats.anomaly_score < 0.3
                ? 'safe'
                : stats.anomaly_score < 0.6
                ? 'warning'
                : 'danger'
            }
            subtitle={`State: ${state}`}
          />
        </div>

        {/* Network Info Panel */}
        <div className="glass-panel p-6">
          <div className="flex items-center gap-2 mb-4">
            <Network className="w-5 h-5 text-cyber-primary" />
            <h3 className="text-lg font-bold">Network Information</h3>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-gray-400 text-sm">IP Address</p>
              <p className="font-mono text-cyber-accent">
                {stats.ip_address || 'N/A'}
              </p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Gateway</p>
              <p className="font-mono text-cyber-primary">
                {stats.gateway || 'N/A'}
              </p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Network</p>
              <p className="font-mono">{stats.network || 'N/A'}</p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">SSID</p>
              <p className="font-mono">{stats.ssid || 'N/A'}</p>
            </div>
          </div>
        </div>

        {/* Attack Detection Panel */}
        <AttackPanel attackInfo={attack_info} />

        {/* Live Graphs */}
        <LiveGraph data={data} />
      </motion.div>

      {/* Right Column - Gotchi Pet */}
      <motion.div
        className="lg:col-span-4"
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <GotchiPet
          isAttack={attack_info.is_attack}
          state={state}
          anomalyScore={stats.anomaly_score}
          connected={stats.connected}
        />
      </motion.div>
    </div>
  )
}
