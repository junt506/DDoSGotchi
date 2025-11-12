#!/usr/bin/env python3
"""
DDoS Gotchi v3.0 - Backend Server for Electron HUD
Real-time network monitoring with WebSocket communication
"""

import asyncio
import json
import psutil
import netifaces
import time
import os
from collections import defaultdict, deque
from datetime import datetime
import websockets
import subprocess
import re
from backend.threat_intelligence import ThreatIntelligence

class DDoSGotchiBackend:
    def __init__(self):
        # Network monitoring data
        self.connection_counts = defaultdict(int)
        self.recent_connections = []
        self.seen_ips = set()
        self.last_refresh = time.time()

        # Performance metrics
        self.latency_data = deque(maxlen=100)
        self.packet_loss_data = deque(maxlen=100)

        # Lab Mode - Sensitive detection for isolated testing environments
        self.lab_mode = os.environ.get('LAB_MODE', '').lower() in ('true', '1', 'yes')

        # Attack detection thresholds (adjusted for lab mode)
        if self.lab_mode:
            self.attack_threshold = 5  # connections per IP (lab mode: very sensitive)
            self.total_connections_threshold = 10  # total connections
            self.suspicious_threshold = 3  # warn at 3 connections per IP
        else:
            self.attack_threshold = 50  # connections per IP (production)
            self.total_connections_threshold = 100  # total connections
            self.suspicious_threshold = 20  # warn at 20 connections per IP

        # Timing
        self.last_update = time.time()
        self.connection_check_interval = 1.0
        self.refresh_interval = 15.0

        # Traffic statistics tracking
        self.last_net_io = psutil.net_io_counters()
        self.last_net_io_time = time.time()
        self.bytes_recv_per_sec = 0
        self.bytes_sent_per_sec = 0
        self.packets_recv_per_sec = 0
        self.packets_sent_per_sec = 0

        # Threat Intelligence (optional API keys from environment)
        abuseipdb_key = os.environ.get('ABUSEIPDB_API_KEY')
        enable_greynoise = os.environ.get('ENABLE_GREYNOISE', '').lower() in ('true', '1', 'yes')
        self.threat_intel = ThreatIntelligence(
            abuseipdb_key=abuseipdb_key,
            enable_greynoise=enable_greynoise
        )
        self.ip_threats = {}  # IP -> threat data
        self.threat_check_queue = asyncio.Queue()
        self.last_threat_check = time.time()

    def get_local_ip(self):
        """Get the local IP address"""
        try:
            interfaces = netifaces.interfaces()
            for interface in interfaces:
                if interface.startswith(('lo', 'docker', 'veth')):
                    continue

                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr_info in addrs[netifaces.AF_INET]:
                        ip = addr_info.get('addr')
                        if ip and not ip.startswith('127.'):
                            return ip
        except Exception as e:
            print(f"Error getting local IP: {e}")

        return "127.0.0.1"

    def get_gateway_ip(self):
        """Get the default gateway IP address"""
        try:
            gateways = netifaces.gateways()
            if 'default' in gateways and netifaces.AF_INET in gateways['default']:
                return gateways['default'][netifaces.AF_INET][0]
        except Exception as e:
            print(f"Error getting gateway IP: {e}")

        return "0.0.0.0"

    def get_network_address(self):
        """Get the network address (IP/CIDR)"""
        try:
            interfaces = netifaces.interfaces()
            for interface in interfaces:
                if interface.startswith(('lo', 'docker', 'veth')):
                    continue

                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr_info in addrs[netifaces.AF_INET]:
                        ip = addr_info.get('addr')
                        netmask = addr_info.get('netmask')

                        if ip and netmask and not ip.startswith('127.'):
                            # Calculate CIDR notation
                            cidr = sum([bin(int(x)).count('1') for x in netmask.split('.')])

                            # Calculate network address
                            ip_parts = [int(x) for x in ip.split('.')]
                            mask_parts = [int(x) for x in netmask.split('.')]
                            network_parts = [str(ip_parts[i] & mask_parts[i]) for i in range(4)]
                            network = '.'.join(network_parts)

                            return f"{network}/{cidr}"
        except Exception as e:
            print(f"Error getting network address: {e}")

        return "0.0.0.0/24"

    def get_network_info(self):
        """Get complete network information"""
        return {
            'local_ip': self.get_local_ip(),
            'gateway': self.get_gateway_ip(),
            'network': self.get_network_address()
        }

    def measure_latency(self):
        """Measure network latency using ping"""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '1', '8.8.8.8'],
                capture_output=True,
                text=True,
                timeout=2
            )

            if result.returncode == 0:
                match = re.search(r'time=(\d+\.?\d*)', result.stdout)
                if match:
                    return float(match.group(1))
        except Exception as e:
            print(f"Error measuring latency: {e}")

        return 0.0

    def measure_packet_loss(self):
        """Measure packet loss using ping"""
        try:
            result = subprocess.run(
                ['ping', '-c', '10', '-W', '1', '8.8.8.8'],
                capture_output=True,
                text=True,
                timeout=12
            )

            if result.returncode == 0:
                match = re.search(r'(\d+)% packet loss', result.stdout)
                if match:
                    return float(match.group(1))
        except Exception as e:
            print(f"Error measuring packet loss: {e}")

        return 0.0

    def get_network_connections(self):
        """Get all active network connections with protocol information"""
        connections = []
        protocol_counts = {'TCP': 0, 'UDP': 0, 'ICMP': 0, 'OTHER': 0}
        incoming_count = 0
        outgoing_count = 0

        try:
            import socket
            local_ips = self._get_all_local_ips()

            for conn in psutil.net_connections(kind='inet'):
                # In lab mode, monitor ALL connection states (including SYN floods, half-open)
                # In normal mode, only monitor ESTABLISHED connections
                if self.lab_mode:
                    # Monitor everything with remote address (SYN_SENT, SYN_RECV, ESTABLISHED, etc.)
                    should_monitor = conn.raddr is not None
                else:
                    # Original behavior - only ESTABLISHED connections
                    should_monitor = conn.status == 'ESTABLISHED' and conn.raddr

                if should_monitor:
                    # Determine protocol type
                    protocol = 'OTHER'
                    if conn.type == socket.SOCK_STREAM:
                        protocol = 'TCP'
                        protocol_counts['TCP'] += 1
                    elif conn.type == socket.SOCK_DGRAM:
                        protocol = 'UDP'
                        protocol_counts['UDP'] += 1
                    elif conn.type == socket.SOCK_RAW:
                        protocol = 'ICMP'
                        protocol_counts['ICMP'] += 1
                    else:
                        protocol_counts['OTHER'] += 1

                    # Determine direction (incoming vs outgoing)
                    is_incoming = False
                    if conn.laddr and conn.raddr:
                        # Incoming: remote IP is connecting TO us (we're listening)
                        # Common listening ports: 22, 80, 443, 8080, etc.
                        if conn.laddr.port < 1024 or conn.status in ('LISTEN', 'SYN_RECV'):
                            is_incoming = True
                            incoming_count += 1
                        else:
                            outgoing_count += 1

                    connections.append({
                        'local_ip': conn.laddr.ip if conn.laddr else '',
                        'local_port': conn.laddr.port if conn.laddr else 0,
                        'remote_ip': conn.raddr.ip if conn.raddr else '',
                        'remote_port': conn.raddr.port if conn.raddr else 0,
                        'status': conn.status,
                        'protocol': protocol,
                        'is_incoming': is_incoming
                    })
        except Exception as e:
            print(f"Error getting connections: {e}")

        return connections, protocol_counts, incoming_count, outgoing_count

    def _get_all_local_ips(self):
        """Get all local IP addresses for direction detection"""
        local_ips = set(['127.0.0.1', 'localhost'])
        try:
            import netifaces
            for interface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr_info in addrs[netifaces.AF_INET]:
                        ip = addr_info.get('addr')
                        if ip:
                            local_ips.add(ip)
        except:
            pass
        return local_ips

    def detect_attack(self, connections):
        """Detect potential DDoS attacks with lab mode sensitivity"""
        # Count connections per IP (incoming only for attack detection)
        ip_counts = defaultdict(int)
        incoming_ip_counts = defaultdict(int)

        for conn in connections:
            remote_ip = conn['remote_ip']
            if remote_ip:
                ip_counts[remote_ip] += 1
                if conn.get('is_incoming', False):
                    incoming_ip_counts[remote_ip] += 1

        # Check for attack patterns
        attack_detected = False
        suspicious_detected = False
        attack_ips = []
        suspicious_ips = []

        # Per-IP threshold detection
        for ip, count in incoming_ip_counts.items():
            if count >= self.attack_threshold:
                attack_detected = True
                attack_ips.append(ip)
            elif count >= self.suspicious_threshold:
                suspicious_detected = True
                suspicious_ips.append(ip)

        # Total connections threshold
        total_incoming = sum(incoming_ip_counts.values())
        if total_incoming >= self.total_connections_threshold:
            attack_detected = True

        # Lab mode: Additional detection heuristics
        if self.lab_mode:
            # Multiple IPs from same subnet attacking (botnet pattern)
            subnet_counts = defaultdict(int)
            for ip in incoming_ip_counts.keys():
                subnet = '.'.join(ip.split('.')[:3])  # /24 subnet
                subnet_counts[subnet] += 1

            # If 3+ IPs from same subnet, likely botnet
            for subnet, count in subnet_counts.items():
                if count >= 3:
                    attack_detected = True
                    if self.lab_mode:
                        print(f"🚨 LAB MODE: Botnet pattern detected from subnet {subnet}.0/24 ({count} IPs)")

        # Determine threat level
        if attack_detected:
            threat_level = 'critical'
        elif suspicious_detected:
            threat_level = 'warning'
        elif len(connections) > 5:
            threat_level = 'elevated'
        else:
            threat_level = 'normal'

        return {
            'attack_detected': attack_detected,
            'suspicious_detected': suspicious_detected,
            'attack_ips': attack_ips,
            'suspicious_ips': suspicious_ips,
            'ip_counts': dict(ip_counts),
            'incoming_ip_counts': dict(incoming_ip_counts),
            'threat_level': threat_level
        }

    async def check_threats(self, unique_ips):
        """Check unique IPs for threats (rate-limited, async)"""
        # Only check new IPs we haven't checked yet
        ips_to_check = [ip for ip in unique_ips if ip not in self.ip_threats]

        # Limit to 1 new check per iteration to respect API rate limits
        ips_to_check = ips_to_check[:1]

        if ips_to_check:
            # Check IPs sequentially to respect rate limits
            results = []
            for ip in ips_to_check:
                try:
                    result = await self.threat_intel.check_ip(ip)
                    results.append(result)
                except Exception as e:
                    results.append(e)

            # Store results and report only threats (benign IPs not logged to reduce spam)
            for ip, result in zip(ips_to_check, results):
                if isinstance(result, Exception):
                    continue  # Silently skip errors

                self.ip_threats[ip] = result

                # Only log threats - keep console clean
                if result.get('is_threat'):
                    threat_level = result.get('threat_level', 'unknown')
                    confidence = result.get('confidence', 0)
                    sources = ', '.join(result.get('sources', []))
                    tags = ', '.join(result.get('tags', []))
                    print(f"\n⚠️  THREAT DETECTED: {ip}")
                    print(f"   Level: {threat_level.upper()} | Confidence: {confidence}%")
                    print(f"   Sources: {sources}")
                    if tags:
                        print(f"   Tags: {tags}")
                    print()

        # Clean up old entries (keep cache fresh)
        if len(self.ip_threats) > 500:
            # Remove oldest 100 entries
            ips_to_remove = list(self.ip_threats.keys())[:100]
            for ip in ips_to_remove:
                del self.ip_threats[ip]

    def update_traffic_stats(self):
        """Update network traffic statistics (bytes/sec, packets/sec)"""
        try:
            current_io = psutil.net_io_counters()
            current_time = time.time()
            time_delta = current_time - self.last_net_io_time

            if time_delta > 0:
                # Calculate bytes per second
                self.bytes_recv_per_sec = (current_io.bytes_recv - self.last_net_io.bytes_recv) / time_delta
                self.bytes_sent_per_sec = (current_io.bytes_sent - self.last_net_io.bytes_sent) / time_delta

                # Calculate packets per second
                self.packets_recv_per_sec = (current_io.packets_recv - self.last_net_io.packets_recv) / time_delta
                self.packets_sent_per_sec = (current_io.packets_sent - self.last_net_io.packets_sent) / time_delta

                # Lab mode: Log high traffic rates
                if self.lab_mode and self.packets_recv_per_sec > 100:
                    print(f"📊 LAB MODE: High incoming traffic - {self.packets_recv_per_sec:.0f} packets/sec, {self.bytes_recv_per_sec/1024:.1f} KB/sec")

            self.last_net_io = current_io
            self.last_net_io_time = current_time

        except Exception as e:
            print(f"Error updating traffic stats: {e}")

    async def monitor_network(self):
        """Main network monitoring loop"""
        while True:
            current_time = time.time()

            # Update traffic statistics
            self.update_traffic_stats()

            # Get network connections with protocol information and direction
            connections, protocol_counts, incoming_count, outgoing_count = self.get_network_connections()

            # Detect attacks
            attack_info = self.detect_attack(connections)

            # Get unique IPs
            unique_ips = list(set(c['remote_ip'] for c in connections if c['remote_ip']))

            # Check for threats (rate-limited, async)
            await self.check_threats(unique_ips)

            # Count malicious IPs
            malicious_ips = [ip for ip, threat_data in self.ip_threats.items()
                            if threat_data.get('is_threat', False) and ip in unique_ips]

            # Get new connections (not seen before)
            new_connections = []
            for conn in connections:
                remote_ip = conn['remote_ip']
                if remote_ip and remote_ip not in self.seen_ips:
                    self.seen_ips.add(remote_ip)
                    new_connections.append(conn)

            # Store recent connections for display
            if new_connections:
                self.recent_connections = new_connections[-15:]

            # Reset seen IPs periodically
            if current_time - self.last_refresh >= self.refresh_interval:
                self.seen_ips.clear()
                self.last_refresh = current_time

            # Measure latency and packet loss (every 10 seconds to avoid overhead)
            if current_time - self.last_update >= 10.0:
                latency = self.measure_latency()
                packet_loss = self.measure_packet_loss()

                self.latency_data.append(latency)
                self.packet_loss_data.append(packet_loss)
                self.last_update = current_time

            # Lab mode: Enhanced logging
            if self.lab_mode and attack_info['attack_detected']:
                print(f"\n🚨 LAB MODE - ATTACK DETECTED!")
                print(f"   Incoming connections: {incoming_count}")
                print(f"   Attack IPs: {', '.join(attack_info['attack_ips'])}")
                print(f"   Suspicious IPs: {', '.join(attack_info.get('suspicious_ips', []))}")
                print(f"   Threat level: {attack_info['threat_level'].upper()}\n")

            # Prepare data to send
            data = {
                'timestamp': datetime.now().isoformat(),
                'total_connections': len(connections),
                'unique_ips': len(unique_ips),
                'incoming_connections': incoming_count,
                'outgoing_connections': outgoing_count,
                'latency': self.latency_data[-1] if self.latency_data else 0,
                'packet_loss': self.packet_loss_data[-1] if self.packet_loss_data else 0,
                'attack_detected': attack_info['attack_detected'],
                'suspicious_detected': attack_info.get('suspicious_detected', False),
                'attack_ips': attack_info['attack_ips'],
                'suspicious_ips': attack_info.get('suspicious_ips', []),
                'threat_level': attack_info['threat_level'],
                'connections': connections,  # All active connections
                'recent_connections': self.recent_connections,
                'network_info': self.get_network_info(),
                'protocol_distribution': protocol_counts,
                'traffic_stats': {
                    'bytes_recv_per_sec': self.bytes_recv_per_sec,
                    'bytes_sent_per_sec': self.bytes_sent_per_sec,
                    'packets_recv_per_sec': self.packets_recv_per_sec,
                    'packets_sent_per_sec': self.packets_sent_per_sec
                },
                'threats': {
                    'malicious_count': len(malicious_ips),
                    'malicious_ips': malicious_ips,
                    'ip_threat_data': self.ip_threats
                },
                'lab_mode': self.lab_mode
            }

            # Store for WebSocket broadcast
            self.current_data = data

            await asyncio.sleep(self.connection_check_interval)

    async def websocket_handler(self, websocket):
        """Handle WebSocket connections from Electron frontend"""
        print(f"✓ Client connected: {websocket.remote_address}")

        try:
            # Send initial data
            if hasattr(self, 'current_data'):
                await websocket.send(json.dumps(self.current_data))

            # Keep connection alive and send updates
            while True:
                if hasattr(self, 'current_data'):
                    await websocket.send(json.dumps(self.current_data))

                await asyncio.sleep(1.0)

        except websockets.exceptions.ConnectionClosed:
            print(f"✗ Client disconnected: {websocket.remote_address}")
        except Exception as e:
            print(f"WebSocket error: {e}")

    async def start_server(self):
        """Start the WebSocket server"""
        # Initialize threat intelligence session
        await self.threat_intel.init_session()

        try:
            # Start network monitoring in background
            asyncio.create_task(self.monitor_network())

            # Start WebSocket server
            print("🛡️  DDoS Gotchi Backend v3.0 - HUD Edition")
            print("=" * 60)
            print("WebSocket server starting on ws://localhost:8765")
            print("Waiting for Electron frontend to connect...")
            print("")

            # Detection Mode Status
            if self.lab_mode:
                print("🔬 LAB MODE ENABLED - Sensitive Detection Active")
                print(f"   Attack threshold: {self.attack_threshold} connections/IP")
                print(f"   Suspicious threshold: {self.suspicious_threshold} connections/IP")
                print(f"   Total connections threshold: {self.total_connections_threshold}")
                print(f"   Monitoring ALL connection states (SYN floods, half-open, etc.)")
                print(f"   Botnet pattern detection: 3+ IPs from same subnet")
                print("")
            else:
                print("🌐 Production Mode - Standard Thresholds")
                print(f"   Attack threshold: {self.attack_threshold} connections/IP")
                print(f"   Total connections threshold: {self.total_connections_threshold}")
                print(f"   Set LAB_MODE=true for sensitive detection")
                print("")

            print("🛡️  Threat Intelligence Status:")
            if self.threat_intel.enable_greynoise:
                print(f"   ✓ GreyNoise: Enabled (set via ENABLE_GREYNOISE)")
            else:
                print(f"   ℹ GreyNoise: Disabled (set ENABLE_GREYNOISE=true to enable)")
            if self.threat_intel.abuseipdb_key:
                print(f"   ✓ AbuseIPDB: Enabled (API key configured)")
            else:
                print(f"   ℹ AbuseIPDB: Disabled (set ABUSEIPDB_API_KEY to enable)")
            print("=" * 60)

            async with websockets.serve(self.websocket_handler, "localhost", 8765):
                await asyncio.Future()  # run forever
        finally:
            # Clean up threat intelligence session
            await self.threat_intel.close()
            print("\n✓ Backend shutdown complete")

if __name__ == "__main__":
    backend = DDoSGotchiBackend()
    try:
        asyncio.run(backend.start_server())
    except KeyboardInterrupt:
        print("\n✓ Shutting down gracefully...")
