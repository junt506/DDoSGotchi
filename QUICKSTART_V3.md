# 🚀 Quick Start Guide - DDoS Gotchi v3.0

You're currently on the `main` branch, but the v3.0 code is on the feature branch.

## Option 1: Switch to Feature Branch (Recommended)

```bash
git checkout claude/ddos-detection-system-011CUv8M9TmW9oU946yKmdaX
./setup.sh
./start-dev.sh
```

## Option 2: Merge to Main (if you want v3.0 on main)

```bash
git merge claude/ddos-detection-system-011CUv8M9TmW9oU946yKmdaX
./setup.sh
./start-dev.sh
```

## Installation Steps

### 1. Switch to the v3.0 branch
```bash
git checkout claude/ddos-detection-system-011CUv8M9TmW9oU946yKmdaX
```

### 2. Run the setup script
```bash
./setup.sh
```

This will:
- Check Python 3.8+ is installed
- Check Node.js is installed
- Install backend dependencies in a virtual environment
- Install frontend dependencies
- Create necessary directories

### 3. Start the application
```bash
./start-dev.sh
```

This will start:
- Backend on http://localhost:8000
- Frontend on http://localhost:5173 (Vite dev server)

### 4. Open your browser
```
http://localhost:5173
```

## What If I Don't Have Node.js?

Install Node.js:

**Ubuntu/Debian:**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Fedora:**
```bash
sudo dnf install nodejs
```

**Or use nvm:**
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
```

## Manual Setup (if scripts don't work)

### Backend:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (in a new terminal):
```bash
cd frontend
npm install
npm run dev
```

## Troubleshooting

### "Command not found: git"
```bash
# Ubuntu/Debian
sudo apt install git

# Fedora
sudo dnf install git
```

### "Permission denied"
```bash
chmod +x setup.sh
chmod +x start-dev.sh
```

### "Module not found" errors
```bash
cd backend
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## What You'll See

Once everything is running, you'll have:

1. **Backend API** at http://localhost:8000
   - Interactive docs at http://localhost:8000/docs
   - Health check at http://localhost:8000/api/health

2. **Frontend Dashboard** at http://localhost:5173
   - Modern glassmorphism UI
   - Real-time animated graphs
   - Animated Gotchi pet
   - Network statistics

## System Requirements

- **OS**: Linux (Fedora, Ubuntu, or any modern distro)
- **Python**: 3.8 or higher
- **Node.js**: 16 or higher
- **RAM**: 2GB+ recommended
- **Disk**: 500MB for dependencies

## Need Help?

Check the comprehensive documentation:
- `README_V3.md` - Full v3.0 documentation
- `API.md` - API reference
- `DEPLOYMENT.md` - Deployment guide

---

**Note**: The v3.0 code with the modern React frontend is on the feature branch, not main. Make sure to switch branches first!
