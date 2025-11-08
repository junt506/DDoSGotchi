# DDoS Gotchi 🛡️

**Real-time DDoS detection with a retro Pwnagotchi-style interface**

A desktop application that monitors your network for DDoS attacks, featuring a cute Pwnagotchi character, real-time graphs, and live connection logging.

![Version](https://img.shields.io/badge/version-3.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🎯 Two Versions Available

### 🖥️ Electron Version (Recommended) - **NEW!**
- **Retro CRT terminal aesthetic** with green phosphor glow effect
- **3D rotating wireframe sphere** animation
- **Modern web technologies** wrapped in a native desktop app
- **Scanline effects** and vintage monitor look
- Same powerful DDoS detection as desktop version

**Launch:** `./run-electron.sh`

### 🐍 Desktop Version (Python/Tkinter)
- **Classic desktop GUI** with Tkinter
- **Matplotlib graphs** for metrics
- **Lightweight** - pure Python implementation

**Launch:** `./run-desktop.sh`

## ✨ Features

### 🎮 Pwnagotchi Interface
- **Animated Pwnagotchi faces** - (◕‿‿◕) changes expression based on network state
- **Random quotes** - Pwnagotchi-style status messages that update every 5 seconds
- **Attack modes** - Face changes to (╬ಠ益ಠ) when under attack

### 📊 Real-Time Monitoring
- **Live graphs** - Latency and packet loss visualization using matplotlib
- **Network stats** - Gateway, IP address, latency, packet loss
- **Attack detection** - Identifies DDoS patterns (ICMP flood, SYN flood, UDP flood, etc.)

### 🌐 Connection Logging
- **All IPs** - Shows every connection to your machine (both local and public)
- **Local network highlight** - Local IPs (192.168.x.x) shown in cyan
- **Auto-refresh** - Logs clear every 15 seconds to catch new connections
- **Connection count** - Shows total active connections periodically

### 🎨 Retro Terminal Aesthetic
- **Black & green theme** - Classic terminal colors
- **Monospace fonts** - Courier New for that retro feel
- **ASCII borders** - Clean retro UI elements

## 🚀 Quick Start

### Electron Version (Recommended)

**Prerequisites:**
- Python 3.7+
- Node.js 16+ and npm
- Linux, macOS, or Windows

**Installation:**

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/DDoSGotchi.git
cd DDoSGotchi
```

2. **Install Node.js** (if not already installed)
```bash
# Fedora
sudo dnf install nodejs npm

# Ubuntu/Debian
sudo apt-get install nodejs npm

# macOS
brew install node
```

3. **Run the launcher** (auto-installs all dependencies)
```bash
./run-electron.sh
```

The launcher will:
- Install Python dependencies (psutil, netifaces, websockets)
- Install Electron and Three.js via npm
- Start the Python backend server
- Launch the Electron app with the retro CRT interface

**Manual installation:**
```bash
# Install Python dependencies
pip3 install -r requirements-electron.txt

# Install Electron dependencies
cd electron && npm install && cd ..

# Start backend
python3 backend_electron.py &

# Start Electron app
cd electron && npm start
```

---

### Desktop Version (Python/Tkinter)

**Prerequisites:**

**System Packages** (required for graphs):
```bash
# Fedora
sudo dnf install python3-tkinter python3-pillow-tk

# Ubuntu/Debian
sudo apt-get install python3-tk python3-pil.imagetk

# macOS
# tkinter comes with Python - no additional packages needed
```

**Installation:**

1. **Clone the repository** (if not already done)
```bash
git clone https://github.com/yourusername/DDoSGotchi.git
cd DDoSGotchi
```

2. **Run the launcher** (auto-installs dependencies)
```bash
./run-desktop.sh
```

Or install manually:
```bash
pip3 install -r requirements-desktop.txt
python3 ddos_gotchi_desktop.py
```

## 📖 How It Works

### Attack Detection

DDoS Gotchi monitors your network for:
- **High latency** - Sustained latency > 100ms
- **Packet loss** - Packet loss > 5%
- **Anomalous patterns** - Traffic compared to baseline

When an attack is detected:
```
STATUS:        🚨 UNDER ATTACK
ATTACK TYPE:   ICMP Flood / Network Saturation
CONFIDENCE:    85%
```

### Connection Logging

The live log shows all network activity:
```
[14:30:45] System initialized
[14:30:45] Monitoring all network connections...
[14:30:47] → LOCAL 192.168.0.100:54321 → :443
[14:30:48] → 142.250.185.46:443 → :54322
[14:30:49] → 52.109.88.123:443 → :54323
[14:31:00] --- 12 active connections ---
```

- **LOCAL** prefix = connections from your local network (highlighted in cyan)
- **No prefix** = public IP connections

### Pwnagotchi Quotes

**Normal state:**
- "monitoring packets..."
- "sniffing networks..."
- "analyzing traffic..."
- "all systems operational"

**Under attack:**
- "ATTACK DETECTED!"
- "network under siege!"
- "defensive mode activated"
- "threat level: HIGH"

## 🎯 What You'll See

### Electron Version (Retro CRT Terminal)

```
████████████████████████████████████████████████████
█                                                  █
█    [3D Rotating Wireframe Sphere Animation]     █
█                                                  █
█              (◕‿‿◕)                              █
█                                                  █
█         "monitoring packets..."                  █
█                                                  █
█    ════════════════════════════════════════     █
█                                                  █
█    [ NETWORK STATUS ]                            █
█                                                  █
█    Connections:      12                          █
█    Unique IPs:       8                           █
█    Latency:          1.2ms                       █
█    Packet Loss:      0%                          █
█    Threat Level:     NORMAL                      █
█                                                  █
█    ════════════════════════════════════════     █
█                                                  █
█    [ LIVE CONNECTION LOG ]                       █
█                                                  █
█    → LOCAL 192.168.0.100:54321 → :443           █
█    → PUBLIC 142.250.185.46:443 → :54322         █
█    → PUBLIC 52.109.88.123:443 → :54323          █
█                                                  █
█    ════════════════════════════════════════     █
█                                                  █
█    [ NETWORK METRICS ]                           █
█                                                  █
█    [Real-time Latency & Packet Loss Graph]      █
█                                                  █
█    ════════════════════════════════════════     █
█                                                  █
█    [► monitoring active]  [⛶ fullscreen]        █
█                                                  █
████████████████████████████████████████████████████
```

**Visual Features:**
- Green phosphor glow effect (like old CRT monitors)
- Scanline overlay for authentic retro feel
- VT323 monospace font
- Text shadow and blur effects
- 3D wireframe sphere rotating in real-time
- Fullscreen mode (click anywhere or press button)

---

### Desktop Version (Python/Tkinter)

```
┌─────────────────────────────────────────────┐
│  ║▌│█║▌│ DDoS GOTCHI v3.0 │▌║█│▌║           │
├─────────────────────────────────────────────┤
│  PWNAGOTCHI      │  >>> NETWORK STATUS      │
│                  │  STATUS:        ✓ NORMAL │
│    (◕‿‿◕)        │  GATEWAY:       192.168.0.1 │
│                  │  LATENCY:       1.2 ms   │
│ monitoring...    │  PACKET LOSS:   0.0 %    │
├─────────────────────────────────────────────┤
│  >>> REAL-TIME METRICS (LIVE GRAPHS)        │
│  [Latency Graph]     [Packet Loss Graph]    │
├─────────────────────────────────────────────┤
│  >>> LIVE CONNECTION LOG                    │
│  [14:30:47] → LOCAL 192.168.0.100:54321     │
│  [14:30:48] → 142.250.185.46:443            │
│  [14:30:49] → 52.109.88.123:443             │
└─────────────────────────────────────────────┘
```

## 🔧 Architecture

### Electron Version

**Frontend (electron/):**
- **`main.js`** - Electron main process (window management)
- **`index.html`** - CRT-styled UI layout
- **`style.css`** - Retro terminal styling with glow effects
- **`renderer.js`** - Frontend logic
  - Three.js 3D wireframe sphere
  - WebSocket client for real-time data
  - Graph rendering on canvas
  - Connection log display

**Backend:**
- **`backend_electron.py`** - WebSocket server
  - Real-time network monitoring with psutil
  - DDoS attack detection
  - Latency and packet loss measurement
  - WebSocket broadcasting to Electron frontend

**Communication:**
- WebSocket connection on `ws://localhost:8765`
- JSON data format
- Updates every 1 second
- Auto-reconnection on disconnect

---

### Desktop Version

**Backend Components:**

- **`backend/core/network_monitor.py`** - Network monitoring with background thread
  - Socket-based latency measurement (no ping required)
  - TCP connection testing for packet loss
  - Thread-safe caching for non-blocking access

- **`backend/core/attack_detector.py`** - DDoS detection engine
  - Baseline comparison
  - Anomaly scoring
  - Attack classification (ICMP, SYN, UDP floods)

- **`backend/core/network_watcher.py`** - Network change detection
  - Monitors for network switches
  - Auto-reconfiguration

**Desktop App:**

- **`ddos_gotchi_desktop.py`** - Main GUI application
  - Tkinter-based interface
  - Matplotlib graphs
  - Real-time connection logging using psutil

## 📋 Requirements

### Electron Version

**Node.js:**
- Node.js 16+
- npm (comes with Node.js)

**Python Packages:**
- `netifaces>=0.11.0` - Network interface detection
- `psutil>=5.9.0` - System monitoring & connections
- `websockets>=12.0` - WebSocket server for frontend communication

**JavaScript Packages** (auto-installed):
- `electron` - Desktop app framework
- `three` - 3D graphics library

---

### Desktop Version

**Python Packages:**
- `netifaces>=0.11.0` - Network interface detection
- `psutil>=5.9.0` - System monitoring & connections
- `matplotlib>=3.5.0` - Real-time graphs

**System Packages:**
- `python3-tkinter` - GUI framework
- `python3-pillow-tk` - Image support for matplotlib

## 🐛 Troubleshooting

### Electron Version

**"Cannot connect to backend" / WebSocket errors?**
```bash
# Make sure backend is running
python3 backend_electron.py

# Check if port 8765 is available
netstat -tuln | grep 8765

# Try restarting both processes
./run-electron.sh
```

**"Node.js not found" / "npm not found"?**
```bash
# Fedora
sudo dnf install nodejs npm

# Ubuntu/Debian
sudo apt-get install nodejs npm

# macOS
brew install node

# Verify installation
node --version
npm --version
```

**Electron app crashes or won't start?**
```bash
# Reinstall Electron dependencies
cd electron
rm -rf node_modules package-lock.json
npm install
cd ..

# Try again
./run-electron.sh
```

**No data showing in the app?**
- Backend might not be running - check terminal output
- Firewall might be blocking localhost:8765
- Try running backend manually: `python3 backend_electron.py`

---

### Desktop Version

**Graphs not showing?**
```bash
# Install matplotlib support
pip3 install matplotlib

# Install system packages (Fedora)
sudo dnf install python3-tkinter python3-pillow-tk

# Install system packages (Ubuntu/Debian)
sudo apt-get install python3-tk python3-pil.imagetk
```

**No connections in log?**
- Run with sudo/admin privileges to see all connections
- Check firewall settings
- Make sure psutil is installed: `pip3 install psutil`

**Connection log stops updating?**
- It refreshes every 15 seconds (clears seen IPs)
- New connections appear immediately
- Connection count shown every 15 seconds

## 🎨 Pwnagotchi Faces

The app uses different faces based on state:

- `(◕‿‿◕)` - Happy (normal operation)
- `(◕‿◕)✧` - Cool (normal, variant)
- `ヽ(◕‿‿◕)ﾉ` - Excited (normal, variant)
- `(╬ಠ益ಠ)` - Angry (under attack!)

## 📊 Graph Details

**Latency Graph** (Green)
- Shows last 100 data points
- Updates every second
- Auto-scales Y-axis

**Packet Loss Graph** (Red)
- Shows last 100 data points
- 0-100% scale
- Spikes indicate connection issues

## 🔒 Privacy & Security

- **All monitoring is local** - No data sent to external servers
- **Read-only log** - Cannot edit or delete log entries
- **No persistent storage** - Logs cleared on restart

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

## 🙏 Credits

Inspired by [Pwnagotchi](https://github.com/evilsocket/pwnagotchi) - the AI-powered WiFi handshake capture tool

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📞 Support

Having issues? Check:
1. System packages installed (tkinter, pillow-tk)
2. Python packages installed (`pip3 install -r requirements-desktop.txt`)
3. Running with sufficient permissions for connection monitoring

## 🎯 Roadmap

- [ ] Alert notifications for attacks
- [ ] Export attack logs
- [ ] Custom attack thresholds
- [ ] More Pwnagotchi faces and quotes
- [ ] Dark/light theme toggle

---

**Made with ❤️ for network security enthusiasts**
