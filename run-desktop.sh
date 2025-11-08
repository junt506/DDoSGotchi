#!/bin/bash
# Quick launcher for DDoS Gotchi Desktop

echo "🚀 Starting DDoS Gotchi Desktop..."

# Check if dependencies are installed
if ! python3 -c "import netifaces, psutil, matplotlib, tkinter" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements-desktop.txt
fi

# Run the desktop app
python3 ddos_gotchi_desktop.py
