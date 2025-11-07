#!/bin/bash
# DDoS Gotchi Launcher Script

echo "
╔═══════════════════════════════════════╗
║        DDoS GOTCHI LAUNCHER           ║
║     Cyber Security Virtual Pet        ║
╚═══════════════════════════════════════╝
"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python version: $PYTHON_VERSION"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
echo "Checking dependencies..."
pip install -q --upgrade pip

if [ -f "requirements.txt" ]; then
    pip install -q -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "⚠️  requirements.txt not found, installing manually..."
    pip install -q pygame psutil netifaces
fi

# Check if config exists
if [ -f "config.json" ]; then
    echo "✓ Configuration file found"
else
    echo "ℹ️  Using default configuration"
fi

# Launch options
echo ""
echo "Select launch mode:"
echo "1) Normal mode"
echo "2) Debug mode (verbose output)"
echo "3) Fullscreen mode"
echo "4) Test mode (with simulator)"

read -p "Choice [1]: " choice
choice=${choice:-1}

case $choice in
    1)
        echo "Launching DDoS Gotchi..."
        python3 ddos_gotchi.py
        ;;
    2)
        echo "Launching DDoS Gotchi in debug mode..."
        python3 -u ddos_gotchi.py
        ;;
    3)
        echo "Launching DDoS Gotchi in fullscreen..."
        # You would need to modify the main script to support fullscreen flag
        python3 ddos_gotchi.py --fullscreen
        ;;
    4)
        echo "Launching test mode..."
        echo "Start DDoS Gotchi in another terminal, then run:"
        echo "sudo python3 test_simulator.py"
        gnome-terminal -- bash -c "python3 ddos_gotchi.py; exec bash" &
        sleep 3
        sudo python3 test_simulator.py
        ;;
    *)
        echo "Invalid choice, launching normal mode..."
        python3 ddos_gotchi.py
        ;;
esac

# Deactivate virtual environment on exit
deactivate 2>/dev/null

echo ""
echo "DDoS Gotchi has been terminated."
echo "Thanks for playing! 🤖"
