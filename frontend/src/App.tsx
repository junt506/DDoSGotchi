import { useWebSocket } from './hooks/useWebSocket'
import Dashboard from './components/Dashboard'
import { Activity, WifiOff } from 'lucide-react'
import { memo } from 'react'

const Header = memo(({ isConnected }: { isConnected: boolean }) => (
  <header className="mb-8">
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-4">
        <Activity className="w-10 h-10 text-cyber-primary animate-pulse" />
        <div>
          <h1 className="text-4xl font-bold gradient-text">
            DDoS Gotchi
          </h1>
          <p className="text-gray-400 text-sm">
            Advanced DDoS Detection System v3.0
          </p>
        </div>
      </div>

      {/* Connection Status */}
      <div className={`flex items-center gap-2 px-4 py-2 rounded-lg glass-panel ${
        isConnected ? 'status-safe' : 'status-danger'
      }`}>
        <div className={`w-3 h-3 rounded-full ${
          isConnected ? 'bg-cyber-accent animate-pulse' : 'bg-cyber-danger'
        }`} />
        <span className="font-semibold">
          {isConnected ? 'Connected' : 'Disconnected'}
        </span>
      </div>
    </div>
  </header>
))

const Footer = memo(() => (
  <footer className="mt-8 text-center text-gray-500 text-sm">
    <p>Built with FastAPI + React + WebSocket</p>
    <p className="mt-1">
      Network Monitoring • Attack Detection • Real-time Analytics
    </p>
  </footer>
))

function App() {
  const { data, isConnected, error, reconnect } = useWebSocket('/ws/realtime')

  return (
    <div className="min-h-screen p-6 scanlines">
      <Header isConnected={isConnected} />

      {/* Main Content */}
      {!isConnected && (
        <div className="glass-panel p-8 text-center mb-8">
          <WifiOff className="w-16 h-16 mx-auto mb-4 text-cyber-danger" />
          <h2 className="text-2xl font-bold mb-2">Connection Lost</h2>
          <p className="text-gray-400 mb-4">
            {error || 'Unable to connect to backend server'}
          </p>
          <button onClick={reconnect} className="cyber-button">
            Reconnect
          </button>
        </div>
      )}

      {data && isConnected && <Dashboard data={data} />}

      <Footer />
    </div>
  )
}

export default App
