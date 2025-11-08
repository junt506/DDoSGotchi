import { useEffect, useState, useCallback, useRef } from 'react'

export interface NetworkStats {
  connected: boolean
  latency: number
  packet_loss: number
  anomaly_score: number
  ip_address?: string
  gateway?: string
  network?: string
  ssid?: string
}

export interface AttackInfo {
  is_attack: boolean
  attack_type?: string
  confidence: number
  severity: 'low' | 'medium' | 'high' | 'critical'
  anomaly_score: number
}

export interface RealtimeData {
  timestamp: string
  stats: NetworkStats
  attack_info: AttackInfo
  state: string
}

interface UseWebSocketReturn {
  data: RealtimeData | null
  isConnected: boolean
  error: string | null
  reconnect: () => void
}

export function useWebSocket(url: string): UseWebSocketReturn {
  const [data, setData] = useState<RealtimeData | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>()
  const reconnectAttemptsRef = useRef(0)

  const connect = useCallback(() => {
    try {
      // Close existing connection
      if (wsRef.current) {
        wsRef.current.close()
      }

      // Create WebSocket URL (handle both dev and production)
      const wsUrl = url.startsWith('ws')
        ? url
        : `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}${url}`

      console.log('🔌 Connecting to WebSocket:', wsUrl)
      const ws = new WebSocket(wsUrl)

      ws.onopen = () => {
        console.log('✅ WebSocket connected')
        setIsConnected(true)
        setError(null)
        reconnectAttemptsRef.current = 0
      }

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)

          // Ignore initial connection message
          if (message.type === 'connected') {
            console.log('📩 Received connection confirmation')
            return
          }

          // Process real-time data
          setData(message as RealtimeData)
        } catch (err) {
          console.error('Failed to parse WebSocket message:', err, event.data)
        }
      }

      ws.onerror = (event) => {
        console.error('❌ WebSocket error:', event)
        setError('WebSocket connection error')
      }

      ws.onclose = () => {
        console.log('🔌 WebSocket disconnected')
        setIsConnected(false)

        // Exponential backoff reconnection
        const delay = Math.min(1000 * Math.pow(2, reconnectAttemptsRef.current), 30000)
        reconnectAttemptsRef.current += 1

        console.log(`🔄 Reconnecting in ${delay}ms (attempt ${reconnectAttemptsRef.current})`)

        reconnectTimeoutRef.current = setTimeout(() => {
          connect()
        }, delay)
      }

      wsRef.current = ws
    } catch (err) {
      console.error('Failed to create WebSocket:', err)
      setError(err instanceof Error ? err.message : 'Unknown error')
    }
  }, [url])

  const reconnect = useCallback(() => {
    reconnectAttemptsRef.current = 0
    connect()
  }, [connect])

  useEffect(() => {
    connect()

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current)
      }
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [connect])

  return { data, isConnected, error, reconnect }
}
