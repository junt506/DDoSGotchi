# DDoS Gotchi Lab Mode 🔬

**Sensitive detection mode for isolated malware testing environments**

## What is Lab Mode?

Lab Mode is a special detection mode designed for security researchers testing DDoS attacks in isolated/airgapped lab environments. It uses much lower thresholds and more aggressive detection than production mode.

Perfect for:
- Testing Mirai botnet variants
- Low-volume DDoS attack simulation
- Honeypot deployments with limited attack traffic
- Security research in controlled environments

## Key Differences from Production Mode

| Feature | Production Mode | Lab Mode |
|---------|----------------|----------|
| Attack Threshold | 50 connections/IP | **5 connections/IP** |
| Suspicious Threshold | 20 connections/IP | **3 connections/IP** |
| Total Connections | 100 total | **10 total** |
| Traffic-Based Detection | 1000 packets/sec | **150 packets/sec** (UDP/ICMP floods) |
| Connection Monitoring | ESTABLISHED only | **ALL states** (SYN floods, half-open, etc.) |
| Botnet Detection | ❌ Disabled | **✅ Enabled** (3+ IPs from same subnet) |
| Debug Logging | Minimal | **Enhanced** (attack details, traffic stats) |
| Traffic Volume Monitoring | ❌ Basic | **✅ Full** (bytes/sec, packets/sec) |

## Quick Start

### Method 1: Use Lab Mode Launcher (Recommended)

```bash
./run-electron-lab.sh
```

This automatically enables Lab Mode with optimal settings for malware testing.

### Method 2: Manual Environment Variable

```bash
export LAB_MODE=true
./run-electron.sh
```

### Method 3: One-Line Command

```bash
LAB_MODE=true ./run-electron.sh
```

## What Lab Mode Detects

### 1. **Low-Volume Attacks**
- Detects attacks with as few as **5 connections from a single IP**
- Suspicious activity flagged at **3 connections**
- Perfect for small Mirai botnets (6-10 Raspberry Pis)

### 2. **SYN Floods & Half-Open Connections**
- Monitors **all connection states**, not just ESTABLISHED
- Detects SYN_SENT, SYN_RECV, FIN_WAIT, etc.
- Catches attacks that don't complete TCP handshake

### 3. **Botnet Patterns**
- Automatically detects **multiple IPs from same subnet**
- Flags when 3+ IPs from **ANY** /24 subnet attack
- **Works with any subnet** (45.33.0.x, 192.168.x.x, 10.x.x.x, etc.)
- Dynamically extracts subnet from attacking IPs
- Perfect for detecting coordinated botnet behavior

### 4. **Traffic Volume Spikes (UDP/ICMP Floods)**
- **CRITICAL for detecting UDP floods** - doesn't rely on connections
- Triggers attack at **150 packets/sec** in Lab Mode (vs 1000 in production)
- Tracks **bytes per second** and **packets per second**
- Detects volumetric attacks that don't show up as TCP connections
- Perfect for Mirai UDP floods, ICMP floods, and other stateless attacks

### 5. **Directional Connection Tracking**
- Distinguishes **incoming vs outgoing** connections
- Focuses attack detection on incoming traffic only
- Reduces false positives from normal outbound connections

## Enhanced Logging in Lab Mode

Lab Mode provides detailed attack information in the console:

**Example 1: UDP Flood Detection**
```
🚨 LAB MODE - ATTACK DETECTED!
   Attack Type: Volumetric DDoS (UDP/ICMP Flood)
   Incoming connections: 2
   Traffic: 402 packets/sec, 22.1 KB/sec
   Attack IPs: Unknown (volumetric)
   Threat level: CRITICAL
```

**Example 2: Connection-Based Attack (HTTP flood, SYN flood)**
```
🚨 LAB MODE - ATTACK DETECTED!
   Attack Type: Connection-based DDoS
   Incoming connections: 18
   Traffic: 120 packets/sec, 15.3 KB/sec
   Attack IPs: 192.168.1.101, 192.168.1.102, 192.168.1.103
   Suspicious IPs: 192.168.1.104, 192.168.1.105
   Threat level: CRITICAL

🚨 LAB MODE: Botnet pattern detected from subnet 192.168.1.0/24 (6 IPs)
```

**Note:** The subnet shown is **dynamically detected** from the attacking IPs. It works with any subnet (192.168.x.x, 45.33.0.x, 10.x.x.x, etc.)

**Continuous Traffic Monitoring:**
```
📊 LAB MODE: High incoming traffic - 850 packets/sec, 1024.5 KB/sec
```

## Testing with Mirai Botnet

### Your Use Case: 5-6 Raspberry Pis attacking Pwnagotchi

**Problem**: Production mode didn't detect Raspberry Pis attacking your laptop
**Solution**: Lab Mode detects this easily!

**Why it now works:**

1. **Lower thresholds**: Each Pi only needs 5 connections to trigger alert
2. **Botnet detection**: 3+ Pis from same subnet = automatic detection (works with ANY subnet!)
3. **All connection states**: Catches SYN floods and incomplete connections
4. **Traffic monitoring**: Detects volumetric attack patterns

