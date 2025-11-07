# QUICK START GUIDE - DDoS Gotchi

## 🚀 Fastest Setup (Copy & Paste)

```bash
# 1. Install dependencies (Ubuntu/Debian)
sudo apt update && sudo apt install python3 python3-pip
pip3 install pygame psutil netifaces

# 2. Run DDoS Gotchi
python3 ddos_gotchi.py
```

## 🎮 Controls
- **ESC** = Exit
- **SPACE** = Change quote

## 🧪 Test Without Real Attacks

Run the simulator (Linux only):
```bash
# Terminal 1 - Run DDoS Gotchi
python3 ddos_gotchi.py

# Terminal 2 - Run simulator (requires sudo)
sudo python3 test_simulator.py
```

## 📁 Files Included

- `ddos_gotchi.py` - Main program
- `requirements.txt` - Python dependencies  
- `config.json` - Optional configuration
- `test_simulator.py` - Network condition simulator
- `launch.sh` - Easy launcher script
- `README.md` - Full documentation

## 🎯 What You'll See

The gotchi will react to your network conditions:
- **Happy Face** `(⌐■_■)` = Network is stable
- **Alert Face** `(⌐■_◉)` = Slight issues detected
- **Attack Face** `(✖╭╮✖)` = DDoS detected!
- **Stressed Face** `(⊙﹏⊙)` = Severe attack
- **Disconnected** `(×_×)` = No network

## 💡 Tips

1. **For Mirai Lab Testing**: 
   - Set gateway to your router IP in the code
   - Connect to the target network
   - Launch Mirai attacks to see reactions

2. **For General Use**:
   - Works on any network
   - Monitors your current connection
   - Detects any network degradation

3. **Customization**:
   - Edit `config.json` for settings
   - Modify quotes in the main file
   - Adjust detection thresholds

## ⚠️ Troubleshooting

**"No module named pygame"**
→ Run: `pip3 install pygame psutil netifaces`

**High latency on normal network**
→ Your network might actually be slow, or adjust thresholds in config

**Can't see SSID**
→ Normal on some systems, the IP detection still works

## 🎨 Enjoy Your Cyber Pet!

Watch as your DDoS Gotchi protects your network with style! 
The Matrix rain effect and cyber aesthetics make monitoring fun.

---
Educational Use Only | Built with 💚 for the Cybersecurity Community
