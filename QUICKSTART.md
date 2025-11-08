# QUICK START GUIDE - DDoS Gotchi v2.0

## 🚀 Fastest Setup (Copy & Paste)

### Ubuntu/Debian
```bash
# 1. Install system dependencies
sudo apt update && sudo apt install python3 python3-pip wireless-tools iproute2 libnotify-bin

# 2. Install Python packages
pip3 install pygame psutil netifaces requests

# 3. Run DDoS Gotchi
python3 ddos_gotchi.py
```

### Fedora/RHEL
```bash
# 1. Install system dependencies
sudo dnf install python3 python3-pip wireless-tools iproute libnotify

# 2. Install Python packages
pip3 install pygame psutil netifaces requests

# 3. Run DDoS Gotchi
python3 ddos_gotchi.py
```

### Using requirements.txt
```bash
pip3 install -r requirements.txt
python3 ddos_gotchi.py
```

## 🎮 Controls
- **ESC** = Exit
- **SPACE** = Change quote

## ✨ What's New in v2.0

**Major Upgrade!** DDoS Gotchi is now a production-ready security monitoring tool:
- ✅ **1280x800 resolution** with multi-panel dashboard
- ✅ **Config.json NOW WORKS** - All settings are functional!
- ✅ **Auto-detection** - Works on ANY network automatically
- ✅ **Real-time graphs** - Latency and packet loss visualization
- ✅ **IP display** - Shows your local + public IP
- ✅ **Attack classification** - Identifies SYN flood, UDP flood, ICMP flood, etc.
- ✅ **Desktop notifications** - Get alerts when attacks detected (Linux)
- ✅ **Attack logging** - Saves to `logs/attacks.json`
- ✅ **Stats export** - Saves to `logs/stats.csv`
- ✅ **Baseline learning** - Learns your network's normal behavior

## 🧪 Test Without Real Attacks

Run the simulator (Linux only):
```bash
# Terminal 1 - Run DDoS Gotchi
python3 ddos_gotchi.py

# Terminal 2 - Run simulator (requires sudo)
sudo python3 test_simulator.py
# Select from 7 attack scenarios!
```

The new detection system will **automatically classify** the attack type!

## 📁 Files Included

- `ddos_gotchi.py` - Main program (v2.0 - 1,702 lines!)
- `config.json` - **FULLY FUNCTIONAL** configuration
- `requirements.txt` - Python dependencies
- `test_simulator.py` - Network condition simulator
- `launch.sh` - Easy launcher script
- `README.md` - Comprehensive documentation (700+ lines)
- `CHANGELOG.md` - Version history
- `QUICKSTART.md` - This file

## 🎯 What You'll See

### Multi-Panel Dashboard (1280x800)

```
┌────────────────────────────────────────────────┐
│  [ DDOS GOTCHI - ADVANCED DETECTION SYSTEM ]   │
│  LOCAL IP: 192.168.1.100 | PUBLIC: 1.2.3.4    │
├──────────────┬─────────────────────────────────┤
│  GOTCHI      │  REAL-TIME GRAPHS               │
│  (⌐■_■)      │  [Latency Graph]                │
│  [ HAPPY ]   │  [Packet Loss Graph]            │
│              │                                 │
│  NETWORK     │  ATTACK DETECTION               │
│  STATS       │  Status: ✓ No Attack            │
│  17 metrics  │  Recent Attacks (24h)           │
└──────────────┴─────────────────────────────────┘
```

### The Gotchi Moods
- **Happy** `(⌐■_■)` = Network is stable (< 10ms latency)
- **Alert** `(⌐■_◉)` = Slight issues detected (10-50ms)
- **Under Attack** `(✖╭╮✖)` = DDoS detected! (50-200ms)
- **Stressed** `(⊙﹏⊙)` = Severe attack (> 200ms)
- **Disconnected** `(×_×)` = No network connection

## ⚙️ Quick Configuration

Edit `config.json` to customize (all settings now work!):

### Auto-Detect (Default - Recommended)
```json
{
  "network": {
    "target_network": "auto",
    "gateway": "auto"
  }
}
```
**Just run it - no config needed!** Works on any network.

### Manual Configuration
```json
{
  "network": {
    "target_network": "192.168.1",
    "gateway": "192.168.1.1"
  }
}
```

