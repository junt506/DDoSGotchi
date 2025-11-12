# DDoS Gotchi v3.0 🛡️

**Real-time DDoS detection and network threat analysis with Pwnagotchi-style charm**

A powerful security monitoring tool that combines DDoS detection, threat intelligence, and stunning 3D visualization in a retro-futuristic interface. Perfect for honeypots, security research, and network analysis.

![Version](https://img.shields.io/badge/version-3.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Python](https://img.shields.io/badge/python-3.7+-blue)
![Node](https://img.shields.io/badge/node-16+-green)

## 🌟 Highlights

- 🎯 **Real-time Threat Intelligence** - Identify malicious IPs using AbuseIPDB & GreyNoise
- 🎨 **Stunning 3D Visualization** - 28,000 particle harmonic sphere that reacts to attacks
- 🛡️ **Honeypot-Ready** - Detection-only mode (no blocking) for security research
- 📊 **Comprehensive Monitoring** - Connections, protocols, geo-IP, port analysis
- 🎮 **Pwnagotchi Interface** - Animated faces and witty status messages
- 🔔 **Smart Alerts** - Desktop notifications and sound alerts for threats
- 🌍 **Cross-Platform** - Windows, macOS, Linux (Ubuntu, Fedora, etc.)

## 🖼️ Screenshots

> *Coming soon - DDoS Gotchi in action!*

## ✨ Key Features

### 🛡️ Threat Intelligence

- **Malicious IP Detection** - Real-time identification of known attackers
- **AbuseIPDB Integration** - Community-driven abuse database (1000 free checks/day)
- **GreyNoise Support** - Scanner and malicious actor detection (optional)
- **Confidence Scoring** - 0-100% threat confidence with source attribution
- **Visual Indicators** - 💀 MALICIOUS and ⚠️ SUSPICIOUS badges on IPs
- **Detailed Reports** - Click any IP for full threat intelligence breakdown

### 🎨 3D Visualization

- **28,000 Particle Harmonic Sphere** - Mathematically generated 3D visualization
- **Real-time Color Changes** - Green (normal) → Red (attack)
- **Attack Mode Animations** - 8x faster rotation during DDoS attacks
- **Trail System** - 10,000 particle data flow effects
- **Post-Processing** - Bloom and distortion effects for sci-fi aesthetic

### 📊 Network Monitoring

- **Live Connection Tracking** - All active connections with IP details
- **Protocol Analysis** - TCP, UDP, ICMP breakdown
- **Port Detection** - Suspicious port highlighting (SSH, RDP, SQL, etc.)
- **Geo-IP Lookup** - Country, region, city, ISP for all public IPs
- **Latency & Packet Loss** - Real-time graphs with 24-hour history
- **Attack Detection** - Multiple threshold-based DDoS detection

### 🎮 Pwnagotchi Interface

- **Animated Faces** - (◕‿‿◕) normal, (╬ಠ益ಠ) attack mode
- **Dynamic Quotes** - Witty status messages that change based on network state
- **Color Schemes** - Classic green, cyberpunk pink, matrix lime
- **Settings Panel** - Customizable thresholds, notifications, sounds

### 🔔 Alerts & Notifications

- **Desktop Notifications** - Native OS notifications for attacks
- **Sound Alerts** - Synthesized audio (800Hz attack, 600Hz all-clear)
- **Rate-Limited** - Smart notification throttling to prevent spam
- **Configurable** - Enable/disable per alert type

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+** - Backend monitoring engine
- **Node.js 16+** - Electron frontend
- **npm** - Package manager for Node.js

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/DDoSGotchi.git
cd DDoSGotchi
```

2. **Install Node.js** (if needed)
```bash
# Ubuntu/Debian
sudo apt-get install nodejs npm

# Fedora
sudo dnf install nodejs npm

# macOS
brew install node

# Windows - Download from https://nodejs.org/
```

3. **Run DDoS Gotchi** (auto-installs all dependencies)
```bash
# Linux/macOS
./run-electron.sh

# Windows
run-electron.bat
```

That's it! The launcher handles all Python and Node.js dependencies automatically.

## 🔬 Lab Mode (For Security Research)

Testing DDoS attacks in an isolated lab? Use **Lab Mode** for sensitive detection:

```bash
# Linux/macOS
./run-electron-lab.sh

# Or set environment variable
LAB_MODE=true ./run-electron.sh
```

**Lab Mode Features:**
- **Ultra-sensitive detection** - Detects attacks from as few as 5 connections/IP
- **All connection states** - Monitors SYN floods, half-open connections, etc.
- **Botnet pattern detection** - Identifies multiple IPs from same subnet
- **Traffic volume monitoring** - Tracks bytes/sec and packets/sec
- **Enhanced logging** - Detailed attack information in console

**Perfect for:**
- Testing Mirai botnet variants in airgapped labs
- Low-volume attack simulation (6-10 Raspberry Pi botnets)
- Honeypot deployments with limited traffic
- Security research in controlled environments

📖 **See [LAB_MODE.md](LAB_MODE.md) for complete documentation**

## 🔑 Threat Intelligence Setup (Optional)

DDoS Gotchi works without API keys, but you'll get enhanced threat detection with them:

### AbuseIPDB (Recommended)

1. Get your free API key: https://www.abuseipdb.com/account/api
2. Free tier: **1000 checks/day**
3. Set the environment variable:

```bash
# Linux/macOS
export ABUSEIPDB_API_KEY="your_key_here"
./run-electron.sh

# Windows
set ABUSEIPDB_API_KEY=your_key_here
run-electron.bat
```

### GreyNoise (Optional)

GreyNoise is **disabled by default** due to strict rate limits. To enable:

```bash
export ENABLE_GREYNOISE=true
export ABUSEIPDB_API_KEY="your_key_here"
./run-electron.sh
```

**Note:** GreyNoise Community API has limited free tier. Only enable if needed.

## 📖 Usage

### Understanding the Interface

**Left Panel - Network Status:**
- Network configuration (IP, gateway, network)
- Total connections and unique IPs
- **Threats Detected** counter (turns red when threats found)
- Latency and packet loss metrics
- Protocol distribution pie chart

**Center - 3D Visualization:**
- Green harmonic sphere = Normal operation
- Red sphere spinning fast = DDoS attack detected!
- Click and drag to rotate the view

**Right Panel - Active Connections:**
- Live list of all unique IPs connecting to you
- **💀 MALICIOUS** badges = Known bad actors (high confidence)
- **⚠️ SUSPICIOUS** badges = Potentially malicious (medium confidence)
- Click any IP to see full details (geo, ports, threats)

**Bottom Graphs:**
- Real-time latency and packet loss over time
- 2-minute rolling window

### Testing Attack Mode

Want to see the attack visualization? Use the included traffic simulator:

```bash
# In another terminal
python3 test_attack.py medium
```

The blob will turn red and spin like crazy! 🔴

### Keyboard Shortcuts

- **Ctrl/Cmd + ,** - Open settings panel
- **Ctrl/Cmd + Shift + C** - Cycle color themes
- **Ctrl/Cmd + W** - Close app

## 🎨 Customization

### Color Schemes

Three built-in themes available in settings:
- **Classic** - Retro green terminal (default)
- **Cyberpunk** - Hot pink futuristic
- **Matrix** - Bright lime green

### Detection Thresholds

Customize in the settings panel (⚙️):
- Connection count thresholds (warning: 50, attack: 100)
- Latency thresholds (warning: 50ms, attack: 200ms)
- Packet loss thresholds (warning: 5%, attack: 20%)
- Update interval (default: 1 second)

### Notifications

- Desktop notifications (on/off)
- Sound alerts (on/off)
- Alert frequency (rate-limited to prevent spam)

## 🍯 Honeypot Deployment

DDoS Gotchi is perfect for honeypot use:

1. **Detection-only** - Never blocks traffic, only analyzes
2. **Threat attribution** - Identifies attackers via threat intelligence
3. **Pattern analysis** - Track attack sources and methods
4. **Data visualization** - See attacks as they happen in 3D

**Deployment tips:**
- Deploy on a dedicated monitoring machine
- Configure firewall to allow all incoming (for analysis)
- Use AbuseIPDB for threat attribution
- Monitor the "Threats Detected" counter
- Export connection logs for forensic analysis

## 🛠️ Advanced Configuration

### Environment Variables

```bash
# Threat Intelligence
export ABUSEIPDB_API_KEY="your_key_here"        # Enable AbuseIPDB
export ENABLE_GREYNOISE=true                    # Enable GreyNoise (optional)

# Run the app
./run-electron.sh
```

### Manual Installation

If you prefer manual setup:

```bash
# Install Python dependencies
pip3 install -r requirements-electron.txt

# Install Node.js dependencies
cd electron
npm install
cd ..

# Start backend
python3 backend_electron.py &

# Start frontend
cd electron && npm start
```

## 🐛 Troubleshooting

### Port 8765 Already in Use

```bash
# Kill the old backend process
pkill -f backend_electron.py

# Or find and kill manually
ps aux | grep backend_electron.py
kill <PID>
```

### Dependencies Not Installing

```bash
# Manually install Python deps
pip3 install -r requirements-electron.txt

# Manually install Node deps
cd electron && npm install
```

### No Threats Detected

- Make sure AbuseIPDB API key is set correctly
- Check "Threat Intelligence Status" in console output
- Most normal connections are benign (this is expected!)
- Try the test attack script to see detection in action

### Graphs Not Showing

- Check browser console for errors (Ctrl+Shift+I in Electron)
- Verify backend is running (check console output)
- Try refreshing the app (Ctrl+R)

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🤝 Contributing

Contributions welcome! This is a security research and educational tool.

**Ideas for contributions:**
- Additional threat intelligence sources
- Data export functionality (CSV, JSON)
- Historical threat tracking
- More visualization modes
- Performance optimizations

## ⚠️ Disclaimer

DDoS Gotchi is a **security monitoring and analysis tool** for:
- Network security research
- Honeypot deployments
- DDoS attack detection and analysis
- Educational purposes

**Not intended for:**
- Offensive security operations
- Automated blocking/filtering (detection-only)
- Production network protection (use a real IDS/IPS)

Use responsibly and only on networks you own or have permission to monitor.

## 🙏 Credits

- **Pwnagotchi** - Inspiration for the interface style
- **Three.js** - 3D visualization engine
- **AbuseIPDB** - Threat intelligence data
- **GreyNoise** - Scanner detection

## 📚 Documentation

- [Threat Intelligence Guide](THREAT_INTELLIGENCE.md) - Detailed threat intelligence setup
- [Architecture Overview](docs/ARCHITECTURE.md) - How it all works (coming soon)

## 🔗 Links

- **Report Issues:** https://github.com/yourusername/DDoSGotchi/issues
- **AbuseIPDB:** https://www.abuseipdb.com/
- **GreyNoise:** https://greynoise.io/

---

Made with 💚 for the security research community

**Stay safe, monitor smart!** 🛡️
