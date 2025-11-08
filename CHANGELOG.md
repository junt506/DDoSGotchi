# Changelog

All notable changes to DDoS Gotchi will be documented in this file.

## [2.0.0] - 2025-11-08

### 🎉 Major Rewrite - Advanced Detection System

This is a complete rewrite of DDoS Gotchi with professional-grade features while maintaining the fun virtual pet interface.

### ✨ Added

#### Core Functionality
- **ConfigManager class** - Fully functional configuration loading system
  - All settings in config.json are now actually used
  - Auto-detection of network configuration (gateway, network prefix)
  - Graceful fallback to defaults

- **IPDetector class** - Local and public IP address detection
  - Displays both local and public IP in header
  - Auto-refresh every 60 seconds
  - Multiple API fallbacks for reliability

#### Advanced Detection
- **AttackDetector class** - Multi-layered attack detection
  - Baseline learning (learns normal network behavior)
  - Anomaly score calculation
  - Attack type classification (SYN flood, UDP flood, ICMP flood, Mixed, Slow DDoS)
  - Confidence scoring

- **TrafficAnalyzer class** - Network traffic analysis
  - Connection count tracking
  - TCP connection state monitoring
  - Port scan detection
  - Anomaly detection in connection patterns

#### Data Management
- **DataLogger class** - Persistent data storage
  - Attack logging to JSON (logs/attacks.json)
  - Statistics export to CSV (logs/stats.csv)
  - 24-hour attack history retrieval
  - Automatic log directory creation

#### Alerting System
- **AlertManager class** - Multi-channel alerts
  - Desktop notifications (Linux notify-send)
  - Discord webhook integration with rich embeds
  - Email alerts via SMTP (TLS/SSL support)
  - Configurable cooldown periods (default: 5 minutes)

#### Visualization
- **GraphRenderer class** - Real-time graphing
  - Latency graph (last 60 data points)
  - Packet loss graph (last 60 data points)
  - Line graphs with color-coded borders
  - Current value display

- **Enhanced UI (CyberUI class)** - Multi-panel dashboard
  - Increased resolution to 1280x800 (configurable up to 4K)
  - 4-panel layout: Gotchi, Stats, Graphs, Attack History
  - Header with IP information display
  - Color-coded statistics
  - Enhanced visual effects

#### Network Monitoring
- **NetworkMonitor enhancements**
  - Auto-detection of gateway using netifaces
  - Auto-detection of network prefix
  - Multi-gateway monitoring support
  - Baseline learning (collects 100 samples)
  - Configurable ping count and intervals

#### Configuration
- Complete config.json redesign with 8 sections:
  - `network` - Network configuration
  - `thresholds` - Detection thresholds (now actually used!)
  - `ui` - Window size, FPS, animations
  - `colors` - Customizable color scheme
  - `monitoring` - Smoothing, history, intervals
  - `features` - Feature toggles
  - `alerts` - Alert configuration (Discord, Email)
  - `logging` - Log file settings
  - `detection` - Detection algorithm settings

### 🔧 Changed

- **Window size**: Increased from 900x600 to 1280x800 (configurable)
- **FPS**: Now configurable via config.json (default: 30)
- **State determination**: Now uses configured thresholds from config.json
- **Network detection**: Now auto-detects gateway and network on ANY network
- **UI layout**: Complete redesign with multi-panel dashboard
- **Statistics display**: More comprehensive with 17 metrics
- **Quote system**: Improved with cleaner rendering

### 🚀 Improved

- **Performance**:
  - Connection tracking in background thread
  - IP detection with caching (60-second refresh)
  - Optimized graph rendering

- **Reliability**:
  - Multiple fallback methods for network detection
  - Graceful handling of missing configuration
  - Defensive coding for race conditions
  - Better error handling throughout

- **Cross-platform**:
  - Better Windows compatibility
  - Auto-adaptation when features unavailable
  - Platform-specific code paths

