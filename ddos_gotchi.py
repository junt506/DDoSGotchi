#!/usr/bin/env python3
"""
DDoS Gotchi - Advanced DDoS Detection System with Virtual Pet Interface
Educational/Lab Use Only - Defensive Security Tool
Enhanced version with multi-layered detection, analytics, and alerting
"""

import pygame
import sys
import time
import json
import random
import threading
import subprocess
import platform
import socket
import psutil
import netifaces
import os
import csv
import requests
from collections import deque, Counter
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import statistics
import math

# Constants - will be overridden by config
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
FPS = 30

# Color defaults
MATRIX_GREEN = (0, 255, 65)
DARK_GREEN = (0, 128, 32)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 150, 255)
PURPLE = (200, 100, 255)
WHITE = (255, 255, 255)

# ASCII Art Faces
FACES = {
    'happy': ["  (⌐■_■)  ", "          ", "  \\___/   "],
    'alert': ["  (⌐■_◉)  ", "          ", "   ___    "],
    'under_attack': ["  (✖╭╮✖)  ", "          ", "   ~~~    "],
    'stressed': ["  (⊙﹏⊙)  ", "          ", "  /___\\   "],
    'disconnected': ["  (×_×)   ", "          ", "   ---    "]
}

# Quotes for each state
QUOTES = {
    'happy': [
        "Living my best life in this subnet",
        "Zero DDoS, infinite vibes",
        "Just a gotchi in the cyber-verse",
        "They see me pinging, they ain't flooding",
        "Connection so stable I could retire",
        "No attack? No problem!",
        "Chilling in the lab, dodging DDoS like Neo",
        "This network is my safe space",
        "Ping: low. Vibes: high.",
        "No packets dropped, no worries found",
        "Living the dream at layer 3",
        "Subnet secured, gotchi assured"
    ],
    'alert': [
        "Something's... off",
        "Hold up, detecting anomalies",
        "Is that... traffic?",
        "My spidey sense is tingling",
        "Unusual activity detected",
        "Hmm, that doesn't look right",
        "Elevated latency detected...",
        "Getting some weird vibes here"
    ],
    'under_attack': [
        "WE'RE GETTING DDOS'D!",
        "THE PACKETS! THEY'RE EVERYWHERE!",
        "ATTACK DETECTED!",
        "SYN FLOOD INCOMING!",
        "BRACE FOR IMPACT!",
        "UDP FLOOD DETECTED!",
        "THEY'RE IN THE WALLS!",
        "PACKETS OVERWHELMING!"
    ],
    'stressed': [
        "I CAN'T BREATHE!",
        "MAKE IT STOP!",
        "THIS IS NOT A DRILL!",
        "SOMEONE CALL THE NETWORK ADMIN!",
        "CRITICAL OVERLOAD!",
        "SYSTEM FAILING!",
        "CAN'T HANDLE THE PRESSURE!"
    ],
    'disconnected': [
        "No service...",
        "Disconnected from the matrix",
        "404: Network not found",
        "Lost in the void",
        "Offline and afraid",
        "Where did everybody go?",
        "Hello? Is anyone there?"
    ]
}


class ConfigManager:
    """Manages configuration loading and validation"""

    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                print(f"✓ Configuration loaded from {self.config_path}")
                return config
            else:
                print(f"⚠ Config file not found, using defaults")
                return self._get_default_config()
        except Exception as e:
            print(f"⚠ Error loading config: {e}, using defaults")
            return self._get_default_config()

    def _get_default_config(self) -> Dict:
        """Return default configuration"""
        return {
            "network": {
                "target_network": "auto",
                "gateway": "auto",
                "target_ssid": "Auto-Detect",
                "ping_count": 5,
                "ping_interval": 2,
                "additional_gateways": []
            },
            "thresholds": {
                "happy": {"max_latency": 10, "max_packet_loss": 1},
                "alert": {"max_latency": 50, "max_packet_loss": 5},
                "under_attack": {"max_latency": 200, "max_packet_loss": 20},
                "stressed": {"min_latency": 200, "min_packet_loss": 20}
            },
            "ui": {
                "window_width": 1280,
                "window_height": 800,
                "fps": 30,
                "quote_interval_seconds": 15,
                "matrix_rain_enabled": True,
                "scanlines_enabled": True,
                "blink_animation_enabled": True,
                "glitch_effects_enabled": True
            },
            "colors": {
                "matrix_green": [0, 255, 65],
                "dark_green": [0, 128, 32],
                "black": [0, 0, 0],
                "red": [255, 0, 0],
                "orange": [255, 165, 0],
                "yellow": [255, 255, 0]
            },
            "monitoring": {
                "smoothing_window": 5,
                "history_size": 10,
                "check_interval_seconds": 2,
                "connection_timeout": 1,
                "baseline_learning_period": 300
            },
            "features": {
                "sound_effects": False,
                "log_attacks": True,
                "export_stats": True,
                "desktop_notifications": True,
                "discord_webhooks": False,
                "email_alerts": False
            },
            "alerts": {
                "discord_webhook_url": "",
                "email_smtp_server": "",
                "email_smtp_port": 587,
                "email_from": "",
                "email_password": "",
                "email_to": "",
                "alert_cooldown_seconds": 300
            },
            "logging": {
                "log_directory": "logs",
                "attack_log_file": "attacks.json",
                "stats_export_file": "stats.csv",
                "max_log_size_mb": 100
            },
            "detection": {
                "enable_baseline_learning": True,
                "enable_attack_classification": True,
                "enable_connection_tracking": True,
                "suspicious_connection_threshold": 100
            }
        }

    def get(self, section: str, key: str = None, default=None):
        """Get configuration value"""
        if key is None:
            return self.config.get(section, default)
        return self.config.get(section, {}).get(key, default)

    def save(self):
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            print(f"✓ Configuration saved to {self.config_path}")
        except Exception as e:
            print(f"⚠ Error saving config: {e}")


