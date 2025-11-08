#!/usr/bin/env python3
"""
DDoS Gotchi v3.0 - Backend Server for Electron
Real-time network monitoring with WebSocket communication
"""

import asyncio
import json
import psutil
import netifaces
import time
from collections import defaultdict, deque
from datetime import datetime
import websockets
import subprocess
import re

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

        # Attack detection
        self.attack_threshold = 50  # connections per IP
        self.total_connections_threshold = 100

        # Timing
        self.last_update = time.time()
        self.connection_check_interval = 1.0
        self.refresh_interval = 15.0

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
        """Get all active network connections"""
        connections = []
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED' and conn.raddr:
                    connections.append({
                        'local_ip': conn.laddr.ip if conn.laddr else '',
                        'local_port': conn.laddr.port if conn.laddr else 0,
                        'remote_ip': conn.raddr.ip if conn.raddr else '',
                        'remote_port': conn.raddr.port if conn.raddr else 0,
                        'status': conn.status
                    })
        except Exception as e:
            print(f"Error getting connections: {e}")

        return connections

    def detect_attack(self, connections):
        """Detect potential DDoS attacks"""
        # Count connections per IP
        ip_counts = defaultdict(int)
        for conn in connections:
            remote_ip = conn['remote_ip']
            if remote_ip:
                ip_counts[remote_ip] += 1

        # Check for attack patterns
        attack_detected = False
        attack_ips = []

        # Single IP threshold
        for ip, count in ip_counts.items():
            if count >= self.attack_threshold:
                attack_detected = True
                attack_ips.append(ip)

        # Total connections threshold
        if len(connections) >= self.total_connections_threshold:
            attack_detected = True

        return {
            'attack_detected': attack_detected,
            'attack_ips': attack_ips,
            'ip_counts': dict(ip_counts)
        }

    async def monitor_network(self):
        """Main network monitoring loop"""
        while True:
            current_time = time.time()

            # Get network connections
            connections = self.get_network_connections()

            # Detect attacks
            attack_info = self.detect_attack(connections)

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

            # Prepare data to send
            data = {
                'timestamp': datetime.now().isoformat(),
                'total_connections': len(connections),
                'unique_ips': len(set(c['remote_ip'] for c in connections if c['remote_ip'])),
                'latency': self.latency_data[-1] if self.latency_data else 0,
                'packet_loss': self.packet_loss_data[-1] if self.packet_loss_data else 0,
                'attack_detected': attack_info['attack_detected'],
                'attack_ips': attack_info['attack_ips'],
                'threat_level': 'critical' if attack_info['attack_detected'] else 'normal',
                'recent_connections': self.recent_connections,
                'local_ip': self.get_local_ip()
            }

            # Store for WebSocket broadcast
            self.current_data = data

            await asyncio.sleep(self.connection_check_interval)

    async def websocket_handler(self, websocket):
        """Handle WebSocket connections from Electron frontend"""
        print(f"Client connected: {websocket.remote_address}")

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
            print(f"Client disconnected: {websocket.remote_address}")
        except Exception as e:
            print(f"WebSocket error: {e}")

    async def start_server(self):
        """Start the WebSocket server"""
        # Start network monitoring in background
        asyncio.create_task(self.monitor_network())

        # Start WebSocket server
        print("🛡️  DDoS Gotchi Backend v3.0")
        print("=" * 50)
        print("WebSocket server starting on ws://localhost:8765")
        print("Waiting for Electron frontend to connect...")
        print("=" * 50)

        async with websockets.serve(self.websocket_handler, "localhost", 8765):
            await asyncio.Future()  # run forever

if __name__ == "__main__":
    backend = DDoSGotchiBackend()
    asyncio.run(backend.start_server())
