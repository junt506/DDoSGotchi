#!/bin/bash

# DDoS Gotchi v3.0 - Electron HUD Launcher (LAB MODE)
# This script starts DDoS Gotchi in LAB MODE with sensitive detection
# Perfect for isolated malware testing environments (airgapped labs)

set -e

echo "🔬 DDoS Gotchi v3.0 - LAB MODE Edition"
echo "=============================================="
echo ""
echo "⚠️  LAB MODE - Sensitive Detection Active"
echo "   - Attack threshold: 5 connections/IP"
echo "   - Suspicious threshold: 3 connections/IP"
echo "   - Monitors ALL connection states (SYN floods, half-open, etc.)"
echo "   - Botnet pattern detection enabled"
echo ""
echo "Perfect for testing with low-volume attacks (Mirai botnets, etc.)"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3 and try again"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python 3 found: $(python3 --version)"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    echo "Please install Node.js from: https://nodejs.org/"
    echo ""
    echo "For Fedora: sudo dnf install nodejs npm"
    echo "For Ubuntu: sudo apt-get install nodejs npm"
    echo "For macOS: brew install node"
    exit 1
fi

echo -e "${GREEN}✓${NC} Node.js found: $(node --version)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed${NC}"
    echo "Please install npm and try again"
    exit 1
fi

echo -e "${GREEN}✓${NC} npm found: $(npm --version)"
echo ""

# Check Python dependencies
echo "Checking Python dependencies..."

if ! python3 -c "import psutil" 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC}  Installing Python dependencies..."
    pip3 install -r requirements-electron.txt --user
fi

if ! python3 -c "import websockets" 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC}  Installing websockets..."
    pip3 install websockets --user
fi

if ! python3 -c "import netifaces" 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC}  Installing netifaces..."
    pip3 install netifaces --user
fi

if ! python3 -c "import aiohttp" 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC}  Installing aiohttp..."
    pip3 install aiohttp --user
fi

echo -e "${GREEN}✓${NC} Python dependencies OK"
echo ""

# Check and install Electron dependencies
echo "Checking Electron dependencies..."
cd electron

if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠${NC}  Installing Electron dependencies..."
    echo -e "${BLUE}   This may take a few minutes on first run...${NC}"
    npm install
    echo -e "${GREEN}✓${NC} Electron dependencies installed"
else
    echo -e "${GREEN}✓${NC} Electron dependencies OK"
fi

cd ..
echo ""

# Enable LAB MODE via environment variable
export LAB_MODE=true

# Optional: Disable threat intelligence APIs in isolated lab (they won't work anyway)
# Uncomment these if you don't have internet in your airgapped lab:
# export ENABLE_GREYNOISE=false
# unset ABUSEIPDB_API_KEY

echo -e "${BLUE}🔬 Starting in LAB MODE...${NC}"
echo ""

# Start Python backend in background
echo "Starting Python backend with LAB_MODE=true..."
python3 backend_electron.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 2

# Check if backend is running
if ! ps -p $BACKEND_PID > /dev/null; then
    echo -e "${RED}❌ Failed to start Python backend${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Backend started (PID: $BACKEND_PID)"
echo ""

# Start Electron app
echo -e "${BLUE}Launching Lab Mode HUD Interface...${NC}"
echo ""
cd electron
npm start

# Cleanup: Kill backend when Electron exits
echo ""
echo "Shutting down..."
kill $BACKEND_PID 2>/dev/null || true
echo "Backend stopped"
echo ""
echo -e "${BLUE}Thank you for using DDoS Gotchi LAB MODE! 🔬🛡️${NC}"
echo "Goodbye! 👋"
