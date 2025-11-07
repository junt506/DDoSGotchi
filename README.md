# DDoS Gotchi 🤖⚡

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey?style=for-the-badge)

**A cybersecurity virtual pet that detects and reacts to DDoS attacks**

Inspired by Pwnagotchi • Cyber-themed • Real-time monitoring

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Configuration](#%EF%B8%8F-configuration)

</div>

---

## 📖 Overview

DDoS Gotchi is a network monitoring tool with personality! It watches your network for signs of DDoS attacks and responds with different moods, ASCII faces, and sassy quotes. Features a beautiful Matrix-inspired rain effect and smooth animations.

Perfect for:
- 🔬 Security research labs
- 🎓 Educational environments
- 🛡️ Network monitoring
- 🎮 Having a cyber-pet companion

## ✨ Features

- **🔍 Real-time Network Monitoring** - Tracks latency, packet loss, and connection stability
- **🚨 DDoS Detection** - Identifies network degradation patterns consistent with attacks
- **😎 5 Dynamic Moods** - ASCII faces change based on network health
- **🌊 Matrix Rain Effect** - Animated cyberpunk-themed background with Japanese characters
- **📊 Live Statistics** - Latency, packet loss, threat levels, and attack counter
- **🎭 Contextual Quotes** - Witty responses to network conditions
- **🔄 Smooth State Transitions** - Intelligent smoothing prevents flickering
- **💻 Cross-platform** - Works on Linux, Windows (with some limitations)

## 🎭 Mood States

| State | Face | Trigger Conditions | Quote Example |
|-------|------|-------------------|---------------|
| **Happy** | `(⌐■_■)` | Latency <10ms, Loss <1% | "Living my best life in the 45.33 subnet" |
| **Alert** | `(⌐■_◉)` | Latency 10-50ms, Loss 1-5% | "Hold up, detecting anomalies" |
| **Under Attack** | `(✖╭╮✖)` | Latency 50-200ms, Loss 5-20% | "WE'RE GETTING DDOS'D!" |
| **Stressed** | `(⊙﹏⊙)` | Latency >200ms, Loss >20% | "I CAN'T BREATHE!" |
| **Disconnected** | `(×_×)` | No connection | "404: Network not found" |

## 📦 Installation

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- Active network connection

### Quick Setup

```bash
# 1. Clone the repository
git clone https://github.com/junt506/DDoSGotchi.git
cd DDoSGotchi

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run DDoS Gotchi
python3 ddos_gotchi.py
```

### Platform-Specific Installation

<details>
<summary><b>Ubuntu/Debian</b></summary>

```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv wireless-tools iproute2

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Run the program
python3 ddos_gotchi.py
```
</details>

<details>
<summary><b>Fedora/RHEL</b></summary>

```bash
# Install system dependencies
sudo dnf install python3 python3-pip wireless-tools iproute

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Run the program
python3 ddos_gotchi.py
```
</details>

<details>
<summary><b>Windows</b></summary>

```powershell
# Install Python from https://www.python.org/downloads/
# Make sure to check "Add Python to PATH" during installation

# Install dependencies
pip install -r requirements.txt

# Run the program
python ddos_gotchi.py
```

**Note:** SSID detection and the test simulator require Linux. Basic monitoring works on Windows.
</details>

### Using the Launch Script (Linux)

```bash
chmod +x launch.sh
./launch.sh
```

The launch script provides options for:
1. Normal mode
2. Debug mode (verbose output)
3. Fullscreen mode
4. Test mode (with simulator)

## 🚀 Usage

### Basic Usage

```bash
python3 ddos_gotchi.py
```

### Controls

| Key | Action |
|-----|--------|
| **ESC** | Exit program |
| **SPACE** | Change quote |
| **Close Window** | Exit program |

### What You'll See

The interface displays:
- 🌧️ Animated Matrix rain background
- 😎 ASCII art face showing current mood
- 🔗 Connection status indicator
- 📡 Network name (SSID)
- ⏱️ Current latency in milliseconds
- 📦 Packet delivery success rate
- ⚠️ Visual threat level bars
- 💬 Contextual quote bubbles
- ⏰ Runtime and total attacks detected

## 🛠️ Configuration

### Option 1: Edit config.json

The `config.json` file allows easy customization without modifying code:

```json
{
  "network": {
    "target_network": "45.33.0",
    "gateway": "45.33.0.1",
    "target_ssid": "Mirai <3"
  },
  "thresholds": {
    "happy": {
      "max_latency": 10,
      "max_packet_loss": 1
    },
    "alert": {
      "max_latency": 50,
      "max_packet_loss": 5
    },
    "under_attack": {
      "max_latency": 200,
      "max_packet_loss": 20
    }
  },
  "ui": {
    "window_width": 900,
    "window_height": 600,
    "fps": 30,
    "quote_interval_seconds": 15
  }
}
```

### Option 2: Edit ddos_gotchi.py

**Change Network Settings:**

Find line ~627:
```python
self.network_monitor = NetworkMonitor(
    target_network="192.168.1",  # Your network prefix
    gateway="192.168.1.1"         # Your router IP
)
```

**Adjust Detection Thresholds:**

Find line ~370 in `StateManager.determine_state()`:
```python
if latency < 10 and packet_loss < 1:
    new_state = 'happy'
elif latency < 50 and packet_loss < 5:
    new_state = 'alert'
# Adjust these values as needed
```

**Customize Quotes:**

Find line ~63 and modify the `QUOTES` dictionary:
```python
QUOTES = {
    'happy': [
        "Your custom happy quote here",
        "Another quote",
    ],
    # ... other states
}
```

**Change Colors:**

Find line ~28 and modify RGB values:
```python
MATRIX_GREEN = (0, 255, 65)  # Lime green
DARK_GREEN = (0, 128, 32)
RED = (255, 0, 0)
# Add your custom colors
```

## 🧪 Testing Without Real Attacks

### Using the Test Simulator

The `test_simulator.py` script simulates network conditions using Linux traffic control:

```bash
# Terminal 1 - Run DDoS Gotchi
python3 ddos_gotchi.py

# Terminal 2 - Run simulator (requires sudo)
sudo python3 test_simulator.py
```

**Available Scenarios:**
1. Normal Network → Happy face
2. Alert Condition → Alert face
3. Active Attack → Under attack face
4. Severe Attack → Stressed face
5. Progressive Attack → Gradual escalation
6. Fluctuating Conditions → Random changes
7. Complete Cycle → All states in sequence

**Requirements:**
- Linux OS only (uses `tc` command)
- Root/sudo privileges
- `iproute2` package installed

## 🧪 Testing with Mirai Lab

### Lab Setup

This is designed for airgapped security research environments:

```
┌─────────────────────┐         ┌──────────────────────┐
│  Attacker Network   │         │   Victim Network     │
│   203.0.113.0/24    │────X────│   45.33.0.0/24       │
│  (Mirai CNC/Botnet) │ Airgap  │  (IoT Devices/WiFi)  │
└─────────────────────┘         └──────────────────────┘
                                          │
                                  ┌───────▼────────┐
                                  │  DDoS Gotchi   │
                                  │ (Ubuntu Laptop) │
                                  └────────────────┘
```

### Testing Workflow

1. **Connect** - Join the victim network WiFi (45.33.0.0/24)
2. **Launch DDoS Gotchi** - Start monitoring
3. **Execute Attack** - Launch Mirai DDoS from CNC
4. **Observe** - Watch gotchi react to network degradation
5. **Stop Attack** - Watch recovery transition

### Expected Behavior

```
Normal → Alert → Under Attack → Stressed
  ↑                                 ↓
  └────────── Recovery ←────────────┘
```

- **Before Attack**: Happy face, <10ms latency, stable connection
- **Early Attack**: Alert face, 10-50ms latency, minor packet loss
- **Active Attack**: Under attack face, 50-200ms latency, glitch effects
- **Severe Attack**: Stressed face, >200ms latency, heavy packet loss
- **Recovery**: Gradual transition back through states

## 📁 Project Structure

```
DDoSGotchi/
├── ddos_gotchi.py       # Main application
├── test_simulator.py    # Network condition simulator (Linux only)
├── requirements.txt     # Python dependencies
├── config.json          # Configuration file
├── launch.sh           # Launcher script (Linux)
├── QUICKSTART.md       # Quick reference guide
└── README.md           # This file
```

## 🔍 How It Works

### Architecture

```
┌─────────────────────────────────────────┐
│         Background Thread               │
│  ┌───────────────────────────────────┐  │
│  │  Network Monitor                  │  │
│  │  • Ping gateway every 2 seconds   │  │
│  │  • Measure latency                │  │
│  │  • Calculate packet loss          │  │
│  │  • Update stats dictionary        │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│            Main Thread                  │
│  ┌───────────────────────────────────┐  │
│  │  State Manager                    │  │
│  │  • Read stats from monitor        │  │
│  │  • Determine current state        │  │
│  │  • Apply smoothing algorithm      │  │
│  │  • Select appropriate quote       │  │
│  └───────────────────────────────────┘  │
│                 │                        │
│                 ▼                        │
│  ┌───────────────────────────────────┐  │
│  │  Cyber UI Renderer                │  │
│  │  • Matrix rain animation          │  │
│  │  • Draw ASCII face                │  │
│  │  • Display statistics             │  │
│  │  • Render threat levels           │  │
│  │  • Show quotes                    │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Key Components

**NetworkMonitor** (`ddos_gotchi.py:174-345`)
- Detects WiFi interface automatically
- Pings gateway using subprocess
- Parses ping output with regex
- Maintains rolling history (10 samples)
- Handles cross-platform differences

**StateManager** (`ddos_gotchi.py:348-412`)
- Analyzes network metrics
- Compares against thresholds
- Uses state history for smoothing (5 samples)
- Prevents rapid flickering
- Manages quote rotation

**CyberUI** (`ddos_gotchi.py:415-603`)
- Renders Matrix rain effect
- Draws ASCII faces with animations
- Shows color-coded statistics
- Creates threat level bars
- Handles visual effects (glitch, scanlines, blinking)

**MatrixRain** (`ddos_gotchi.py:121-171`)
- Generates falling characters (Japanese + ASCII)
- Implements fade effect
- Randomizes character positions
- Creates authentic Matrix aesthetic

## 🐛 Troubleshooting

### Common Issues

<details>
<summary><b>"No network detected"</b></summary>

**Causes:**
- Not connected to WiFi
- Incorrect gateway IP
- Firewall blocking ping

**Solutions:**
```bash
# Check connection
ip addr show
ping 45.33.0.1

# Edit gateway in config.json
nano config.json

# Allow ICMP (if firewall blocks)
sudo iptables -A INPUT -p icmp -j ACCEPT
sudo iptables -A OUTPUT -p icmp -j ACCEPT
```
</details>

<details>
<summary><b>"No module named 'pygame'"</b></summary>

```bash
pip install pygame psutil netifaces
# Or with pip3
pip3 install pygame psutil netifaces
```
</details>

<details>
<summary><b>High latency on normal network</b></summary>

Your network might actually be slow, or adjust thresholds:

```python
# In config.json or ddos_gotchi.py line ~370
if latency < 20 and packet_loss < 2:  # More lenient
    new_state = 'happy'
```
</details>

<details>
<summary><b>SSID not showing</b></summary>

This is normal on some systems. The program uses IP-based detection as fallback.

```bash
# Linux: Install wireless tools
sudo apt install wireless-tools

# If still doesn't work, it will show "Network: 45.33.0" instead of SSID
```
</details>

<details>
<summary><b>Permission denied errors</b></summary>

```bash
# Linux/Mac
sudo python3 ddos_gotchi.py

# Windows
# Run Command Prompt as Administrator
```
</details>

<details>
<summary><b>Test simulator not working</b></summary>

The simulator only works on Linux:

```bash
# Install traffic control
sudo apt install iproute2

# Run with sudo
sudo python3 test_simulator.py
```
</details>

## 🎨 Customization Ideas

### Add Sound Effects

```python
# Initialize mixer
pygame.mixer.init()

# Load sounds
alert_sound = pygame.mixer.Sound("alert.wav")
attack_sound = pygame.mixer.Sound("attack.wav")

# Play on state change
if new_state == 'under_attack':
    attack_sound.play()
```

### Advanced Features

- 📧 Email/Discord alerts for attacks
- 📝 Log attacks to file with timestamps
- 📊 Export statistics to JSON/CSV
- 📈 Add graphs for latency over time
- 🌐 Monitor multiple gateways simultaneously
- 🎯 Custom attack pattern signatures
- 🖼️ Additional visual themes
- 🌈 RGB LED integration for physical feedback

## 🔒 Security & Ethics

⚠️ **EDUCATIONAL USE ONLY** ⚠️

This tool is designed **exclusively** for:
- ✅ Authorized security research
- ✅ Educational purposes
- ✅ Controlled lab environments (airgapped)
- ✅ Personal network monitoring
- ✅ CTF competitions
- ✅ DDoS detection research

**Strictly DO NOT:**
- ❌ Use on networks you don't own
- ❌ Launch actual DDoS attacks
- ❌ Monitor networks without permission
- ❌ Deploy for malicious purposes
- ❌ Violate computer fraud laws (CFAA, etc.)

**Legal Notice:** The authors are not responsible for misuse. Users must ensure compliance with all applicable laws and regulations.

## 📚 Learn More

### Understanding DDoS Detection

DDoS Gotchi detects attacks by monitoring:
1. **Latency spikes** - Overwhelmed routers respond slowly
2. **Packet loss** - Congestion causes dropped packets
3. **Connection stability** - Network becomes unreliable

### Detection Algorithm

```python
# Simplified logic
if latency > 200ms OR packet_loss > 20%:
    state = "stressed"  # Severe attack
elif latency > 50ms OR packet_loss > 5%:
    state = "under_attack"  # Active attack
elif latency > 10ms OR packet_loss > 1%:
    state = "alert"  # Degradation detected
else:
    state = "happy"  # All good
```

### Why Smoothing Matters

Without smoothing, a single ping timeout causes rapid state changes. DDoS Gotchi uses:
- **Rolling averages** (10 samples) for metrics
- **State history** (5 samples) for mode calculation
- **Debouncing** to prevent flickering

## 🤝 Contributing

Contributions welcome! Ideas for enhancement:

- 🎨 New themes (steampunk, vaporwave, etc.)
- 😄 Additional facial expressions
- 📊 Better detection algorithms
- 🌐 Multi-network monitoring
- 🔌 Plugin system for extensibility
- 🐳 Docker containerization
- 🎮 Raspberry Pi support with e-ink display

## 📄 License

This project is for **educational purposes only**. Use responsibly and only on networks you own or have explicit permission to monitor.

## 🙏 Acknowledgments

- **[Pwnagotchi](https://pwnagotchi.ai/)** - The original AI-powered WiFi hacking companion
- **[Fancygotchi](https://github.com/V0rtex420/Fancygotchi)** - Beautiful cyber themes and aesthetics
- **Mirai Botnet Research** - Understanding real-world DDoS attack patterns
- **The Matrix** - Visual inspiration for the rain effect

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/junt506/DDoSGotchi/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/junt506/DDoSGotchi/discussions)
- 📖 **Documentation**: See [QUICKSTART.md](QUICKSTART.md)

---

<div align="center">

**Keep your gotchi happy by maintaining a stable network!** 🛡️

*Built with 💚 for the cybersecurity community*

⭐ **Star this repo if you find it useful!** ⭐

</div>
