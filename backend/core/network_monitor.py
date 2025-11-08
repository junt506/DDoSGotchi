"""
Network Monitor - Core detection engine
Handles network monitoring with auto-switching support
"""

import subprocess
import platform
import netifaces
import socket
import psutil
import statistics
import time
import re
from collections import deque
from typing import Dict, Optional, List


class NetworkMonitor:
    """Enhanced network monitoring with dynamic network switching"""

    def __init__(self):
        self.gateway = None
        self.target_network = None
        self.interface = None
        self.current_ssid = None
        self.connected = False

        # History tracking
        self.latency_history = deque(maxlen=60)
        self.packet_loss_history = deque(maxlen=60)
        self.baseline_latencies = deque(maxlen=100)
        self.baseline_packet_loss = deque(maxlen=100)

        # Current state
        self.current_state = 'disconnected'
        self.last_update = 0

        # Initialize
        self.detect_and_configure()

    def detect_and_configure(self):
        """Detect and configure network parameters"""
        print("🔍 Detecting network configuration...")

        self.gateway = self._detect_gateway()
        self.target_network = self._detect_network_prefix()
        self.interface = self._get_active_interface()
        self.current_ssid = self._get_ssid()
        self.connected = self._check_connectivity()

        print(f"✅ Configured: Gateway={self.gateway}, Network={self.target_network}, Interface={self.interface}")

    def _detect_gateway(self) -> Optional[str]:
        """Auto-detect default gateway"""
        try:
            gws = netifaces.gateways()
            if 'default' in gws and netifaces.AF_INET in gws['default']:
                return gws['default'][netifaces.AF_INET][0]
        except Exception as e:
            print(f"Gateway detection error: {e}")
        return None

    def _detect_network_prefix(self) -> Optional[str]:
        """Auto-detect network prefix from local IP"""
        try:
            local_ip = self._get_local_ip()
            if local_ip:
                return '.'.join(local_ip.split('.')[:3])
        except Exception as e:
            print(f"Network prefix detection error: {e}")
        return None

    def _get_active_interface(self) -> Optional[str]:
        """Find the active network interface"""
        try:
            interfaces = netifaces.interfaces()

            # Prioritize wireless
            for iface in interfaces:
                if iface.startswith(('wl', 'wifi', 'wlan')):
                    addrs = netifaces.ifaddresses(iface)
                    if netifaces.AF_INET in addrs:
                        return iface

            # Fallback to any active
            for iface in interfaces:
                if iface != 'lo':
                    addrs = netifaces.ifaddresses(iface)
                    if netifaces.AF_INET in addrs:
                        return iface
        except Exception as e:
            print(f"Interface detection error: {e}")
        return None

    def _get_local_ip(self) -> Optional[str]:
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return None

    def _get_ssid(self) -> Optional[str]:
        """Get current SSID (Linux only)"""
        if platform.system() == "Linux":
            try:
                result = subprocess.run(
                    ['iwgetid', '-r'],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except:
                pass
        return self.target_network if self.target_network else "Unknown"

    def _check_connectivity(self) -> bool:
        """Check if we have network connectivity"""
        if not self.gateway:
            return False

        try:
            socket.create_connection((self.gateway, 80), timeout=1).close()
            return True
        except:
            return False

    def get_latency(self) -> float:
        """Measure latency to gateway"""
        if not self.connected or not self.gateway:
            return -1

        try:
            if platform.system() == "Windows":
                cmd = ['ping', '-n', '1', '-w', '1000', self.gateway]
            else:
                cmd = ['ping', '-c', '1', '-W', '1', self.gateway]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)

            if result.returncode == 0:
                match = re.search(r'time=(\d+\.?\d*)\s*ms', result.stdout)
                if match:
                    latency = float(match.group(1))
                    self.latency_history.append(latency)
                    self.baseline_latencies.append(latency)
                    return latency
        except Exception as e:
            print(f"Latency check error: {e}")

        return -1

    def get_packet_loss(self) -> float:
        """Measure packet loss"""
        if not self.connected or not self.gateway:
            return 100.0

        try:
            if platform.system() == "Windows":
                cmd = ['ping', '-n', '5', '-w', '1000', self.gateway]
            else:
                cmd = ['ping', '-c', '5', '-W', '1', '-i', '0.2', self.gateway]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

            match = re.search(r'(\d+)%\s*(packet\s*)?loss', result.stdout)
            if match:
                loss = float(match.group(1))
                self.packet_loss_history.append(loss)
                self.baseline_packet_loss.append(loss)
                return loss
        except Exception as e:
            print(f"Packet loss check error: {e}")

        return 0.0 if self.connected else 100.0

    def get_current_stats(self) -> Dict:
        """Get current network statistics"""
        # Update connection status
        self.connected = self._check_connectivity()

        stats = {
            'timestamp': time.time(),
            'connected': self.connected,
            'ssid': self.current_ssid or 'Not Connected',
            'gateway': self.gateway,
            'interface': self.interface,
            'network': self.target_network,
            'latency': -1,
            'packet_loss': 0,
            'avg_latency': -1,
            'avg_packet_loss': 0,
            'baseline_latency': 0,
            'baseline_packet_loss': 0
        }

        if self.connected:
            latency = self.get_latency()
            packet_loss = self.get_packet_loss()

            stats['latency'] = latency
            stats['packet_loss'] = packet_loss

            if self.latency_history:
                stats['avg_latency'] = sum(self.latency_history) / len(self.latency_history)

            if self.packet_loss_history:
                stats['avg_packet_loss'] = sum(self.packet_loss_history) / len(self.packet_loss_history)

            if self.baseline_latencies:
                stats['baseline_latency'] = statistics.median(self.baseline_latencies)

            if self.baseline_packet_loss:
                stats['baseline_packet_loss'] = statistics.median(self.baseline_packet_loss)

        return stats

    def get_network_info(self) -> Dict:
        """Get detailed network information"""
        return {
            'gateway': self.gateway,
            'network': self.target_network,
            'interface': self.interface,
            'ssid': self.current_ssid,
            'local_ip': self._get_local_ip(),
            'connected': self.connected
        }

    def reinitialize(self):
        """Reinitialize network configuration (called on network change)"""
        print("🔄 Reinitializing network configuration...")

        # Clear histories
        self.latency_history.clear()
        self.packet_loss_history.clear()

        # Re-detect network
        self.detect_and_configure()

        print(f"✅ Reinitialized on new network: {self.target_network}")
