"""
DDoS Gotchi - FastAPI Backend
Production-grade API with WebSocket support
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import asyncio
import json
from typing import List, Dict, Any
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.network_monitor import NetworkMonitor
from core.attack_detector import AttackDetector
from core.network_watcher import NetworkWatcher
from database.manager import DatabaseManager
from utils.config import Settings

# Initialize settings
settings = Settings()

# Global state
monitor_state = {
    'network_monitor': None,
    'attack_detector': None,
    'network_watcher': None,
    'db_manager': None,
    'active_connections': []
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    print("🚀 Starting DDoS Gotchi Backend...")

    # Initialize database
    monitor_state['db_manager'] = DatabaseManager()
    await monitor_state['db_manager'].init_db()

    # Initialize network monitoring
    monitor_state['network_monitor'] = NetworkMonitor()
    monitor_state['attack_detector'] = AttackDetector()
    monitor_state['network_watcher'] = NetworkWatcher(monitor_state['network_monitor'])

    # Start background monitoring
    monitor_state['network_watcher'].start()

    print("✅ Backend ready!")

    yield

    # Shutdown
    print("🛑 Shutting down...")
    if monitor_state['network_watcher']:
        monitor_state['network_watcher'].stop()
    print("✅ Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="DDoS Gotchi API",
    description="Advanced DDoS Detection System with Real-time Monitoring",
    version="3.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# WEBSOCKET ENDPOINTS
# ============================================================================

class ConnectionManager:
    """Manages WebSocket connections"""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"✅ WebSocket connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"❌ WebSocket disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting: {e}")


manager = ConnectionManager()


@app.websocket("/ws/realtime")
async def websocket_realtime(websocket: WebSocket):
    """Real-time data stream via WebSocket"""
    await manager.connect(websocket)

    try:
        while True:
            try:
                # Get current stats
                stats = monitor_state['network_monitor'].get_current_stats()
                attack_info = monitor_state['attack_detector'].detect(stats)

                # Convert attack_info to match frontend expectations
                attack_message = {
                    'is_attack': attack_info.get('attack_detected', False),
                    'attack_type': attack_info.get('attack_type'),
                    'confidence': float(attack_info.get('confidence', 0)),
                    'severity': 'low',  # Default severity
                    'anomaly_score': float(attack_info.get('anomaly_score', 0))
                }

                # Determine severity based on confidence
                confidence = attack_message['confidence']
                if confidence > 0.8:
                    attack_message['severity'] = 'critical'
                elif confidence > 0.6:
                    attack_message['severity'] = 'high'
                elif confidence > 0.4:
                    attack_message['severity'] = 'medium'

                # Prepare message with explicit type conversions
                message = {
                    'timestamp': datetime.now().isoformat(),
                    'stats': {
                        'connected': bool(stats.get('connected', False)),
                        'latency': float(stats.get('latency', -1)),
                        'packet_loss': float(stats.get('packet_loss', 0)),
                        'anomaly_score': float(attack_info.get('anomaly_score', 0)),
                        'ip_address': str(stats.get('ip_address', 'N/A')),
                        'gateway': str(stats.get('gateway', 'N/A')),
                        'network': str(stats.get('network', 'N/A')),
                        'ssid': str(stats.get('ssid', 'N/A'))
                    },
                    'attack_info': attack_message,
                    'state': str(attack_info.get('state', 'unknown'))
                }

                # Send to client
                await websocket.send_json(message)

            except Exception as e:
                print(f"❌ Error preparing WebSocket message: {e}")
                import traceback
                traceback.print_exc()

            # Wait before next update
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"❌ WebSocket connection error: {e}")
        import traceback
        traceback.print_exc()
        try:
            manager.disconnect(websocket)
        except:
            pass


# ============================================================================
# REST API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "DDoS Gotchi API",
        "version": "3.0.0",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "monitoring_active": monitor_state['network_monitor'] is not None
    }


@app.get("/api/stats/current")
async def get_current_stats():
    """Get current network statistics"""
    if not monitor_state['network_monitor']:
        raise HTTPException(status_code=503, detail="Monitor not initialized")

    stats = monitor_state['network_monitor'].get_current_stats()
    attack_info = monitor_state['attack_detector'].detect(stats)

    return {
        "timestamp": datetime.now().isoformat(),
        "stats": stats,
        "attack_info": attack_info
    }


@app.get("/api/stats/history")
async def get_stats_history(limit: int = 100):
    """Get historical statistics"""
    if not monitor_state['db_manager']:
        raise HTTPException(status_code=503, detail="Database not initialized")

    history = await monitor_state['db_manager'].get_stats_history(limit)
    return {"data": history}


@app.get("/api/attacks/recent")
async def get_recent_attacks(hours: int = 24):
    """Get recent attacks"""
    if not monitor_state['db_manager']:
        raise HTTPException(status_code=503, detail="Database not initialized")

    attacks = await monitor_state['db_manager'].get_recent_attacks(hours)
    return {"attacks": attacks}


@app.get("/api/network/info")
async def get_network_info():
    """Get current network information"""
    if not monitor_state['network_monitor']:
        raise HTTPException(status_code=503, detail="Monitor not initialized")

    return monitor_state['network_monitor'].get_network_info()


@app.post("/api/config/update")
async def update_config(config: Dict[str, Any]):
    """Update configuration"""
    # Validate and update config
    # This would update the monitoring thresholds, etc.
    return {"status": "updated", "config": config}


@app.get("/api/system/status")
async def get_system_status():
    """Get system status and metrics"""
    import psutil

    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "network_connections": len(psutil.net_connections()),
        "uptime": datetime.now().isoformat()
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    print(f"❌ Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "type": type(exc).__name__}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