class IPDetector:
    """Detects local and public IP addresses"""

    def __init__(self):
        self.local_ip = None
        self.public_ip = None
        self.last_update = 0
        self.update_interval = 60  # Update every 60 seconds

    def get_local_ip(self) -> Optional[str]:
        """Get local IP address"""
        try:
            # Get default interface
            interfaces = netifaces.interfaces()
            for iface in interfaces:
                if iface == 'lo':
                    continue
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        ip = addr.get('addr')
                        if ip and not ip.startswith('127.'):
                            self.local_ip = ip
                            return ip
        except Exception as e:
            print(f"Error getting local IP: {e}")

        # Fallback method
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            self.local_ip = s.getsockname()[0]
            s.close()
            return self.local_ip
        except:
            return None

    def get_public_ip(self) -> Optional[str]:
        """Get public IP address via API"""
        current_time = time.time()

        # Use cached value if recent
        if self.public_ip and (current_time - self.last_update) < self.update_interval:
            return self.public_ip

        try:
            # Try multiple services for reliability
            services = [
                'https://api.ipify.org',
                'https://ifconfig.me/ip',
                'https://icanhazip.com'
            ]

            for service in services:
                try:
                    response = requests.get(service, timeout=3)
                    if response.status_code == 200:
                        self.public_ip = response.text.strip()
                        self.last_update = current_time
                        return self.public_ip
                except:
                    continue
        except Exception as e:
            print(f"Error getting public IP: {e}")

        return self.public_ip  # Return cached value or None


class NetworkMonitor:
    """Enhanced network monitoring with multi-gateway support"""

    def __init__(self, config: ConfigManager):
        self.config = config

        # Auto-detect or use configured values
        self.gateway = self._detect_gateway()
        self.target_network = self._detect_network_prefix()

        # Additional gateways for redundancy
        self.additional_gateways = config.get('network', 'additional_gateways', [])

        self.latency_history = deque(maxlen=config.get('monitoring', 'history_size', 10))
        self.packet_loss_history = deque(maxlen=config.get('monitoring', 'history_size', 10))
        self.connected = False
        self.current_ssid = None
        self.interface = self._get_wifi_interface()

        # Multi-gateway stats
        self.gateway_stats = {}

        # Baseline learning
        self.baseline_latencies = deque(maxlen=100)
        self.baseline_packet_loss = deque(maxlen=100)
        self.baseline_learned = False

    def _detect_gateway(self) -> str:
        """Auto-detect default gateway"""
        configured_gateway = self.config.get('network', 'gateway', 'auto')
        if configured_gateway != 'auto':
            return configured_gateway

        try:
            # Try to get default gateway
            gws = netifaces.gateways()
            if 'default' in gws:
                if netifaces.AF_INET in gws['default']:
                    gateway = gws['default'][netifaces.AF_INET][0]
                    print(f"✓ Auto-detected gateway: {gateway}")
                    return gateway
        except Exception as e:
            print(f"Gateway detection error: {e}")

        # Fallback
        return "192.168.1.1"

    def _detect_network_prefix(self) -> str:
        """Auto-detect network prefix from local IP"""
        configured_network = self.config.get('network', 'target_network', 'auto')
        if configured_network != 'auto':
            return configured_network

        try:
            local_ip = IPDetector().get_local_ip()
            if local_ip:
                # Get first 3 octets
                prefix = '.'.join(local_ip.split('.')[:3])
                print(f"✓ Auto-detected network: {prefix}.0/24")
                return prefix
        except Exception as e:
            print(f"Network detection error: {e}")

        return "192.168.1"

    def _get_wifi_interface(self):
        """Find the active network interface"""
        interfaces = netifaces.interfaces()

        # Prioritize wireless interfaces
        for iface in interfaces:
            if iface.startswith(('wl', 'wifi', 'wlan')):
                return iface

        # Fallback to any active interface
        for iface in interfaces:
            if iface != 'lo':
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    return iface
        return None

    def check_wifi_connection(self) -> bool:
        """Check if connected to network and get SSID"""
        try:
            # Try to get SSID using iwgetid (Linux)
            if platform.system() == "Linux":
                try:
                    result = subprocess.run(['iwgetid', '-r'],
                                         capture_output=True,
                                         text=True,
                                         timeout=2)
                    if result.returncode == 0 and result.stdout.strip():
                        self.current_ssid = result.stdout.strip()
                        self.connected = True
                        return True
                except:
                    pass

            # Check if we have an IP in the target network
            if self.interface:
                addrs = netifaces.ifaddresses(self.interface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        ip = addr['addr']
                        if ip.startswith(self.target_network):
                            self.connected = True
                            if not self.current_ssid:
                                self.current_ssid = f"{self.target_network}.0/24"
                            return True

            # Final fallback: Can we reach the gateway?
            try:
                socket.create_connection((self.gateway, 80), timeout=1).close()
                self.connected = True
                return True
            except:
                pass

        except Exception as e:
            print(f"Connection check error: {e}")

        self.connected = False
        self.current_ssid = None
        return False

    def get_latency(self, target: str = None) -> float:
        """Measure latency to gateway using ping"""
        if not self.connected:
            return -1

        if target is None:
            target = self.gateway

        try:
            # Use ping command (cross-platform)
            if platform.system() == "Windows":
                cmd = ['ping', '-n', '1', '-w', '1000', target]
            else:
                cmd = ['ping', '-c', '1', '-W', '1', target]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)

            if result.returncode == 0:
                output = result.stdout

                # Linux/Mac pattern
                match = re.search(r'time=(\d+\.?\d*)\s*ms', output)
                if match:
                    latency = float(match.group(1))
                    if target == self.gateway:
                        self.latency_history.append(latency)
                        if self.config.get('detection', 'enable_baseline_learning', True):
                            self.baseline_latencies.append(latency)
                    return latency

                # Windows pattern
                match = re.search(r'Average = (\d+)ms', output)
                if match:
                    latency = float(match.group(1))
                    if target == self.gateway:
                        self.latency_history.append(latency)
                        if self.config.get('detection', 'enable_baseline_learning', True):
                            self.baseline_latencies.append(latency)
                    return latency
        except Exception as e:
            print(f"Latency check error: {e}")

        return -1

    def get_packet_loss(self, target: str = None) -> float:
        """Measure packet loss percentage"""
        if not self.connected:
            return 100.0

        if target is None:
            target = self.gateway

        try:
            ping_count = self.config.get('network', 'ping_count', 5)

            if platform.system() == "Windows":
                cmd = ['ping', '-n', str(ping_count), '-w', '1000', target]
            else:
                cmd = ['ping', '-c', str(ping_count), '-W', '1', '-i', '0.2', target]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            output = result.stdout

            # Parse packet loss
            match = re.search(r'(\d+)%\s*(packet\s*)?loss', output)
            if match:
                loss = float(match.group(1))
                if target == self.gateway:
                    self.packet_loss_history.append(loss)
                    if self.config.get('detection', 'enable_baseline_learning', True):
                        self.baseline_packet_loss.append(loss)
                return loss

            # Windows pattern
            match = re.search(r'\((\d+)% loss\)', output)
            if match:
                loss = float(match.group(1))
                if target == self.gateway:
                    self.packet_loss_history.append(loss)
                    if self.config.get('detection', 'enable_baseline_learning', True):
                        self.baseline_packet_loss.append(loss)
                return loss

        except Exception as e:
            print(f"Packet loss check error: {e}")

        return 0.0 if self.connected else 100.0

    def check_multiple_gateways(self) -> Dict:
        """Check latency to multiple gateways"""
        results = {}

        # Check primary gateway
        results[self.gateway] = {
            'latency': self.get_latency(self.gateway),
            'packet_loss': self.get_packet_loss(self.gateway),
            'reachable': True
        }

        # Check additional gateways
        for gw in self.additional_gateways:
            lat = self.get_latency(gw)
            results[gw] = {
                'latency': lat,
                'reachable': lat > 0
            }

        self.gateway_stats = results
        return results

    def get_network_stats(self) -> Dict:
        """Get comprehensive network statistics"""
        stats = {
            'connected': self.connected,
            'ssid': self.current_ssid or 'Not Connected',
            'latency': -1,
            'packet_loss': 0,
            'avg_latency': -1,
            'avg_packet_loss': 0,
            'interface': self.interface,
            'gateway': self.gateway,
            'baseline_latency': 0,
            'baseline_packet_loss': 0,
            'gateway_count': 1 + len(self.additional_gateways)
        }

        if self.connected:
            latency = self.get_latency()
            packet_loss = self.get_packet_loss()

            stats['latency'] = latency
            stats['packet_loss'] = packet_loss

            # Calculate averages
            if self.latency_history:
                stats['avg_latency'] = sum(self.latency_history) / len(self.latency_history)
            else:
                stats['avg_latency'] = latency

            if self.packet_loss_history:
                stats['avg_packet_loss'] = sum(self.packet_loss_history) / len(self.packet_loss_history)
            else:
                stats['avg_packet_loss'] = packet_loss

            # Calculate baseline
            if self.baseline_latencies:
                stats['baseline_latency'] = statistics.median(self.baseline_latencies)
            if self.baseline_packet_loss:
                stats['baseline_packet_loss'] = statistics.median(self.baseline_packet_loss)

        return stats


