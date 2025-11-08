# DDoS Gotchi API Documentation

Complete API reference for DDoS Gotchi v3.0 Backend.

## Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
```

## Authentication

Currently, the API does not require authentication. For production deployments, consider adding:
- API Keys
- JWT tokens
- OAuth 2.0

## API Endpoints

### Health Check

#### `GET /api/health`

Check if the API is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "monitoring_active": true
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

### Root Endpoint

#### `GET /`

Get API information.

**Response:**
```json
{
  "name": "DDoS Gotchi API",
  "version": "3.0.0",
  "status": "operational",
  "docs": "/docs"
}
```

---

### Current Statistics

#### `GET /api/stats/current`

Get current real-time network statistics.

**Response:**
```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "stats": {
    "connected": true,
    "latency": 12.5,
    "packet_loss": 0.2,
    "anomaly_score": 0.15,
    "ip_address": "192.168.1.100",
    "gateway": "192.168.1.1",
    "network": "192.168.1.0/24",
    "ssid": "MyNetwork"
  },
  "attack_info": {
    "is_attack": false,
    "attack_type": null,
    "confidence": 0.0,
    "severity": "low",
    "anomaly_score": 0.15
  }
}
```

**Status Codes:**
- `200 OK` - Statistics retrieved successfully
- `503 Service Unavailable` - Monitor not initialized

---

### Statistics History

#### `GET /api/stats/history`

Get historical statistics from the database.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | integer | 100 | Maximum number of records to return |

**Example Request:**
```bash
curl "http://localhost:8000/api/stats/history?limit=50"
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "timestamp": "2024-01-15T10:30:00",
      "connected": true,
      "latency": 12.5,
      "packet_loss": 0.2,
      "state": "GOOD",
      "anomaly_score": 0.15
    },
    {
      "id": 2,
      "timestamp": "2024-01-15T10:30:01",
      "connected": true,
      "latency": 13.2,
      "packet_loss": 0.1,
      "state": "GOOD",
      "anomaly_score": 0.12
    }
  ]
}
```

**Status Codes:**
- `200 OK` - History retrieved successfully
- `503 Service Unavailable` - Database not initialized

---

### Recent Attacks

#### `GET /api/attacks/recent`

Get recently detected attacks.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| hours | integer | 24 | Time range in hours |

**Example Request:**
```bash
curl "http://localhost:8000/api/attacks/recent?hours=48"
```

**Response:**
```json
{
  "attacks": [
    {
      "id": 1,
      "timestamp": "2024-01-15T09:15:00",
      "attack_type": "SYN Flood Detected",
      "latency": 450.5,
      "packet_loss": 15.3,
      "anomaly_score": 0.85,
      "confidence": 0.92,
      "severity": "high"
    },
    {
      "id": 2,
      "timestamp": "2024-01-15T08:30:00",
      "attack_type": "UDP Flood Detected",
      "latency": 320.1,
      "packet_loss": 25.7,
      "anomaly_score": 0.91,
      "confidence": 0.88,
      "severity": "critical"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Attacks retrieved successfully
- `503 Service Unavailable` - Database not initialized

---

### Network Information

#### `GET /api/network/info`

Get detailed network information.

**Response:**
```json
{
  "gateway": "192.168.1.1",
  "network": "192.168.1.0/24",
  "interface": "wlan0",
  "ssid": "MyNetwork",
  "ip_address": "192.168.1.100",
  "connected": true,
  "state": "GOOD"
}
```

**Status Codes:**
- `200 OK` - Network info retrieved successfully
- `503 Service Unavailable` - Monitor not initialized

---

### System Status

#### `GET /api/system/status`

Get system resource usage and metrics.

**Response:**
```json
{
  "cpu_percent": 15.2,
  "memory_percent": 42.8,
  "disk_percent": 35.6,
  "network_connections": 127,
  "uptime": "2024-01-15T10:30:00.000Z"
}
```

**Status Codes:**
- `200 OK` - System status retrieved successfully

---

### Update Configuration

#### `POST /api/config/update`

Update monitoring configuration.

**Request Body:**
```json
{
  "ping_interval": 2,
  "latency_threshold": 150.0,
  "packet_loss_threshold": 10.0,
  "anomaly_threshold": 0.7
}
```

**Response:**
```json
{
  "status": "updated",
  "config": {
    "ping_interval": 2,
    "latency_threshold": 150.0,
    "packet_loss_threshold": 10.0,
    "anomaly_threshold": 0.7
  }
}
```

**Status Codes:**
- `200 OK` - Configuration updated successfully
- `400 Bad Request` - Invalid configuration

---

## WebSocket Endpoints

### Real-time Data Stream

#### `WS /ws/realtime`

WebSocket connection for real-time network monitoring data.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/realtime');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};
```

**Message Format:**
```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "stats": {
    "connected": true,
    "latency": 12.5,
    "packet_loss": 0.2,
    "anomaly_score": 0.15,
    "ip_address": "192.168.1.100",
    "gateway": "192.168.1.1",
    "network": "192.168.1.0/24",
    "ssid": "MyNetwork"
  },
  "attack_info": {
    "is_attack": false,
    "attack_type": null,
    "confidence": 0.0,
    "severity": "low",
    "anomaly_score": 0.15
  },
  "state": "GOOD"
}
```

**Update Frequency:**
- 1 second intervals

**Connection Lifecycle:**
1. Client connects to WebSocket endpoint
2. Server accepts connection
3. Server sends data every 1 second
4. Client receives and processes data
5. Connection remains open until closed by either party

**Error Handling:**
```javascript
ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('WebSocket closed, reconnecting...');
  // Implement reconnection logic
};
```

---

## Data Models

### NetworkStats

```typescript
interface NetworkStats {
  connected: boolean;        // Network connectivity status
  latency: number;          // Round-trip time in milliseconds
  packet_loss: number;      // Packet loss percentage (0-100)
  anomaly_score: number;    // Anomaly detection score (0-1)
  ip_address?: string;      // Local IP address
  gateway?: string;         // Gateway IP address
  network?: string;         // Network CIDR
  ssid?: string;           // WiFi SSID (if applicable)
}
```

### AttackInfo

```typescript
interface AttackInfo {
  is_attack: boolean;                        // Attack detected flag
  attack_type?: string;                      // Type of attack
  confidence: number;                        // Confidence score (0-1)
  severity: 'low' | 'medium' | 'high' | 'critical';  // Attack severity
  anomaly_score: number;                     // Anomaly score (0-1)
}
```

### Attack Types

- `"SYN Flood / Resource Exhaustion"` - High latency, low packet loss
- `"UDP Flood Detected"` - High packet loss and latency
- `"ICMP Flood / Network Saturation"` - Very high packet loss
- `"Mixed DDoS Attack"` - Moderate latency and packet loss
- `"Network Congestion / Slow DDoS"` - Moderate latency

---

## Error Responses

### Standard Error Format

```json
{
  "error": "Error message description",
  "type": "ErrorType"
}
```

### Common HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |
| 503 | Service Unavailable - Service not initialized |

---

## Rate Limiting

Currently, no rate limiting is implemented. For production:

**Recommended limits:**
- REST API: 100 requests/minute per IP
- WebSocket: 1 connection per IP
- Stats history: 10 requests/minute

---

## Code Examples

### Python

```python
import requests
import json

# Get current stats
response = requests.get('http://localhost:8000/api/stats/current')
data = response.json()
print(json.dumps(data, indent=2))

# Get attack history
response = requests.get('http://localhost:8000/api/attacks/recent?hours=24')
attacks = response.json()
print(f"Found {len(attacks['attacks'])} attacks")
```

### JavaScript/TypeScript

```typescript
// Fetch current stats
const response = await fetch('http://localhost:8000/api/stats/current');
const data = await response.json();
console.log(data);

// WebSocket connection
const ws = new WebSocket('ws://localhost:8000/ws/realtime');

ws.onopen = () => {
  console.log('Connected to DDoS Gotchi');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.attack_info.is_attack) {
    console.warn(`Attack detected: ${data.attack_info.attack_type}`);
  }
};
```

### cURL

```bash
# Health check
curl http://localhost:8000/api/health

# Current stats
curl http://localhost:8000/api/stats/current

# Attack history
curl "http://localhost:8000/api/attacks/recent?hours=48"

# Update config
curl -X POST http://localhost:8000/api/config/update \
  -H "Content-Type: application/json" \
  -d '{"ping_interval": 2}'
```

---

## Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- Explore all endpoints
- Test API calls directly
- View request/response schemas
- See example data

---

## Changelog

### v3.0.0
- Complete rewrite with FastAPI
- WebSocket real-time streaming
- SQLite database integration
- Network switching detection
- Advanced attack classification

---

## Support

For API issues or questions:
- GitHub Issues: https://github.com/yourusername/DDoSGotchi/issues
- API Documentation: http://localhost:8000/docs