- **Documentation**:
  - Complete README rewrite (700+ lines)
  - Configuration examples
  - Troubleshooting guide
  - Performance optimization tips
  - Security best practices

### 📝 Technical Details

#### New Classes (11 total)
1. **ConfigManager** - Configuration management
2. **IPDetector** - IP address detection
3. **AttackDetector** - Attack detection algorithms
4. **TrafficAnalyzer** - Traffic pattern analysis
5. **DataLogger** - Persistent storage
6. **AlertManager** - Multi-channel alerting
7. **SoundManager** - Sound effects framework
8. **GraphRenderer** - Real-time graphing
9. **NetworkMonitor** (enhanced) - Network monitoring
10. **StateManager** (enhanced) - State management
11. **CyberUI** (enhanced) - UI rendering

#### New Dependencies
- `requests` - For public IP detection and Discord webhooks
- All other features use standard library

#### Code Statistics
- **Lines of code**: 741 → 1702 (130% increase)
- **Classes**: 5 → 11 (120% increase)
- **Features**: 10 → 30+ (200% increase)
- **Configurable parameters**: 0 → 50+ (∞% increase!)

### 🐛 Fixed

- **CRITICAL**: Config file is now actually loaded and used (was completely ignored in v1.0)
- Race condition on startup (stats initialization)
- Hardcoded window dimensions
- Hardcoded thresholds
- Hardcoded network configuration
- No public IP display
- No attack logging
- No data export
- No alerting system

### 🔐 Security

- All alerts use proper authentication (webhook URLs, SMTP passwords)
- No credentials stored in code
- Secure SMTP with TLS/SSL
- Alert cooldowns prevent spam
- Designed for airgapped lab environments

### 📊 Statistics

**Features Implemented:**
- ✅ Config.json loading (NEW!)
- ✅ Auto-network detection (NEW!)
- ✅ Multi-layered detection (NEW!)
- ✅ Attack classification (NEW!)
- ✅ Baseline learning (NEW!)
- ✅ Real-time graphs (NEW!)
- ✅ Desktop notifications (NEW!)
- ✅ Discord alerts (NEW!)
- ✅ Email alerts (NEW!)
- ✅ Attack logging (NEW!)
- ✅ Stats export (NEW!)
- ✅ Public IP display (NEW!)
- ✅ Connection tracking (NEW!)
- ✅ 1280x800 resolution (NEW!)
- ✅ Multi-panel dashboard (NEW!)
- ✅ 50+ configurable parameters (NEW!)

### 🎯 Breaking Changes

- Configuration file structure changed (but backwards compatible)
- Window size changed (900x600 → 1280x800)
- New dependency: `requests` library

### 🔄 Migration Guide

If upgrading from v1.0:

1. **Backup your old config.json** (though it wasn't being used!)
2. **Update config.json** to new format (see README)
3. **Install new dependency**: `pip install requests`
4. **Adjust window size** if needed in config.json
5. **Configure alerts** (optional) in config.json

The application will work with the old config.json but won't use the new features. Use the new format for full functionality.

### 📚 Documentation

- **README.md**: Complete rewrite (700+ lines)
- **QUICKSTART.md**: Unchanged (still valid)
- **CHANGELOG.md**: This file (NEW!)
- **config.json**: Fully documented with all options

### 🙏 Acknowledgments

This release transforms DDoS Gotchi from a fun demo into a production-ready security monitoring tool while keeping its charming personality!

**Perfect for:**
- Security researchers analyzing Mirai malware
- Network administrators monitoring for DDoS
- Students learning about attack detection
- Anyone who wants a cyber-pet with superpowers!

---

## [1.0.0] - 2025-11-06

### Initial Release

- Basic DDoS detection using latency and packet loss
- 5 mood states with ASCII faces
- Matrix rain background effect
- Simple threshold-based detection
- Test simulator for attack simulation
- Cross-platform support (Linux, Windows, macOS)

**Note**: This version had a critical bug where config.json was read but never actually used!
