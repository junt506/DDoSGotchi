# DDoS Gotchi - Desktop Edition 🖥️

Simple, modern desktop application for real-time DDoS detection.

## Quick Start (New Computer)

### 1. Install Dependencies

```bash
pip install -r requirements-desktop.txt
```

Or install individually:
```bash
pip install netifaces psutil matplotlib
```

**Note**: If you get a tkinter error, install it via your system package manager:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS**: Already included with Python

### 2. Run the App

**Easy way:**
```bash
./run-desktop.sh
```

**Manual way:**
```bash
python3 ddos_gotchi_desktop.py
```

## Features

- ✅ **Simple Status**: Just "Normal" or "Under Attack" - no complicated emotions
- 🎨 **Cyber Aesthetic**: Dark theme with neon cyan/pink accents
- 📊 **Real-time Graphs**: Smooth latency and packet loss visualization
- 🚀 **No Web Server**: Single Python file, runs instantly
- 🔒 **Reliable**: Background thread monitoring with no blocking

## What You'll See

```
┌─────────────────────────────────┐
│  DDoS GOTCHI                    │
├─────────────────────────────────┤
│  ✅ NORMAL                      │  ← Large status indicator
├─────────────────────────────────┤
│ Network Status    │  Monitor    │
│ Gateway: X.X.X.X  │    😊       │
│ Latency: 1.2ms    │             │
│ Packet Loss: 0%   │  All OK     │
├─────────────────────────────────┤
│  [Real-time Graphs]             │
│  Latency │ Packet Loss          │
└─────────────────────────────────┘
```

## How It Detects Attacks

The app monitors your network for:
- **High latency** (>100ms sustained)
- **Packet loss** (>5% sustained)
- **Anomalous patterns** compared to your baseline

When detected, the status switches to:
```
🚨 UNDER ATTACK
Attack Type: ICMP Flood / Network Saturation
```

## Troubleshooting

**"No module named 'tkinter'"**
- Install tkinter via system package manager (see above)

**"No network detected"**
- Make sure you're connected to a network
- Check that netifaces can detect your gateway

**Graphs not showing**
- Make sure matplotlib is installed: `pip install matplotlib`

## Differences from Web Version

| Feature | Web Version | Desktop Version |
|---------|-------------|-----------------|
| Setup | FastAPI + React + WebSocket | Single Python file |
| Dependencies | ~340 npm packages + Python | 3 Python packages |
| Start time | ~30 seconds | Instant |
| Complexity | High | Low |
| States | 4 emotions | 2 simple states |
| Reliability | WebSocket issues | Stable |

## Why Desktop?

The web version (v3.0) was overcomplicated with:
- FastAPI backend server
- React frontend with Vite build
- WebSocket real-time connections
- Complex state management
- Multiple emotional states

This desktop version is **much simpler** while keeping all the core functionality you need.
