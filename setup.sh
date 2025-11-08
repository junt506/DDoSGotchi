#!/bin/bash
#
# DDoS Gotchi - Simple Setup (No Docker Required)
# Works on Fedora and Ubuntu
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════╗"
echo "║   DDoS Gotchi v3.0 - Simple Setup    ║"
echo "╚═══════════════════════════════════════╝"
echo -e "${NC}"

# Check Python version
echo -e "${YELLOW}🔍 Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}❌ Python 3.8+ is required (you have $PYTHON_VERSION)${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"

# Check Node.js
echo -e "${YELLOW}🔍 Checking Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    echo "Install Node.js from: https://nodejs.org/"
    exit 1
fi
NODE_VERSION=$(node --version)
echo -e "${GREEN}✅ Node.js $NODE_VERSION found${NC}"

# Install backend dependencies
echo -e "\n${YELLOW}📦 Installing backend dependencies...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt

echo -e "${GREEN}✅ Backend dependencies installed${NC}"
cd ..

# Install frontend dependencies
echo -e "\n${YELLOW}📦 Installing frontend dependencies...${NC}"
cd frontend

if [ ! -d "node_modules" ]; then
    npm install
else
    echo "Node modules already installed"
fi

echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
cd ..

# Create data directory
mkdir -p data

echo -e "\n${GREEN}✅ Setup complete!${NC}\n"
echo -e "To start DDoS Gotchi:"
echo -e "  ${CYAN}./start-dev.sh${NC}   - Start both backend and frontend"
echo -e "\nOr run manually:"
echo -e "  ${CYAN}Terminal 1:${NC}"
echo -e "    cd backend && source venv/bin/activate"
echo -e "    uvicorn api.main:app --reload --host 0.0.0.0 --port 8000"
echo -e "  ${CYAN}Terminal 2:${NC}"
echo -e "    cd frontend && npm run dev"
echo -e "\nThen open: ${GREEN}http://localhost:5173${NC}\n"