class AttackDetector:
    """Advanced attack detection with multiple algorithms"""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.attack_history = deque(maxlen=100)
        self.anomaly_scores = deque(maxlen=50)

    def classify_attack_type(self, stats: Dict) -> Optional[str]:
        """Classify the type of attack based on patterns"""
        if not self.config.get('detection', 'enable_attack_classification', True):
            return None

        latency = stats.get('avg_latency', 0)
        packet_loss = stats.get('avg_packet_loss', 0)

        # Pattern-based classification
        if packet_loss > 50:
            return "ICMP Flood / Network Saturation"
        elif packet_loss > 20 and latency > 200:
            return "UDP Flood Detected"
        elif latency > 500 and packet_loss < 10:
            return "SYN Flood / Resource Exhaustion"
        elif latency > 100 and packet_loss > 10:
            return "Mixed DDoS Attack"
        elif latency > 50:
            return "Network Congestion / Slow DDoS"

        return None

    def calculate_anomaly_score(self, stats: Dict) -> float:
        """Calculate anomaly score based on deviation from baseline"""
        score = 0.0

        baseline_lat = stats.get('baseline_latency', 0)
        current_lat = stats.get('avg_latency', 0)
        baseline_loss = stats.get('baseline_packet_loss', 0)
        current_loss = stats.get('avg_packet_loss', 0)

        if baseline_lat > 0:
            # Latency deviation (normalized to 0-50 range)
            lat_deviation = (current_lat - baseline_lat) / baseline_lat
            score += min(lat_deviation * 30, 50)

        if baseline_loss >= 0:
            # Packet loss deviation (normalized to 0-50 range)
            loss_deviation = current_loss - baseline_loss
            score += min(loss_deviation * 2, 50)

        self.anomaly_scores.append(score)
        return score

    def detect_attack_pattern(self, stats: Dict) -> Dict:
        """Detect attack using multiple algorithms"""
        attack_type = self.classify_attack_type(stats)
        anomaly_score = self.calculate_anomaly_score(stats)

        return {
            'attack_detected': attack_type is not None,
            'attack_type': attack_type,
            'anomaly_score': anomaly_score,
            'confidence': self._calculate_confidence(stats)
        }

    def _calculate_confidence(self, stats: Dict) -> float:
        """Calculate confidence level of attack detection"""
        if not stats.get('connected', False):
            return 0.0

        latency = stats.get('avg_latency', 0)
        packet_loss = stats.get('avg_packet_loss', 0)

        # Higher latency/loss = higher confidence
        confidence = 0.0
        if latency > 200:
            confidence += 40
        elif latency > 100:
            confidence += 20
        elif latency > 50:
            confidence += 10

        if packet_loss > 20:
            confidence += 60
        elif packet_loss > 10:
            confidence += 30
        elif packet_loss > 5:
            confidence += 15

        return min(confidence, 100.0)


class TrafficAnalyzer:
    """Analyzes network traffic patterns and connection counts"""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.connection_counts = deque(maxlen=60)  # Last 60 samples
        self.suspicious_ips = set()

    def get_connection_count(self) -> Dict:
        """Get current connection statistics"""
        try:
            connections = psutil.net_connections(kind='inet')

            stats = {
                'total': len(connections),
                'established': 0,
                'listening': 0,
                'syn_sent': 0,
                'syn_recv': 0,
                'time_wait': 0,
                'close_wait': 0,
                'unique_remote_ips': set()
            }

            for conn in connections:
                status = conn.status
                stats['established'] += 1 if status == 'ESTABLISHED' else 0
                stats['listening'] += 1 if status == 'LISTEN' else 0
                stats['syn_sent'] += 1 if status == 'SYN_SENT' else 0
                stats['syn_recv'] += 1 if status == 'SYN_RECV' else 0
                stats['time_wait'] += 1 if status == 'TIME_WAIT' else 0
                stats['close_wait'] += 1 if status == 'CLOSE_WAIT' else 0

                if conn.raddr:
                    stats['unique_remote_ips'].add(conn.raddr.ip)

            stats['unique_remote_ips'] = len(stats['unique_remote_ips'])
            self.connection_counts.append(stats['total'])

            return stats
        except Exception as e:
            print(f"Connection count error: {e}")
            return {'total': 0, 'established': 0}

    def detect_port_scan(self, connection_stats: Dict) -> bool:
        """Detect potential port scanning activity"""
        if not self.config.get('detection', 'enable_connection_tracking', True):
            return False

        # High number of SYN_RECV or unique IPs indicates scanning
        syn_recv = connection_stats.get('syn_recv', 0)
        unique_ips = connection_stats.get('unique_remote_ips', 0)

        threshold = self.config.get('detection', 'suspicious_connection_threshold', 100)

        return syn_recv > 20 or unique_ips > threshold

    def is_connection_anomaly(self) -> bool:
        """Detect anomalous connection counts"""
        if len(self.connection_counts) < 10:
            return False

        avg = statistics.mean(self.connection_counts)
        current = self.connection_counts[-1]

        # Anomaly if current is 3x average
        return current > avg * 3


