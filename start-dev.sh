#!/bin/bash
#
# DDoS Gotchi - Development Mode Launcher
# Starts both backend and frontend in development mode
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════╗"
echo "║     DDoS Gotchi - Dev Mode v3.0      ║"
echo "╚═══════════════════════════════════════╝"
echo -e "${NC}"

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

# Install backend dependencies
echo -e "${YELLOW}📦 Installing backend dependencies...${NC}"
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt
cd ..

# Install frontend dependencies
echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
cd ..

# Create data directory
mkdir -p data

echo -e "\n${GREEN}✅ Dependencies installed!${NC}\n"

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down...${NC}"
    kill $(jobs -p) 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend
echo -e "${CYAN}🚀 Starting backend on http://localhost:8000${NC}"
cd backend
source venv/bin/activate
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 3

# Start frontend
echo -e "${CYAN}🚀 Starting frontend on http://localhost:3000${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo -e "\n${GREEN}✅ Development servers running!${NC}"
echo -e "   Frontend: ${CYAN}http://localhost:3000${NC}"
echo -e "   Backend:  ${CYAN}http://localhost:8000${NC}"
echo -e "   API Docs: ${CYAN}http://localhost:8000/docs${NC}"
echo -e "\n${YELLOW}Press Ctrl+C to stop${NC}\n"

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID
