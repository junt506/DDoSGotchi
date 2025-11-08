# DDoS Gotchi 🛡️

**Real-time DDoS detection with a retro Pwnagotchi-style interface**

A desktop application that monitors your network for DDoS attacks, featuring a cute Pwnagotchi character, real-time graphs, and live connection logging.

![Version](https://img.shields.io/badge/version-3.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

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

### Prerequisites

**System Packages** (required for graphs):
```bash
# Fedora
sudo dnf install python3-tkinter python3-pillow-tk

# Ubuntu/Debian
sudo apt-get install python3-tk python3-pil.imagetk

# macOS
# tkinter comes with Python - no additional packages needed
```

### Installation

1. **Clone the repository**
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

### Backend Components

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

### Desktop App

- **`ddos_gotchi_desktop.py`** - Main GUI application
  - Tkinter-based interface
  - Matplotlib graphs
  - Real-time connection logging using psutil

## 📋 Requirements

### Python Packages
- `netifaces>=0.11.0` - Network interface detection
- `psutil>=5.9.0` - System monitoring & connections
- `matplotlib>=3.5.0` - Real-time graphs

### System Packages
- `python3-tkinter` - GUI framework
- `python3-pillow-tk` - Image support for matplotlib

## 🐛 Troubleshooting

### Graphs not showing?
```bash
# Install matplotlib support
pip3 install matplotlib

# Install system packages (Fedora)
sudo dnf install python3-tkinter python3-pillow-tk

# Install system packages (Ubuntu/Debian)
sudo apt-get install python3-tk python3-pil.imagetk
```

### No connections in log?
- Run with sudo/admin privileges to see all connections
- Check firewall settings
- Make sure psutil is installed: `pip3 install psutil`

### Connection log stops updating?
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