class DataLogger:
    """Logs attacks and statistics to files"""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.log_dir = Path(config.get('logging', 'log_directory', 'logs'))
        self.log_dir.mkdir(exist_ok=True)

        self.attack_log_file = self.log_dir / config.get('logging', 'attack_log_file', 'attacks.json')
        self.stats_file = self.log_dir / config.get('logging', 'stats_export_file', 'stats.csv')

        self._init_stats_csv()

    def _init_stats_csv(self):
        """Initialize CSV file with headers if it doesn't exist"""
        if not self.stats_file.exists():
            with open(self.stats_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'state', 'latency', 'packet_loss',
                    'connections', 'attack_type', 'anomaly_score'
                ])

    def log_attack(self, attack_info: Dict):
        """Log attack to JSON file"""
        if not self.config.get('features', 'log_attacks', True):
            return

        try:
            # Load existing attacks
            attacks = []
            if self.attack_log_file.exists():
                with open(self.attack_log_file, 'r') as f:
                    attacks = json.load(f)

            # Add new attack
            attack_info['timestamp'] = datetime.now().isoformat()
            attacks.append(attack_info)

            # Save
            with open(self.attack_log_file, 'w') as f:
                json.dump(attacks, f, indent=2)

            print(f"✓ Attack logged to {self.attack_log_file}")
        except Exception as e:
            print(f"Error logging attack: {e}")

    def log_stats(self, stats: Dict):
        """Append statistics to CSV"""
        if not self.config.get('features', 'export_stats', True):
            return

        try:
            with open(self.stats_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().isoformat(),
                    stats.get('state', 'unknown'),
                    stats.get('latency', 0),
                    stats.get('packet_loss', 0),
                    stats.get('connections', 0),
                    stats.get('attack_type', 'none'),
                    stats.get('anomaly_score', 0)
                ])
        except Exception as e:
            print(f"Error logging stats: {e}")

    def get_attack_history(self, hours: int = 24) -> List[Dict]:
        """Get attack history from last N hours"""
        try:
            if self.attack_log_file.exists():
                with open(self.attack_log_file, 'r') as f:
                    attacks = json.load(f)

                cutoff = datetime.now() - timedelta(hours=hours)
                recent = [a for a in attacks if datetime.fromisoformat(a['timestamp']) > cutoff]
                return recent
        except Exception as e:
            print(f"Error reading attack history: {e}")
        return []


class AlertManager:
    """Manages alerts via desktop notifications, Discord, and email"""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.last_alert_time = {}
        self.cooldown = config.get('alerts', 'alert_cooldown_seconds', 300)

    def send_desktop_notification(self, title: str, message: str):
        """Send desktop notification (Linux)"""
        if not self.config.get('features', 'desktop_notifications', True):
            return

        if not self._check_cooldown('desktop'):
            return

        try:
            if platform.system() == "Linux":
                subprocess.run([
                    'notify-send',
                    '-u', 'critical',
                    '-i', 'dialog-warning',
                    title,
                    message
                ], timeout=2)
                print(f"✓ Desktop notification sent: {title}")
        except Exception as e:
            print(f"Desktop notification error: {e}")

    def send_discord_alert(self, message: str, severity: str = "warning"):
        """Send alert to Discord webhook"""
        if not self.config.get('features', 'discord_webhooks', False):
            return

        webhook_url = self.config.get('alerts', 'discord_webhook_url', '')
        if not webhook_url:
            return

        if not self._check_cooldown('discord'):
            return

        try:
            colors = {
                'info': 0x3498db,
                'warning': 0xf39c12,
                'critical': 0xe74c3c
            }

            embed = {
                "embeds": [{
                    "title": "🛡️ DDoS Gotchi Alert",
                    "description": message,
                    "color": colors.get(severity, 0xf39c12),
                    "timestamp": datetime.now().isoformat()
                }]
            }

            response = requests.post(webhook_url, json=embed, timeout=5)
            if response.status_code == 204:
                print("✓ Discord alert sent")
        except Exception as e:
            print(f"Discord alert error: {e}")

    def send_email_alert(self, subject: str, body: str):
        """Send email alert"""
        if not self.config.get('features', 'email_alerts', False):
            return

        if not self._check_cooldown('email'):
            return

        try:
            smtp_server = self.config.get('alerts', 'email_smtp_server', '')
            smtp_port = self.config.get('alerts', 'email_smtp_port', 587)
            email_from = self.config.get('alerts', 'email_from', '')
            email_password = self.config.get('alerts', 'email_password', '')
            email_to = self.config.get('alerts', 'email_to', '')

            if not all([smtp_server, email_from, email_password, email_to]):
                return

            msg = MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = email_to
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email_from, email_password)
            server.send_message(msg)
            server.quit()

            print("✓ Email alert sent")
        except Exception as e:
            print(f"Email alert error: {e}")

    def _check_cooldown(self, alert_type: str) -> bool:
        """Check if alert is in cooldown period"""
        current_time = time.time()
        last_time = self.last_alert_time.get(alert_type, 0)

        if current_time - last_time < self.cooldown:
            return False

        self.last_alert_time[alert_type] = current_time
        return True

    def alert_attack(self, attack_info: Dict):
        """Send all configured alerts for an attack"""
        attack_type = attack_info.get('attack_type', 'Unknown')
        severity = attack_info.get('severity', 'warning')

        title = f"⚠️ DDoS Attack Detected!"
        message = f"Type: {attack_type}\nSeverity: {severity}\nTime: {datetime.now().strftime('%H:%M:%S')}"

        self.send_desktop_notification(title, message)
        self.send_discord_alert(message, severity)
        self.send_email_alert(title, message)


class SoundManager:
    """Manages sound effects for state changes"""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.enabled = config.get('features', 'sound_effects', False)

        if self.enabled:
            try:
                pygame.mixer.init()
                self.sounds = {}
                # Sounds would be loaded here if available
                # self.sounds['alert'] = pygame.mixer.Sound('sounds/alert.wav')
            except Exception as e:
                print(f"Sound initialization error: {e}")
                self.enabled = False

    def play_sound(self, sound_name: str):
        """Play a sound effect"""
        if not self.enabled:
            return

        try:
            if sound_name in self.sounds:
                self.sounds[sound_name].play()
        except Exception as e:
            print(f"Sound playback error: {e}")


class GraphRenderer:
    """Renders real-time graphs for latency and packet loss"""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.latency_data = deque(maxlen=60)  # 60 data points
        self.packet_loss_data = deque(maxlen=60)
        self.connection_data = deque(maxlen=60)

    def add_data_point(self, latency: float, packet_loss: float, connections: int = 0):
        """Add new data point"""
        self.latency_data.append(latency if latency > 0 else 0)
        self.packet_loss_data.append(packet_loss)
        self.connection_data.append(connections)

    def draw_graph(self, surface: pygame.Surface, x: int, y: int, width: int, height: int,
                   data: deque, color: Tuple, max_value: float, title: str, font):
        """Draw a single graph"""
        if not data or len(data) < 2:
            return

        # Draw background
        bg_surface = pygame.Surface((width, height))
        bg_surface.set_alpha(180)
        bg_surface.fill(BLACK)
        surface.blit(bg_surface, (x, y))

        # Draw border
        pygame.draw.rect(surface, color, (x, y, width, height), 2)

        # Draw title
        title_surf = font.render(title, True, color)
        surface.blit(title_surf, (x + 5, y + 5))

        # Draw graph
        points = []
        step = width / (len(data) - 1) if len(data) > 1 else width

        for i, value in enumerate(data):
            px = x + i * step
            # Normalize value to graph height
            normalized = min(value / max_value, 1.0) if max_value > 0 else 0
            py = y + height - (normalized * (height - 30))
            points.append((px, py))

        # Draw line
        if len(points) >= 2:
            pygame.draw.lines(surface, color, False, points, 2)

        # Draw current value
        if data:
            current_val = data[-1]
            val_text = f"{current_val:.1f}"
            val_surf = font.render(val_text, True, color)
            surface.blit(val_surf, (x + width - 60, y + 5))

    def render(self, surface: pygame.Surface, x: int, y: int, width: int, height: int, font):
        """Render all graphs"""
        graph_height = (height - 20) // 2

        # Latency graph
        self.draw_graph(
            surface, x, y, width, graph_height,
            self.latency_data, MATRIX_GREEN, 300.0,
            "LATENCY (ms)", font
        )

        # Packet loss graph
        self.draw_graph(
            surface, x, y + graph_height + 10, width, graph_height,
            self.packet_loss_data, RED, 100.0,
            "PACKET LOSS (%)", font
        )


class MatrixRain:
    """Matrix-style digital rain effect background"""

    def __init__(self, width, height, font):
        self.width = width
        self.height = height
        self.font = font
        self.char_size = font.get_height()
        self.columns = width // (self.char_size - 5)
        self.drops = [random.randint(-height, 0) for _ in range(self.columns)]
        self.chars = []

        self.matrix_chars = list("アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン")
        self.matrix_chars += list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        for _ in range(self.columns):
            column_chars = [random.choice(self.matrix_chars) for _ in range(height // self.char_size + 1)]
            self.chars.append(column_chars)

    def update(self):
        """Update the rain animation"""
        for i in range(self.columns):
            self.drops[i] += 1

            if self.drops[i] * self.char_size > self.height and random.random() > 0.95:
                self.drops[i] = 0
                self.chars[i] = [random.choice(self.matrix_chars) for _ in range(len(self.chars[i]))]

            if random.random() > 0.98:
                char_index = random.randint(0, len(self.chars[i]) - 1)
                self.chars[i][char_index] = random.choice(self.matrix_chars)

    def draw(self, surface):
        """Draw the rain effect"""
        for i in range(self.columns):
            for j in range(len(self.chars[i])):
                y = (self.drops[i] + j) * self.char_size
                if 0 <= y <= self.height:
                    fade = max(0, 1 - (j / 20))
                    color = (0, int(255 * fade), int(65 * fade))

                    char_surface = self.font.render(self.chars[i][j], True, color)
                    x = i * (self.char_size - 5)
                    surface.blit(char_surface, (x, y))


class StateManager:
    """Enhanced state management with configurable thresholds"""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.states = ['happy', 'alert', 'under_attack', 'stressed', 'disconnected']
        self.current_state = 'disconnected'
        self.state_history = deque(maxlen=config.get('monitoring', 'smoothing_window', 5))
        self.last_quote_change = time.time()
        self.current_quote = ""
        self.quote_interval = config.get('ui', 'quote_interval_seconds', 15)

        # Load thresholds from config
        self.thresholds = config.get('thresholds')

    def determine_state(self, stats: Dict) -> str:
        """Determine state based on network statistics"""
        if not stats['connected']:
            new_state = 'disconnected'
        else:
            latency = stats.get('avg_latency', -1)
            packet_loss = stats.get('avg_packet_loss', 0)

            if latency < 0:
                new_state = 'disconnected'
            else:
                # Use configured thresholds
                happy_thresh = self.thresholds.get('happy', {})
                alert_thresh = self.thresholds.get('alert', {})
                attack_thresh = self.thresholds.get('under_attack', {})

                if (latency < happy_thresh.get('max_latency', 10) and
                    packet_loss < happy_thresh.get('max_packet_loss', 1)):
                    new_state = 'happy'
                elif (latency < alert_thresh.get('max_latency', 50) and
                      packet_loss < alert_thresh.get('max_packet_loss', 5)):
                    new_state = 'alert'
                elif (latency < attack_thresh.get('max_latency', 200) and
                      packet_loss < attack_thresh.get('max_packet_loss', 20)):
                    new_state = 'under_attack'
                else:
                    new_state = 'stressed'

        # Add to history for smoothing
        self.state_history.append(new_state)

        # Use most common state in recent history
        state_counts = Counter(self.state_history)
        smoothed_state = state_counts.most_common(1)[0][0]

        # Update current state
        if smoothed_state != self.current_state:
            self.current_state = smoothed_state
            self.current_quote = self.get_random_quote(smoothed_state)
            self.last_quote_change = time.time()
        elif time.time() - self.last_quote_change > self.quote_interval:
            self.current_quote = self.get_random_quote(self.current_state)
            self.last_quote_change = time.time()

        return self.current_state

    def get_face_for_state(self, state: str) -> List[str]:
        """Get ASCII art face for current state"""
        return FACES.get(state, FACES['disconnected'])

    def get_random_quote(self, state: str) -> str:
        """Get a random quote for the state"""
        quotes = QUOTES.get(state, ["..."])
        return random.choice(quotes)

    def get_current_quote(self) -> str:
        """Get the current quote"""
        if not self.current_quote:
            self.current_quote = self.get_random_quote(self.current_state)
        return self.current_quote


class CyberUI:
    """Advanced cyber-themed UI with multi-panel dashboard"""

    def __init__(self, screen, config: ConfigManager, fonts: Dict):
        self.screen = screen
        self.config = config
        self.fonts = fonts

        # Get dimensions from config
        self.width = config.get('ui', 'window_width', 1280)
        self.height = config.get('ui', 'window_height', 800)

        # Get colors from config
        colors = config.get('colors', {})
        self.matrix_green = tuple(colors.get('matrix_green', [0, 255, 65]))
        self.dark_green = tuple(colors.get('dark_green', [0, 128, 32]))

        # Matrix rain
        if config.get('ui', 'matrix_rain_enabled', True):
            self.matrix_rain = MatrixRain(self.width, self.height, fonts['small'])
        else:
            self.matrix_rain = None

        self.frame_count = 0
        self.blink_timer = 0

        # Graph renderer
        self.graph_renderer = GraphRenderer(config)

    def render_background(self):
        """Render background with Matrix rain"""
        self.screen.fill(BLACK)

        if self.matrix_rain:
            self.matrix_rain.update()
            self.matrix_rain.draw(self.screen)

        # Scanlines
        if self.config.get('ui', 'scanlines_enabled', True):
            if self.frame_count % 2 == 0:
                for y in range(0, self.height, 4):
                    pygame.draw.line(self.screen, (0, 20, 5), (0, y), (self.width, y), 1)

    def render_header(self, ip_info: Dict):
        """Render header with IP information"""
        y_pos = 10
        font = self.fonts['medium']

        # Title
        title = "[ DDOS GOTCHI - ADVANCED DETECTION SYSTEM ]"
        title_surf = font.render(title, True, self.matrix_green)
        title_rect = title_surf.get_rect(center=(self.width // 2, y_pos))
        self.screen.blit(title_surf, title_rect)

        y_pos += 30

        # IP Information
        local_ip = ip_info.get('local_ip', 'N/A')
        public_ip = ip_info.get('public_ip', 'N/A')

        ip_text = f"LOCAL IP: {local_ip}  |  PUBLIC IP: {public_ip}"
        ip_surf = self.fonts['small'].render(ip_text, True, self.matrix_green)
        ip_rect = ip_surf.get_rect(center=(self.width // 2, y_pos))
        self.screen.blit(ip_surf, ip_rect)

    def render_gotchi_panel(self, face: List[str], state: str, x: int, y: int, width: int, height: int):
        """Render the gotchi face panel"""
        # Background
        bg_surface = pygame.Surface((width, height))
        bg_surface.set_alpha(200)
        bg_surface.fill(BLACK)
        self.screen.blit(bg_surface, (x, y))

        # Border
        border_color = self.matrix_green if state != 'disconnected' else RED
        pygame.draw.rect(self.screen, border_color, (x, y, width, height), 3)
        pygame.draw.rect(self.screen, self.dark_green, (x - 2, y - 2, width + 4, height + 4), 1)

        # Render face with blink
        face_to_render = face.copy()
        if state == 'happy' and self.blink_timer > 28 and self.config.get('ui', 'blink_animation_enabled', True):
            face_to_render[0] = "  (⌐-_-)  "

        face_y = y + height // 2 - 30
        for line in face_to_render:
            text_surf = self.fonts['big'].render(line, True, border_color)
            text_rect = text_surf.get_rect(center=(x + width // 2, face_y))
            self.screen.blit(text_surf, text_rect)
            face_y += 30

        # State label
        state_text = f"[ {state.upper().replace('_', ' ')} ]"
        state_surf = self.fonts['medium'].render(state_text, True, border_color)
        state_rect = state_surf.get_rect(center=(x + width // 2, y + height - 20))
        self.screen.blit(state_surf, state_rect)

        # Glitch effect
        if state in ['under_attack', 'stressed'] and random.random() > 0.9 and self.config.get('ui', 'glitch_effects_enabled', True):
            glitch_surface = pygame.Surface((width, height))
            glitch_surface.set_alpha(50)
            glitch_surface.fill((random.randint(0, 255), 0, 0))
            self.screen.blit(glitch_surface, (x + random.randint(-5, 5), y + random.randint(-5, 5)))

    def render_stats_panel(self, stats: Dict, attack_info: Dict, x: int, y: int, width: int, height: int):
        """Render statistics panel"""
        # Background
        bg_surface = pygame.Surface((width, height))
        bg_surface.set_alpha(200)
        bg_surface.fill(BLACK)
        self.screen.blit(bg_surface, (x, y))

        # Border
        pygame.draw.rect(self.screen, self.matrix_green, (x, y, width, height), 2)

        # Title
        title_surf = self.fonts['medium'].render("NETWORK STATISTICS", True, self.matrix_green)
        self.screen.blit(title_surf, (x + 10, y + 10))

        # Stats
        y_offset = y + 40
        font = self.fonts['small']

        stats_lines = [
            f"Status: {'CONNECTED' if stats.get('connected') else 'DISCONNECTED'}",
            f"Network: {stats.get('ssid', 'N/A')}",
            f"Gateway: {stats.get('gateway', 'N/A')}",
            f"Interface: {stats.get('interface', 'N/A')}",
            "",
            f"Latency: {stats.get('latency', -1):.1f} ms",
            f"Avg Latency: {stats.get('avg_latency', -1):.1f} ms",
            f"Baseline: {stats.get('baseline_latency', 0):.1f} ms",
            "",
            f"Packet Loss: {stats.get('packet_loss', 0):.1f}%",
            f"Avg Packet Loss: {stats.get('avg_packet_loss', 0):.1f}%",
            "",
            f"Connections: {stats.get('total_connections', 0)}",
            f"Established: {stats.get('established_connections', 0)}",
            "",
            f"Anomaly Score: {attack_info.get('anomaly_score', 0):.1f}",
            f"Confidence: {attack_info.get('confidence', 0):.1f}%"
        ]

        for line in stats_lines:
            if line:
                # Color coding
                color = self.matrix_green
                if 'Latency' in line and stats.get('latency', 0) > 100:
                    color = ORANGE
                elif 'Loss' in line and stats.get('packet_loss', 0) > 10:
                    color = RED
                elif 'Anomaly' in line and attack_info.get('anomaly_score', 0) > 50:
                    color = RED

                text_surf = font.render(line, True, color)
                self.screen.blit(text_surf, (x + 15, y_offset))
            y_offset += 20

    def render_attack_panel(self, attack_info: Dict, recent_attacks: List, x: int, y: int, width: int, height: int):
        """Render attack information panel"""
        # Background
        bg_surface = pygame.Surface((width, height))
        bg_surface.set_alpha(200)
        bg_surface.fill(BLACK)
        self.screen.blit(bg_surface, (x, y))

        # Border
        border_color = RED if attack_info.get('attack_detected') else self.matrix_green
        pygame.draw.rect(self.screen, border_color, (x, y, width, height), 2)

        # Title
        title_surf = self.fonts['medium'].render("ATTACK DETECTION", True, border_color)
        self.screen.blit(title_surf, (x + 10, y + 10))

        y_offset = y + 40
        font = self.fonts['small']

        # Current attack info
        if attack_info.get('attack_detected'):
            lines = [
                f"STATUS: ⚠️  ATTACK DETECTED",
                f"Type: {attack_info.get('attack_type', 'Unknown')}",
                f"Confidence: {attack_info.get('confidence', 0):.1f}%",
                f"Anomaly Score: {attack_info.get('anomaly_score', 0):.1f}",
                "",
                "RECENT ATTACKS (24h):"
            ]

            for line in lines[:4]:
                text_surf = font.render(line, True, RED)
                self.screen.blit(text_surf, (x + 15, y_offset))
                y_offset += 20
        else:
            text_surf = font.render("STATUS: ✓ NO ATTACK DETECTED", True, self.matrix_green)
            self.screen.blit(text_surf, (x + 15, y_offset))
            y_offset += 40

            text_surf = font.render("RECENT ATTACKS (24h):", True, self.matrix_green)
            self.screen.blit(text_surf, (x + 15, y_offset))

        y_offset += 25

        # Show recent attacks
        for attack in recent_attacks[:5]:  # Show last 5
            time_str = attack.get('timestamp', '')[:19] if 'timestamp' in attack else 'Unknown'
            attack_type = attack.get('attack_type', 'Unknown')[:25]
            line = f"{time_str} - {attack_type}"
            text_surf = font.render(line, True, ORANGE)
            self.screen.blit(text_surf, (x + 15, y_offset))
            y_offset += 18

            if y_offset > y + height - 20:
                break

    def render_graph_panel(self, x: int, y: int, width: int, height: int):
        """Render real-time graphs"""
        # Background
        bg_surface = pygame.Surface((width, height))
        bg_surface.set_alpha(200)
        bg_surface.fill(BLACK)
        self.screen.blit(bg_surface, (x, y))

        # Border
        pygame.draw.rect(self.screen, self.matrix_green, (x, y, width, height), 2)

        # Title
        title_surf = self.fonts['medium'].render("REAL-TIME METRICS", True, self.matrix_green)
        self.screen.blit(title_surf, (x + 10, y + 10))

        # Render graphs
        self.graph_renderer.render(self.screen, x + 10, y + 40, width - 20, height - 50, self.fonts['small'])

    def render_quote(self, quote: str, y: int):
        """Render quote at bottom"""
        max_width = self.width - 100
        words = quote.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = self.fonts['medium'].render(test_line, True, self.matrix_green)
            if test_surface.get_width() > max_width:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
            else:
                current_line.append(word)

        if current_line:
            lines.append(' '.join(current_line))

        # Render lines
        y_offset = y
        for line in lines:
            text_surf = self.fonts['medium'].render(f'"{line}"', True, self.matrix_green)
            text_rect = text_surf.get_rect(center=(self.width // 2, y_offset))
            self.screen.blit(text_surf, text_rect)
            y_offset += 25

    def render_footer(self, runtime: int, total_attacks: int):
        """Render footer with runtime and attack count"""
        runtime_text = f"Runtime: {runtime//3600:02d}:{(runtime%3600)//60:02d}:{runtime%60:02d}  |  Total Attacks: {total_attacks}  |  Press ESC to exit, SPACE to change quote"
        text_surf = self.fonts['small'].render(runtime_text, True, self.dark_green)
        self.screen.blit(text_surf, (10, self.height - 20))

    def update(self):
        """Update UI animations"""
        self.frame_count += 1
        self.blink_timer = (self.blink_timer + 1) % 30


class DDoSGotchi:
    """Main application with enhanced features"""

    def __init__(self):
        pygame.init()

        # Load configuration
        self.config = ConfigManager()

        # Apply config to global dimensions
        global WINDOW_WIDTH, WINDOW_HEIGHT, FPS
        WINDOW_WIDTH = self.config.get('ui', 'window_width', 1280)
        WINDOW_HEIGHT = self.config.get('ui', 'window_height', 800)
        FPS = self.config.get('ui', 'fps', 30)

        # Set up display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("DDoS Gotchi - Advanced Detection System")

        # Load fonts
        self.fonts = self._load_fonts()

        # Initialize components
        self.ip_detector = IPDetector()
        self.network_monitor = NetworkMonitor(self.config)
        self.attack_detector = AttackDetector(self.config)
        self.traffic_analyzer = TrafficAnalyzer(self.config)
        self.data_logger = DataLogger(self.config)
        self.alert_manager = AlertManager(self.config)
        self.sound_manager = SoundManager(self.config)
        self.state_manager = StateManager(self.config)
        self.ui = CyberUI(self.screen, self.config, self.fonts)

        # Threading
        self.running = True
        self.stats = self._init_default_stats()
        self.monitor_thread = threading.Thread(target=self.monitor_network, daemon=True)
        self.monitor_thread.start()

        # Statistics
        self.start_time = time.time()
        self.total_attacks = 0
        self.last_state = 'disconnected'
        self.last_attack_log = 0
        self.attack_log_cooldown = 10  # Log attack every 10 seconds max

        # IP info
        self.ip_info = {
            'local_ip': 'Detecting...',
            'public_ip': 'Detecting...'
        }

        # Start IP detection thread
        threading.Thread(target=self.update_ip_info, daemon=True).start()

        self.clock = pygame.time.Clock()

        print("=" * 60)
        print("DDoS Gotchi - Advanced Detection System")
        print("=" * 60)
        print(f"✓ Configuration loaded")
        print(f"✓ Window size: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        print(f"✓ Gateway: {self.network_monitor.gateway}")
        print(f"✓ Network: {self.network_monitor.target_network}.0/24")
        print(f"✓ Logging enabled: {self.config.get('features', 'log_attacks', True)}")
        print(f"✓ Desktop notifications: {self.config.get('features', 'desktop_notifications', True)}")
        print("=" * 60)

    def _load_fonts(self) -> Dict:
        """Load fonts for UI"""
        try:
            return {
                'small': pygame.font.Font(pygame.font.match_font('couriernew', 'courier', 'monospace'), 12),
                'medium': pygame.font.Font(pygame.font.match_font('couriernew', 'courier', 'monospace'), 16),
                'big': pygame.font.Font(pygame.font.match_font('couriernew', 'courier', 'monospace'), 24)
            }
        except:
            return {
                'small': pygame.font.Font(None, 12),
                'medium': pygame.font.Font(None, 16),
                'big': pygame.font.Font(None, 24)
            }

    def _init_default_stats(self) -> Dict:
        """Initialize default stats"""
        return {
            'connected': False,
            'ssid': 'Initializing...',
            'latency': -1,
            'packet_loss': 0,
            'avg_latency': -1,
            'avg_packet_loss': 0,
            'interface': None,
            'gateway': self.network_monitor.gateway,
            'baseline_latency': 0,
            'baseline_packet_loss': 0,
            'total_connections': 0,
            'established_connections': 0
        }

    def update_ip_info(self):
        """Update IP information in background"""
        while self.running:
            try:
                local_ip = self.ip_detector.get_local_ip()
                public_ip = self.ip_detector.get_public_ip()

                if local_ip:
                    self.ip_info['local_ip'] = local_ip
                if public_ip:
                    self.ip_info['public_ip'] = public_ip

                time.sleep(60)  # Update every minute
            except Exception as e:
                print(f"IP update error: {e}")
                time.sleep(60)

    def monitor_network(self):
        """Background thread for network monitoring"""
        while self.running:
            try:
                # Check connection
                self.network_monitor.check_wifi_connection()

                # Get network stats
                net_stats = self.network_monitor.get_network_stats()

                # Get connection stats
                conn_stats = self.traffic_analyzer.get_connection_count()
                net_stats['total_connections'] = conn_stats.get('total', 0)
                net_stats['established_connections'] = conn_stats.get('established', 0)

                self.stats = net_stats

                # Sleep
                time.sleep(self.config.get('monitoring', 'check_interval_seconds', 2))
            except Exception as e:
                print(f"Monitor thread error: {e}")
                time.sleep(5)

    def run(self):
        """Main game loop"""
        print("Monitoring network for DDoS attacks...")

        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        self.state_manager.last_quote_change = 0

            # Determine state
            state = self.state_manager.determine_state(self.stats)

            # Detect attacks
            attack_info = self.attack_detector.detect_attack_pattern(self.stats)

            # Track attacks
            if state in ['under_attack', 'stressed'] and self.last_state not in ['under_attack', 'stressed']:
                self.total_attacks += 1

                # Log attack
                current_time = time.time()
                if current_time - self.last_attack_log > self.attack_log_cooldown:
                    attack_data = {
                        'state': state,
                        'attack_type': attack_info.get('attack_type', 'Unknown'),
                        'latency': self.stats.get('avg_latency', 0),
                        'packet_loss': self.stats.get('avg_packet_loss', 0),
                        'anomaly_score': attack_info.get('anomaly_score', 0),
                        'confidence': attack_info.get('confidence', 0),
                        'severity': 'critical' if state == 'stressed' else 'warning'
                    }

                    self.data_logger.log_attack(attack_data)
                    self.alert_manager.alert_attack(attack_data)
                    self.last_attack_log = current_time

            self.last_state = state

            # Update graph data
            self.ui.graph_renderer.add_data_point(
                self.stats.get('latency', 0),
                self.stats.get('packet_loss', 0),
                self.stats.get('total_connections', 0)
            )

            # Log stats periodically
            if int(time.time()) % 60 == 0:  # Every minute
                log_data = {
                    'state': state,
                    'latency': self.stats.get('latency', 0),
                    'packet_loss': self.stats.get('packet_loss', 0),
                    'connections': self.stats.get('total_connections', 0),
                    'attack_type': attack_info.get('attack_type', 'none'),
                    'anomaly_score': attack_info.get('anomaly_score', 0)
                }
                self.data_logger.log_stats(log_data)

            # Get visuals
            face = self.state_manager.get_face_for_state(state)
            quote = self.state_manager.get_current_quote()
            recent_attacks = self.data_logger.get_attack_history(24)

            # Render everything
            self.ui.render_background()

            # Header
            self.ui.render_header(self.ip_info)

            # Multi-panel layout
            panel_y = 70
            left_width = 400
            right_width = WINDOW_WIDTH - left_width - 30

            # Left column
            # Gotchi panel
            self.ui.render_gotchi_panel(face, state, 10, panel_y, left_width, 250)

            # Stats panel
            self.ui.render_stats_panel(self.stats, attack_info, 10, panel_y + 260, left_width, 400)

            # Right column
            # Graph panel
            self.ui.render_graph_panel(left_width + 20, panel_y, right_width, 320)

            # Attack panel
            self.ui.render_attack_panel(attack_info, recent_attacks, left_width + 20, panel_y + 330, right_width, 330)

            # Quote
            self.ui.render_quote(quote, WINDOW_HEIGHT - 70)

            # Footer
            runtime = int(time.time() - self.start_time)
            self.ui.render_footer(runtime, self.total_attacks)

            # Update animations
            self.ui.update()

            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """Entry point"""
    try:
        gotchi = DDoSGotchi()
        gotchi.run()
    except KeyboardInterrupt:
        print("\nDDoS Gotchi shutting down...")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
