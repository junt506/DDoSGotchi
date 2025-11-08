"""
Network Watcher - Detects network changes and triggers reconfiguration
"""

import threading
import time
import subprocess
import hashlib
from typing import Optional


class NetworkWatcher:
    """Watches for network changes and triggers reconfiguration"""

    def __init__(self, network_monitor):
        self.network_monitor = network_monitor
        self.running = False
        self.thread = None
        self.last_network_hash = None
        self.check_interval = 5  # Check every 5 seconds

    def start(self):
        """Start watching for network changes"""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._watch_loop, daemon=True)
        self.thread.start()
        print("👁️  Network watcher started")

    def stop(self):
        """Stop watching"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("👁️  Network watcher stopped")

    def _watch_loop(self):
        """Main watching loop"""
        while self.running:
            try:
                current_hash = self._get_network_hash()

                if current_hash != self.last_network_hash:
                    if self.last_network_hash is not None:
                        print(f"🔄 Network change detected!")
                        self.network_monitor.reinitialize()

                    self.last_network_hash = current_hash

            except Exception as e:
                print(f"Network watcher error: {e}")

            time.sleep(self.check_interval)

    def _get_network_hash(self) -> str:
        """Get a hash representing current network state"""
        try:
            # Get routing table (only the default route)
            result = subprocess.run(
                ['ip', 'route', 'show', 'default'],
                capture_output=True,
                text=True,
                timeout=2
            )

            # Get active network interfaces (only UP interfaces)
            interfaces = subprocess.run(
                ['ip', '-o', 'link', 'show', 'up'],
                capture_output=True,
                text=True,
                timeout=2
            )

            # Only hash the relevant parts (routes and active interfaces, not stats)
            combined = result.stdout + interfaces.stdout
            return hashlib.md5(combined.encode()).hexdigest()

        except Exception as e:
            print(f"Network hash error: {e}")
            return ""
