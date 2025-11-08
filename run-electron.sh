#!/bin/bash

# DDoS Gotchi v3.0 - Electron Launcher
# This script starts the Python backend and Electron frontend

set -e

echo "🛡️  DDoS Gotchi v3.0 - Electron Edition"
echo "========================================"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3 and try again"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python 3 found"

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
    echo -e "${YELLOW}⚠${NC}  Missing Python dependencies"
    echo "Installing Python dependencies..."
    pip3 install -r requirements-electron.txt --user
fi

if ! python3 -c "import websockets" 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC}  Installing websockets..."
    pip3 install websockets --user
fi

echo -e "${GREEN}✓${NC} Python dependencies OK"
echo ""

# Check and install Electron dependencies
echo "Checking Electron dependencies..."
cd electron

if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠${NC}  Installing Electron dependencies (this may take a minute)..."
    npm install
    echo -e "${GREEN}✓${NC} Electron dependencies installed"
else
    echo -e "${GREEN}✓${NC} Electron dependencies OK"
fi

cd ..
echo ""

# Start Python backend in background
echo "Starting Python backend..."
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
echo "Starting Electron app..."
cd electron
npm start

# Cleanup: Kill backend when Electron exits
echo ""
echo "Shutting down..."
kill $BACKEND_PID 2>/dev/null || true
echo "Backend stopped"
echo "Goodbye! 👋"