### Window Size
```json
{
  "ui": {
    "window_width": 1280,
    "window_height": 800
  }
}
```
Options: 1280x800 (default), 1920x1080 (full HD), 2560x1440 (2K)

### Detection Sensitivity
```json
{
  "thresholds": {
    "happy": {
      "max_latency": 10,
      "max_packet_loss": 1
    }
  }
}
```
Adjust based on your network's baseline.

## 🔔 Enable Alerts (Optional)

### Desktop Notifications (Linux)
Already enabled by default! You'll get notifications when attacks are detected.

### Discord Alerts
1. Create a webhook in Discord (Server Settings → Integrations → Webhooks)
2. Edit `config.json`:
```json
{
  "features": {
    "discord_webhooks": true
  },
  "alerts": {
    "discord_webhook_url": "https://discord.com/api/webhooks/YOUR_URL"
  }
}
```

### Email Alerts
1. Generate app password (Gmail: Account → Security → App passwords)
2. Edit `config.json`:
```json
{
  "features": {
    "email_alerts": true
  },
  "alerts": {
    "email_smtp_server": "smtp.gmail.com",
    "email_from": "your-email@gmail.com",
    "email_password": "your-app-password",
    "email_to": "recipient@example.com"
  }
}
```

## 📊 View Logs

```bash
# Attack history (JSON)
cat logs/attacks.json

# Statistics export (CSV)
cat logs/stats.csv

# Real-time monitoring
tail -f logs/attacks.json
```

## 💡 Usage Tips

### 1. For Mirai Lab Testing
- **Auto-detection works!** Just run it on your lab network
- Or manually set gateway in `config.json`
- Launch Mirai attacks to see classification
- Check `logs/attacks.json` for detailed attack data

### 2. For General Network Monitoring
- Works on any network (WiFi, Ethernet, VPN)
- Auto-detects gateway and configuration
- Monitors connection quality in real-time
- Desktop notifications keep you informed

### 3. Customization
- Edit `config.json` for ALL settings (50+ parameters!)
- Adjust detection thresholds for your network
- Enable/disable features (graphs, notifications, logging)
- Change window size, colors, animations

### 4. Data Analysis
- Export stats to CSV for analysis with pandas/Excel
- Attack logs in JSON for programmatic analysis
- 24-hour attack history visible in UI

## ⚠️ Troubleshooting

**"No module named pygame/requests"**
```bash
pip3 install -r requirements.txt
```

**Desktop notifications not working**
```bash
sudo apt install libnotify-bin  # Ubuntu/Debian
sudo dnf install libnotify      # Fedora
```

**Public IP shows "Detecting..."**
- Normal if firewall blocks external APIs
- Doesn't affect DDoS detection (only display)

**No SSID detected**
```bash
sudo apt install wireless-tools  # Ubuntu/Debian
# Or set manually: "target_network": "192.168.1" in config.json
```

**Gateway detection error**
- Manually set in `config.json`: `"gateway": "192.168.1.1"`

**Window too big/small**
- Edit `config.json`: Change `window_width` and `window_height`

## 🎓 Learn More

- **Full Documentation**: See `README.md` (700+ lines)
- **Configuration Guide**: All 50+ parameters explained
- **Version History**: See `CHANGELOG.md`
- **Test Scenarios**: `test_simulator.py` has 7 attack types

## 🚀 Advanced Features

Explore the full power of v2.0:
- Multi-layered detection (threshold + baseline + anomaly)
- Attack type classification
- Connection tracking and port scan detection
- Multiple gateway monitoring
- Historical data analysis
- Configurable alert cooldowns
- Custom color schemes
- Animation toggles

**See README.md for complete details!**

## 🎨 Enjoy Your Advanced Cyber Pet!

Watch as your DDoS Gotchi:
- 📊 Displays real-time graphs of network performance
- 🧠 Learns your network's normal behavior
- 🔍 Detects and classifies different attack types
- 🔔 Alerts you via desktop/Discord/email
- 📝 Logs all attacks for analysis
- 🌐 Shows your local and public IP
- 💚 Protects your network with Matrix-themed style!

---

**v2.0 - Production Ready** | Educational Use Only | Built with 💚 for the Cybersecurity Community
