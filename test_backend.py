#!/usr/bin/env python3
"""
Test script to verify network monitoring works
"""

import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from core.network_monitor import NetworkMonitor
from core.attack_detector import AttackDetector
import json

print("🧪 Testing Network Monitor...")
print("=" * 50)

# Initialize monitor
monitor = NetworkMonitor()
detector = AttackDetector()

print(f"✅ Monitor initialized")
print(f"   Gateway: {monitor.gateway}")
print(f"   Network: {monitor.target_network}")
print(f"   Interface: {monitor.interface}")
print(f"   SSID: {monitor.current_ssid}")
print()

# Get stats
print("📊 Getting current stats...")
try:
    stats = monitor.get_current_stats()
    print("✅ Stats retrieved successfully:")
    print(json.dumps(stats, indent=2, default=str))
    print()
except Exception as e:
    print(f"❌ Error getting stats: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test attack detection
print("🔍 Testing attack detection...")
try:
    attack_info = detector.detect(stats)
    print("✅ Attack detection successful:")
    print(json.dumps(attack_info, indent=2, default=str))
except Exception as e:
    print(f"❌ Error in attack detection: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("✅ All tests passed!")