**Your Setup Example:**
- Bots on **45.33.0.0/24** subnet (45.33.0.101, 45.33.0.102, etc.)
- Lab Mode automatically detects: "Botnet pattern detected from subnet **45.33.0.0/24** (5 IPs)"
- Also works with 192.168.x.x, 10.x.x.x, or any other subnet!

### Example Attack Scenarios

#### Scenario 1: Mirai HTTP Flood (6 Raspberry Pis)
- Each Pi makes 5-10 HTTP requests
- **Production Mode**: No detection (only 30-60 total connections)
- **Lab Mode**: ✅ **DETECTED** (botnet pattern + threshold exceeded)

#### Scenario 2: SYN Flood Attack
- Pis send SYN packets without completing handshake
- **Production Mode**: No detection (not ESTABLISHED connections)
- **Lab Mode**: ✅ **DETECTED** (monitors SYN_SENT state)

#### Scenario 3: UDP Flood (Mirai command: `udp 45.33.0.4 60 dport=65535 len=512 rand=1`)
- High packet rate (300-500 pps), zero TCP connections
- UDP packets don't show up in connection monitoring
- **Production Mode**: No detection (requires 1000 pps, focuses on connections)
- **Lab Mode**: ✅ **DETECTED** (150 pps threshold, traffic-based detection)
- **Attack Type**: "Volumetric DDoS (UDP/ICMP Flood)"

## Airgapped Lab Tips

If your lab is completely airgapped (no internet):

1. **Disable threat intelligence APIs** (they won't work anyway):
   ```bash
   export ENABLE_GREYNOISE=false
   unset ABUSEIPDB_API_KEY
   LAB_MODE=true ./run-electron.sh
   ```

2. **Network monitoring still works** - all detection happens locally

3. **Latency/packet loss** - measured to local gateway, not internet

## Customizing Lab Mode Thresholds

Edit `backend_electron.py` if you need different sensitivity:

**Connection-based thresholds** (line 36-43):
```python
if self.lab_mode:
    self.attack_threshold = 5       # Lower to 3 for ultra-sensitive
    self.total_connections_threshold = 10  # Lower to 5
    self.suspicious_threshold = 3   # Lower to 2
```

**Traffic-based thresholds** (line 293-300):
```python
if self.lab_mode:
    packets_threshold = 150  # Lower to 100 for more sensitivity
    bytes_threshold = 10 * 1024  # 10 KB/sec
```

## Troubleshooting

### Still Not Detecting Attacks?

1. **Check if Lab Mode is enabled:**
   ```
   Look for "🔬 LAB MODE ENABLED" in startup banner
   ```

2. **Verify connections are incoming:**
   - Lab Mode focuses on incoming connections
   - Make sure Pis are connecting TO your laptop, not the other way around

3. **Check what DDoSGotchi sees:**
   ```bash
   # While attack is running, check connections manually:
   python3 -c "import psutil; print(len(psutil.net_connections(kind='inet')))"
   ```

4. **Enable debug output:**
   - Watch the backend console for "LAB MODE" messages
   - Should see attack alerts when thresholds exceeded

### Attack Not Showing in UI?

- Check WebSocket connection (should see "Client connected" in backend)
- Refresh Electron app (Ctrl+R)
- Check browser console for errors (Ctrl+Shift+I)

## Performance Considerations

Lab Mode is **more resource-intensive** than production mode:

- Monitors ALL connection states (not just ESTABLISHED)
- More frequent logging and debug output
- Additional traffic statistics tracking

**Recommendation**: Only use Lab Mode in testing environments, not production

## Security Note

⚠️ **Lab Mode is for ISOLATED testing environments only!**

- Lower thresholds = more false positives in production
- Enhanced logging may expose sensitive network details
- Designed for airgapped labs, not internet-facing servers

## Example: Complete Mirai Test Workflow

```bash
# 1. Start DDoS Gotchi in Lab Mode on target laptop
cd DDoSGotchi
./run-electron-lab.sh

# 2. Wait for "LAB MODE ENABLED" message

# 3. From Raspberry Pi botnet (or another terminal), run attack
# Example: Simple HTTP flood to port 80
# for i in {1..10}; do curl http://target-laptop:80 & done

# 4. Watch DDoS Gotchi console for detection:
# 🚨 LAB MODE - ATTACK DETECTED!
#    Incoming connections: 12
#    Attack IPs: 192.168.1.101
#    Threat level: CRITICAL

# 5. See visualization turn red in Electron UI!
```

## Next Steps

After confirming Lab Mode works with your Mirai attack:

1. **Tune thresholds** - Adjust if too sensitive/not sensitive enough
2. **Export data** - Save connection logs for analysis
3. **Compare with production** - Test in both modes to understand difference
4. **Contribute** - Share your findings with the community!

## Questions?

- Check main README.md for general usage
- Report issues: https://github.com/yourusername/DDoSGotchi/issues
- Lab Mode is perfect for security research and education

---

**Happy malware testing! 🔬🛡️**

*Remember: Only use in authorized, isolated lab environments*
