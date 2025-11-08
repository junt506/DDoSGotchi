# DDoS Gotchi v3.0 - Deployment Guide

Complete deployment guide for DDoS Gotchi Advanced DDoS Detection System.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start (Docker)](#quick-start-docker)
- [Development Mode](#development-mode)
- [Production Deployment](#production-deployment)
- [Systemd Service](#systemd-service)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- **OS**: Linux (Fedora, Ubuntu, Debian, or any modern distro)
- **CPU**: 2+ cores recommended
- **RAM**: 2GB+ recommended
- **Network**: Active network connection for monitoring

### Software Requirements

#### For Docker Deployment
- Docker 20.10+
- Docker Compose 2.0+

#### For Development Mode
- Python 3.11+
- Node.js 18+
- npm 9+

## Quick Start (Docker)

The fastest way to get DDoS Gotchi running:

```bash
# Clone the repository
git clone https://github.com/yourusername/DDoSGotchi.git
cd DDoSGotchi

# Start with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f
```

**Access the application:**
- Frontend Dashboard: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development Mode

For development and testing without Docker:

```bash
# Run the development script
./start-dev.sh

# Or manually:

# 1. Start Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# 2. Start Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

**Development URLs:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Hot reload enabled for both

## Production Deployment

### Option 1: Docker Compose (Recommended)

1. **Configure environment variables:**
```bash
# Create .env file
cat > .env << EOF
# Backend Configuration
API_HOST=0.0.0.0
API_PORT=8000
DATABASE_URL=sqlite:////app/data/ddosgotchi.db

# Frontend Configuration
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
EOF
```

2. **Start services:**
```bash
docker-compose up -d
```

3. **Verify deployment:**
```bash
docker-compose ps
docker-compose logs
```

### Option 2: Manual Deployment

#### Backend Deployment

```bash
# Install backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with production settings
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Frontend Deployment

```bash
# Build frontend
cd frontend
npm install
npm run build

# Serve with nginx
sudo cp -r dist/* /var/www/ddosgotchi/
sudo systemctl restart nginx
```

**Nginx configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /var/www/ddosgotchi;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
```

## Systemd Service

For automatic startup and management:

### Installation

```bash
# Run the install script as root
sudo ./install-service.sh
```

The script will:
1. Copy files to `/opt/ddosgotchi`
2. Install systemd service
3. Enable auto-start on boot

### Management Commands

```bash
# Start the service
sudo systemctl start ddosgotchi

# Stop the service
sudo systemctl stop ddosgotchi

# Restart the service
sudo systemctl restart ddosgotchi

# Check status
sudo systemctl status ddosgotchi

# View logs
sudo journalctl -u ddosgotchi -f

# Enable auto-start
sudo systemctl enable ddosgotchi

# Disable auto-start
sudo systemctl disable ddosgotchi
```

### Uninstallation

```bash
sudo ./uninstall-service.sh
```

## Configuration

### Backend Configuration

Edit `backend/utils/config.py` for advanced settings:

```python
class Settings(BaseSettings):
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Database
    database_url: str = "sqlite:///./ddosgotchi.db"

    # Monitoring Settings
    ping_interval: int = 1  # seconds
    ping_count: int = 5

    # Detection Thresholds
    latency_threshold: float = 100.0  # ms
    packet_loss_threshold: float = 5.0  # %
    anomaly_threshold: float = 0.6
```

### Frontend Configuration

Edit `frontend/.env`:

```bash
# API endpoints
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000

# Update interval (ms)
VITE_UPDATE_INTERVAL=1000
```

### Docker Configuration

Edit `docker-compose.yml`:

```yaml
services:
  backend:
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - DATABASE_URL=sqlite:////app/data/ddosgotchi.db
    ports:
      - "8000:8000"

  frontend:
    environment:
      - VITE_API_URL=http://localhost:8000
      - VITE_WS_URL=ws://localhost:8000
    ports:
      - "3000:80"
```

## Troubleshooting

### Backend Issues

**Problem: Permission denied for ping**
```bash
# Solution: Run with proper capabilities or as root
docker-compose down
docker-compose up -d  # Already configured with NET_ADMIN capability
```

**Problem: Database locked**
```bash
# Solution: Stop all instances
docker-compose down
rm data/ddosgotchi.db  # Warning: Deletes all data
docker-compose up -d
```

**Problem: Port already in use**
```bash
# Check what's using port 8000
sudo lsof -i :8000

# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use different external port
```

### Frontend Issues

**Problem: WebSocket connection failed**
- Check backend is running: `curl http://localhost:8000/api/health`
- Verify WebSocket URL in frontend configuration
- Check browser console for errors

**Problem: Blank page**
```bash
# Rebuild frontend
cd frontend
rm -rf dist node_modules
npm install
npm run build
```

### Network Issues

**Problem: Network auto-detection fails**
- Ensure `NET_ADMIN` capability is granted
- Check network interfaces: `ip addr show`
- Verify routing table: `ip route show`

**Problem: Can't detect SSID**
- Install wireless-tools: `sudo apt install wireless-tools`
- Check wireless interface: `iwconfig`

### Docker Issues

**Problem: Container keeps restarting**
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Restart with fresh state
docker-compose down -v
docker-compose up -d
```

**Problem: Out of disk space**
```bash
# Clean Docker
docker system prune -a
docker volume prune
```

## Performance Optimization

### Backend Optimization

1. **Increase workers:**
```bash
uvicorn api.main:app --workers 4
```

2. **Enable caching:**
```python
# Add to backend/api/main.py
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
```

3. **Database optimization:**
```python
# Use connection pooling
# Add indexes to frequently queried columns
```

### Frontend Optimization

1. **Enable production build:**
```bash
npm run build
```

2. **Enable compression in nginx:**
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

3. **Enable caching:**
```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## Security Considerations

1. **Change default ports in production**
2. **Enable HTTPS with SSL certificates**
3. **Configure firewall rules**
4. **Use environment variables for secrets**
5. **Regular security updates**
6. **Limit CORS origins in production**

## Monitoring and Logs

### View Logs

```bash
# Docker logs
docker-compose logs -f

# Systemd logs
sudo journalctl -u ddosgotchi -f

# Application logs
tail -f data/logs/*.log
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/api/health

# Frontend
curl http://localhost:3000

# WebSocket
wscat -c ws://localhost:8000/ws/realtime
```

## Backup and Recovery

### Backup Database

```bash
# Backup
cp data/ddosgotchi.db data/ddosgotchi.db.backup

# Restore
cp data/ddosgotchi.db.backup data/ddosgotchi.db
```

### Export Data

```bash
# Use API endpoint
curl http://localhost:8000/api/stats/history?limit=1000 > stats.json
curl http://localhost:8000/api/attacks/recent?hours=168 > attacks.json
```

## Support

For issues and support:
- GitHub Issues: https://github.com/yourusername/DDoSGotchi/issues
- Documentation: https://github.com/yourusername/DDoSGotchi/wiki

## License

MIT License - See LICENSE file for details.
