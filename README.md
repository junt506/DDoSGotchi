# DDoS Gotchi 🤖⚡ - Advanced Detection System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey?style=for-the-badge)

**An advanced DDoS detection system with virtual pet interface**

Inspired by Pwnagotchi • Cyber-themed • Real-time monitoring • ML-Ready

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Configuration](#%EF%B8%8F-configuration)

</div>

---

## 📖 Overview

DDoS Gotchi is a **production-ready network monitoring and DDoS detection system** with personality! Combining advanced multi-layered detection algorithms with an engaging Matrix-themed interface, it provides real-time network security monitoring in an airgapped lab environment.

**Version 2.0** introduces powerful new features:
- 🧠 **Multi-layered attack detection** with baseline learning
- 📊 **Real-time graphing** of network metrics
- 🔔 **Multi-channel alerting** (Desktop, Discord, Email)
- 📝 **Persistent logging** to JSON/CSV
- 🌐 **Auto-detection** of network configuration
- 📈 **Attack classification** (SYN flood, UDP flood, ICMP flood, etc.)
- 💾 **Historical data** tracking and analysis

Perfect for:
- 🔬 Security research labs analyzing Mirai malware
- 🎓 Educational cybersecurity environments
- 🛡️ Network monitoring and threat detection
- 📊 Network performance analysis
- 🎮 Having an intelligent cyber-pet companion

## ✨ Features

### 🔍 Advanced Detection System

- **Multi-Algorithm Detection**
  - Threshold-based detection with configurable limits
  - Baseline learning (learns normal network behavior)
  - Anomaly score calculation
  - Pattern-based attack classification
  - Confidence scoring for each detection

- **Attack Type Classification**
  - ICMP Flood / Network Saturation
  - UDP Flood Detection
  - SYN Flood / Resource Exhaustion
  - Mixed DDoS Attacks
  - Slow DDoS / Network Congestion

- **Network Intelligence**
  - Auto-detection of gateway and network configuration
  - Multi-gateway monitoring with failover
  - Connection count tracking
  - Port scan detection
  - Traffic pattern analysis

### 📊 Real-Time Visualization

- **Multi-Panel Dashboard** (1280x800 resolution)
  - Gotchi Pet Panel with animated ASCII faces
  - Network Statistics Panel
  - Real-Time Graphs (Latency & Packet Loss)
  - Attack Detection Panel with recent attack history
  - Live IP information (Local + Public)

- **Advanced Graphics**
  - Matrix rain effect background
  - CRT scanlines overlay
  - Real-time line graphs
  - Color-coded statistics
  - Glitch effects during attacks
  - Smooth animations

### 🔔 Multi-Channel Alerting

- **Desktop Notifications** (Linux notify-send)
  - Critical priority alerts
  - Attack type and severity information
  - Configurable cooldown periods

- **Discord Webhook Integration**
  - Rich embed messages
  - Color-coded severity levels
  - Timestamp information
  - Remote monitoring capability

- **Email Alerts** (SMTP)
  - Configurable SMTP server settings
  - Attack notifications
  - Support for TLS/SSL

### 📝 Data Logging & Export

- **Attack Logging**
  - JSON-formatted attack logs
  - Timestamp, type, severity, metrics
  - Historical attack database
  - 24-hour attack history display

- **Statistics Export**
  - CSV export of all network metrics
  - Minute-by-minute data logging
  - State transitions
  - Anomaly scores
  - Connection counts

### 🎭 Dynamic Mood States

| State | Face | Trigger Conditions | Quote Example |
|-------|------|-------------------|---------------|
| **Happy** | `(⌐■_■)` | Latency <10ms, Loss <1% | "Living my best life in this subnet" |
| **Alert** | `(⌐■_◉)` | Latency 10-50ms, Loss 1-5% | "Hold up, detecting anomalies" |
| **Under Attack** | `(✖╭╮✖)` | Latency 50-200ms, Loss 5-20% | "WE'RE GETTING DDOS'D!" |
| **Stressed** | `(⊙﹏⊙)` | Latency >200ms, Loss >20% | "I CAN'T BREATHE!" |
| **Disconnected** | `(×_×)` | No connection | "404: Network not found" |

### 🌐 Network Auto-Detection

- **Automatic Configuration**
  - Gateway auto-detection using netifaces
  - Network prefix auto-detection
  - Interface selection (prioritizes wireless)
  - SSID detection (Linux with iwgetid)
  - Public IP detection via multiple APIs
  - Fallback mechanisms for reliability

## 📦 Installation

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- Active network connection
- **Linux** (Fedora/Ubuntu recommended) or Windows

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
<summary><b>Ubuntu/Debian (Recommended)</b></summary>

```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv wireless-tools iproute2 libnotify-bin

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
<summary><b>Fedora/RHEL (Recommended)</b></summary>

```bash
# Install system dependencies
sudo dnf install python3 python3-pip wireless-tools iproute libnotify

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
# Install Python from python.org if not already installed

# Install dependencies
pip install -r requirements.txt

# Run the program
python ddos_gotchi.py
```

**Note:** Some features (SSID detection, desktop notifications) may not work on Windows.
</details>

### Using the Launch Script (Linux)

```bash
# Make the script executable
chmod +x launch.sh

# Run with interactive menu
./launch.sh

# Or directly:
./launch.sh normal    # Normal mode
./launch.sh debug     # Debug mode with verbose output
./launch.sh test      # Run test simulator (requires sudo)
```

## 🚀 Usage

### Basic Operation

1. **Start the application:**
   ```bash
   python3 ddos_gotchi.py
   ```

2. **Monitor the dashboard:**
   - Watch the Gotchi's mood change based on network conditions
   - View real-time graphs of latency and packet loss
   - Check attack detection panel for alerts
   - Monitor your local and public IP addresses

3. **Keyboard Controls:**
   - `ESC` - Exit the application
   - `SPACE` - Force quote change

### Testing DDoS Detection

**⚠️ WARNING: Only run in isolated lab environments!**

```bash
# Use the built-in test simulator (Linux only, requires sudo)
python3 test_simulator.py

# Select from 7 test scenarios:
# 1. Normal conditions
# 2. Light attack (50ms latency, 5% loss)
# 3. Moderate attack (100ms latency, 10% loss)
# 4. Heavy attack (300ms latency, 30% loss)
# 5. Severe attack (1000ms latency, 50% loss)
# 6. Progressive attack (gradual escalation)
# 7. Fluctuating attack (random spikes)
```

### Monitoring Logs

```bash
# View attack logs
cat logs/attacks.json | jq '.'

# View statistics export
cat logs/stats.csv

# Monitor logs in real-time
tail -f logs/attacks.json
```

## ⚙️ Configuration

All settings are in `config.json` - **fully functional and respected by the application!**

### Network Settings

```json
{
  "network": {
    "target_network": "auto",        // "auto" or specific prefix like "192.168.1"
    "gateway": "auto",               // "auto" or specific IP like "192.168.1.1"
    "target_ssid": "Auto-Detect",
    "ping_count": 5,                 // Packets per loss test
    "ping_interval": 2,              // Seconds between checks
    "additional_gateways": []        // Array of additional gateway IPs to monitor
  }
}
```

**Auto-detection:** Set `"target_network"` and `"gateway"` to `"auto"` to automatically detect your network configuration. This works on **any network**!

### Detection Thresholds

```json
{
  "thresholds": {
    "happy": {
      "max_latency": 10,             // Milliseconds
      "max_packet_loss": 1           // Percentage
    },
    "alert": {
      "max_latency": 50,
      "max_packet_loss": 5
    },
    "under_attack": {
      "max_latency": 200,
      "max_packet_loss": 20
    },
    "stressed": {
      "min_latency": 200,
      "min_packet_loss": 20
    }
  }
}
```

**Customize:** Adjust thresholds based on your network's baseline performance.

### UI Customization

```json
{
  "ui": {
    "window_width": 1280,            // Default: 1280 (can use 1920 for full HD)
    "window_height": 800,            // Default: 800 (can use 1080 for full HD)
    "fps": 30,
    "quote_interval_seconds": 15,
    "matrix_rain_enabled": true,
    "scanlines_enabled": true,
    "blink_animation_enabled": true,
    "glitch_effects_enabled": true
  }
}
```

**Resolution options:**
- `1280x800` - Laptop/default
- `1920x1080` - Full HD desktop
- `2560x1440` - 2K displays

### Alert Configuration

```json
{
  "features": {
    "sound_effects": false,          // Reserved for future sound support
    "log_attacks": true,             // Log attacks to JSON file
    "export_stats": true,            // Export stats to CSV
    "desktop_notifications": true,   // Linux desktop notifications
    "discord_webhooks": false,       // Discord alerts (configure below)
    "email_alerts": false            // Email alerts (configure below)
  },
  "alerts": {
    "discord_webhook_url": "",                    // Your Discord webhook URL
    "email_smtp_server": "smtp.gmail.com",        // SMTP server
    "email_smtp_port": 587,
    "email_from": "your-email@gmail.com",
    "email_password": "your-app-password",
    "email_to": "recipient@example.com",
    "alert_cooldown_seconds": 300                 // 5 minutes between alerts
  }
}
```

#### Setting Up Discord Alerts

1. Create a Discord webhook in your server:
   - Server Settings → Integrations → Webhooks → New Webhook
2. Copy the webhook URL
3. Paste into `config.json`:
   ```json
   {
     "features": {
       "discord_webhooks": true
     },
     "alerts": {
       "discord_webhook_url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
     }
   }
   ```

#### Setting Up Email Alerts

1. Generate an app password (Gmail):
   - Google Account → Security → 2-Step Verification → App passwords
2. Configure in `config.json`:
   ```json
   {
     "features": {
       "email_alerts": true
     },
     "alerts": {
       "email_smtp_server": "smtp.gmail.com",
       "email_smtp_port": 587,
       "email_from": "youremail@gmail.com",
       "email_password": "your-app-password",
       "email_to": "recipient@example.com"
     }
   }
   ```

### Logging Configuration

```json
{
  "logging": {
    "log_directory": "logs",
    "attack_log_file": "attacks.json",
    "stats_export_file": "stats.csv",
    "max_log_size_mb": 100
  }
}
```

### Detection Configuration

```json
{
  "detection": {
    "enable_baseline_learning": true,           // Learn normal network behavior
    "enable_attack_classification": true,       // Classify attack types
    "enable_connection_tracking": true,         // Monitor connection counts
    "suspicious_connection_threshold": 100      // Connections threshold for anomaly
  }
}
```

## 📊 Understanding the Dashboard

### Panel Layout (1280x800)

```
┌─────────────────────────────────────────────────────────────────┐
│              [ DDOS GOTCHI - ADVANCED DETECTION SYSTEM ]        │
│         LOCAL IP: 192.168.1.100  |  PUBLIC IP: 123.45.67.89    │
├────────────────────┬────────────────────────────────────────────┤
│                    │                                            │
│   ┌─────────────┐  │  ┌─────────────────────────────────────┐  │
│   │   GOTCHI    │  │  │     REAL-TIME METRICS               │  │
│   │   (⌐■_■)    │  │  │  ┌───────────────────────────────┐  │  │
│   │             │  │  │  │   LATENCY (ms)                │  │  │
│   │  [ HAPPY ]  │  │  │  │   Graph showing last 60 pts   │  │  │
│   └─────────────┘  │  │  └───────────────────────────────┘  │  │
│                    │  │  ┌───────────────────────────────┐  │  │
│   ┌─────────────┐  │  │  │   PACKET LOSS (%)             │  │  │
│   │  NETWORK    │  │  │  │   Graph showing last 60 pts   │  │  │
│   │ STATISTICS  │  │  │  └───────────────────────────────┘  │  │
│   │             │  │  └─────────────────────────────────────┘  │
│   │ Status: ●   │  │                                            │
│   │ Latency: 5  │  │  ┌─────────────────────────────────────┐  │
│   │ Loss: 0.2%  │  │  │    ATTACK DETECTION                 │  │
│   │ Anomaly: 0  │  │  │                                     │  │
│   └─────────────┘  │  │  STATUS: ✓ NO ATTACK DETECTED       │  │
│                    │  │  RECENT ATTACKS (24h):              │  │
│                    │  │  2025-11-08 14:23 - UDP Flood       │  │
└────────────────────┴──┴─────────────────────────────────────────┤
│         "Living my best life in this subnet"                    │
│  Runtime: 01:23:45  |  Total Attacks: 3  |  ESC=Exit SPACE=... │
└─────────────────────────────────────────────────────────────────┘
```

### Statistics Explained

- **Status:** Connection state (CONNECTED/DISCONNECTED)
- **Network:** SSID or network prefix
- **Gateway:** Router IP being monitored
- **Interface:** Network interface name (e.g., wlan0, eth0)
- **Latency:** Current ping time in milliseconds
- **Avg Latency:** Rolling average of last 10 samples
- **Baseline:** Learned normal latency (median of last 100 samples)
- **Packet Loss:** Percentage of packets lost
- **Connections:** Total active network connections
- **Established:** Active established TCP connections
- **Anomaly Score:** Deviation from baseline (0-100)
- **Confidence:** Detection confidence percentage

### Attack Detection Logic

The system uses **multi-layered detection**:

1. **Threshold-based:** Compares current metrics to configured thresholds
2. **Baseline comparison:** Detects deviation from learned normal behavior
3. **Pattern matching:** Classifies attack type based on signature patterns
4. **Anomaly scoring:** Calculates statistical deviation from baseline

**Attack is detected when:**
- Metrics exceed threshold levels, OR
- Anomaly score is high (>50), AND
- Confidence level is sufficient (>60%)

## 🔧 Advanced Features

### Baseline Learning

The system learns your network's normal behavior:
- Collects first 100 latency/loss samples
- Calculates median baseline values
- Compares current metrics to baseline
- Adapts to network changes over time

**Status:** Check if baseline is learned by looking at "Baseline" values in stats panel.

### Attack Classification

Based on metric patterns:
- **ICMP Flood:** Very high packet loss (>50%)
- **UDP Flood:** High loss (>20%) + high latency (>200ms)
- **SYN Flood:** Very high latency (>500ms) + low loss (<10%)
- **Mixed Attack:** High latency (>100ms) + moderate loss (>10%)

### Connection Tracking

Monitors TCP/UDP connections:
- Total connections
- State distribution (ESTABLISHED, SYN_SENT, TIME_WAIT, etc.)
- Unique remote IPs
- Port scan detection (high SYN_RECV count)

### Historical Data Analysis

```bash
# Analyze attack patterns
python3 -c "
import json
with open('logs/attacks.json') as f:
    attacks = json.load(f)
    print(f'Total attacks: {len(attacks)}')
    types = {}
    for a in attacks:
        t = a['attack_type']
        types[t] = types.get(t, 0) + 1
    print('Attack types:')
    for t, count in types.items():
        print(f'  {t}: {count}')
"

# Analyze statistics
import pandas as pd
df = pd.read_csv('logs/stats.csv')
print(df.describe())
print(df.groupby('state').size())
```

## 🛡️ Security Best Practices

### For Lab Use

1. **Isolated Network:**
   - Run in airgapped lab environment
   - Do not deploy on production networks without permission

2. **Test Simulator:**
   - Only use test_simulator.py in controlled environments
   - Requires root privileges (uses tc command)
   - Automatically cleans up traffic control rules on exit

3. **Alerting:**
   - Use secure webhook URLs (keep Discord webhook private)
   - Use app passwords for email (not your main password)
   - Set appropriate cooldown periods to avoid alert spam

### For Mirai Analysis

This tool is designed for analyzing **Mirai malware in airgapped lab environments**:

- Monitor network degradation during Mirai attacks
- Classify attack types (Mirai uses multiple DDoS vectors)
- Log attack patterns for analysis
- Learn baseline before deploying honeypots

**Never:**
- Connect an infected system to production networks
- Use this as your only security measure
- Deploy without proper lab isolation

## 🐛 Troubleshooting

### Common Issues

**Problem:** "Gateway detection error"
```bash
# Solution: Manually set gateway in config.json
{
  "network": {
    "gateway": "192.168.1.1"  # Your router's IP
  }
}
```

**Problem:** "No SSID detected"
```bash
# Install wireless-tools (Linux)
sudo apt install wireless-tools

# Or set target_network manually
{
  "network": {
    "target_network": "192.168.1"  # First 3 octets of your IP
  }
}
```

**Problem:** Desktop notifications not working
```bash
# Install libnotify (Ubuntu/Debian)
sudo apt install libnotify-bin

# Test manually
notify-send "Test" "This is a test notification"
```

**Problem:** Public IP shows "Detecting..."
```bash
# Check internet connectivity
curl https://api.ipify.org

# If firewall blocks it, public IP will remain N/A (doesn't affect detection)
```

**Problem:** "Permission denied" for test_simulator.py
```bash
# Test simulator requires root for tc (traffic control)
sudo python3 test_simulator.py
```

### Debug Mode

Run with Python's verbose output:
```bash
python3 -v ddos_gotchi.py
```

Check logs:
```bash
# Monitor stdout
python3 ddos_gotchi.py 2>&1 | tee debug.log

# Check system logs
journalctl -f | grep ddos
```

## 📈 Performance

### System Requirements

- **CPU:** Minimal (ping operations every 2 seconds)
- **RAM:** ~50-100 MB
- **Network:** Active connection required
- **Disk:** <10 MB for logs (configurable)

### Optimization Tips

1. **Reduce FPS** if CPU usage is high:
   ```json
   {"ui": {"fps": 20}}
   ```

2. **Increase check interval** for less frequent monitoring:
   ```json
   {"monitoring": {"check_interval_seconds": 5}}
   ```

3. **Disable features** you don't need:
   ```json
   {
     "features": {
       "export_stats": false,
       "desktop_notifications": false
     },
     "ui": {
       "matrix_rain_enabled": false,
       "scanlines_enabled": false
     }
   }
   ```

## 🤝 Contributing

This is an educational/research project. Contributions welcome!

Areas for enhancement:
- Machine learning integration
- More attack signatures
- Network flow analysis
- Sound effects
- Additional visualization options
- Mobile app companion

## 📜 License

MIT License with educational use notice. See LICENSE file.

**Important:** This tool is designed for educational and research purposes in controlled lab environments. Do not use for unauthorized network monitoring or attacks.

## 🙏 Credits

- Inspired by **Pwnagotchi** - AI-powered WiFi auditing companion
- Matrix rain effect inspired by classic cyberpunk aesthetics
- Built for Mirai malware research in isolated lab environments

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/junt506/DDoSGotchi/issues)
- **Docs:** See QUICKSTART.md for quick reference

---

<div align="center">

**Made with ❤️ for the cybersecurity research community**

**Stay safe, monitor networks, defeat DDoS! 🛡️**

</div>
