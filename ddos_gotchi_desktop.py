#!/usr/bin/env python3
"""
DDoS Gotchi - Desktop Edition
Simple, modern desktop app for DDoS detection
"""

import tkinter as tk
from tkinter import ttk
import sys
import os
from threading import Thread
from collections import deque
from datetime import datetime
import time

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from core.network_monitor import NetworkMonitor
from core.attack_detector import AttackDetector

# Try to import matplotlib for graphs
try:
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️  matplotlib not available - running without graphs")


class CyberTheme:
    """Cyber aesthetic color scheme"""
    BG_DARK = '#0a0e27'
    BG_PANEL = '#151932'
    ACCENT_CYAN = '#00f0ff'
    ACCENT_PINK = '#ff2f92'
    TEXT_PRIMARY = '#e0e0e0'
    TEXT_SECONDARY = '#808080'
    DANGER = '#ff2f92'
    SAFE = '#00ff88'
    WARNING = '#ffaa00'


class DDoSGotchiApp:
    """Main desktop application"""

    def __init__(self, root):
        self.root = root
        self.root.title("DDoS Gotchi - Desktop Edition")
        self.root.geometry("900x700")
        self.root.configure(bg=CyberTheme.BG_DARK)

        # Initialize monitoring
        print("🚀 Initializing DDoS Gotchi Desktop...")
        self.network_monitor = NetworkMonitor()
        self.attack_detector = AttackDetector()

        # Data storage for graphs
        self.latency_data = deque(maxlen=60)
        self.packet_loss_data = deque(maxlen=60)
        self.time_data = deque(maxlen=60)

        # State
        self.is_under_attack = False
        self.running = True

        # Build UI
        self._setup_ui()

        # Start monitoring thread
        self.monitor_thread = Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

        # Start UI update loop
        self._update_ui()

    def _setup_ui(self):
        """Setup the user interface"""
        # Header
        header = tk.Frame(self.root, bg=CyberTheme.BG_DARK)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))

        title = tk.Label(
            header,
            text="DDoS GOTCHI",
            font=('Courier New', 28, 'bold'),
            fg=CyberTheme.ACCENT_CYAN,
            bg=CyberTheme.BG_DARK
        )
        title.pack(side=tk.LEFT)

        # Status indicator (large, prominent)
        self.status_frame = tk.Frame(self.root, bg=CyberTheme.BG_PANEL, relief=tk.RAISED, borderwidth=2)
        self.status_frame.pack(fill=tk.X, padx=20, pady=10)

        self.status_label = tk.Label(
            self.status_frame,
            text="● NORMAL",
            font=('Courier New', 32, 'bold'),
            fg=CyberTheme.SAFE,
            bg=CyberTheme.BG_PANEL,
            pady=20
        )
        self.status_label.pack()

        # Stats panel
        stats_container = tk.Frame(self.root, bg=CyberTheme.BG_DARK)
        stats_container.pack(fill=tk.BOTH, padx=20, pady=10)

        # Left: Network stats
        stats_left = tk.Frame(stats_container, bg=CyberTheme.BG_PANEL, relief=tk.SUNKEN, borderwidth=1)
        stats_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        tk.Label(
            stats_left,
            text="NETWORK STATUS",
            font=('Courier New', 12, 'bold'),
            fg=CyberTheme.ACCENT_CYAN,
            bg=CyberTheme.BG_PANEL
        ).pack(pady=(10, 5))

        self.stats_labels = {}
        for stat in ['Gateway', 'Network', 'Latency', 'Packet Loss']:
            frame = tk.Frame(stats_left, bg=CyberTheme.BG_PANEL)
            frame.pack(fill=tk.X, padx=10, pady=2)

            tk.Label(
                frame,
                text=f"{stat}:",
                font=('Courier New', 10),
                fg=CyberTheme.TEXT_SECONDARY,
                bg=CyberTheme.BG_PANEL,
                width=12,
                anchor='w'
            ).pack(side=tk.LEFT)

            value_label = tk.Label(
                frame,
                text="---",
                font=('Courier New', 10, 'bold'),
                fg=CyberTheme.TEXT_PRIMARY,
                bg=CyberTheme.BG_PANEL,
                anchor='w'
            )
            value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.stats_labels[stat] = value_label

        # Right: Character display
        char_frame = tk.Frame(stats_container, bg=CyberTheme.BG_PANEL, relief=tk.SUNKEN, borderwidth=1)
        char_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        tk.Label(
            char_frame,
            text="SYSTEM MONITOR",
            font=('Courier New', 12, 'bold'),
            fg=CyberTheme.ACCENT_CYAN,
            bg=CyberTheme.BG_PANEL
        ).pack(pady=(10, 5))

        self.character_label = tk.Label(
            char_frame,
            text="😊",
            font=('Arial', 80),
            bg=CyberTheme.BG_PANEL,
            pady=20
        )
        self.character_label.pack()

        self.character_status = tk.Label(
            char_frame,
            text="Monitoring...",
            font=('Courier New', 10),
            fg=CyberTheme.TEXT_SECONDARY,
            bg=CyberTheme.BG_PANEL
        )
        self.character_status.pack()

        # Graphs section
        if HAS_MATPLOTLIB:
            graph_frame = tk.Frame(self.root, bg=CyberTheme.BG_DARK)
            graph_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            # Create matplotlib figure
            self.fig = Figure(figsize=(8, 3), facecolor=CyberTheme.BG_PANEL)

            # Latency graph
            self.ax1 = self.fig.add_subplot(121)
            self.ax1.set_facecolor(CyberTheme.BG_DARK)
            self.ax1.set_title('Latency (ms)', color=CyberTheme.TEXT_PRIMARY, fontfamily='monospace')
            self.ax1.tick_params(colors=CyberTheme.TEXT_SECONDARY)
            self.latency_line, = self.ax1.plot([], [], color=CyberTheme.ACCENT_CYAN, linewidth=2)
            self.ax1.set_ylim(0, 100)

            # Packet loss graph
            self.ax2 = self.fig.add_subplot(122)
            self.ax2.set_facecolor(CyberTheme.BG_DARK)
            self.ax2.set_title('Packet Loss (%)', color=CyberTheme.TEXT_PRIMARY, fontfamily='monospace')
            self.ax2.tick_params(colors=CyberTheme.TEXT_SECONDARY)
            self.packet_loss_line, = self.ax2.plot([], [], color=CyberTheme.ACCENT_PINK, linewidth=2)
            self.ax2.set_ylim(0, 100)

            self.fig.tight_layout()

            # Embed in tkinter
            self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Footer
        footer = tk.Label(
            self.root,
            text="Press Ctrl+C to exit • Real-time DDoS Detection",
            font=('Courier New', 8),
            fg=CyberTheme.TEXT_SECONDARY,
            bg=CyberTheme.BG_DARK
        )
        footer.pack(pady=(0, 10))

    def _monitor_loop(self):
        """Background monitoring thread"""
        while self.running:
            try:
                # Get network stats (from cache, non-blocking)
                stats = self.network_monitor.get_current_stats()

                # Detect attacks
                attack_info = self.attack_detector.detect(stats)

                # Store for UI update
                self.latest_stats = stats
                self.latest_attack = attack_info

                # Update graph data
                if stats.get('connected'):
                    self.time_data.append(datetime.now())
                    latency = stats.get('latency', -1)
                    self.latency_data.append(max(0, latency) if latency > 0 else 0)
                    self.packet_loss_data.append(stats.get('packet_loss', 0))

                time.sleep(1)

            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(1)

    def _update_ui(self):
        """Update UI elements (runs in main thread)"""
        if not self.running:
            return

        try:
            if hasattr(self, 'latest_stats') and hasattr(self, 'latest_attack'):
                stats = self.latest_stats
                attack = self.latest_attack

                # Update status
                is_attack = attack.get('attack_detected', False)

                if is_attack:
                    self.status_label.config(
                        text="🚨 UNDER ATTACK",
                        fg=CyberTheme.DANGER
                    )
                    self.status_frame.config(bg=CyberTheme.DANGER)
                    self.character_label.config(text="😱")
                    self.character_status.config(
                        text=f"Attack Type: {attack.get('attack_type', 'Unknown')}",
                        fg=CyberTheme.DANGER
                    )
                else:
                    self.status_label.config(
                        text="✅ NORMAL",
                        fg=CyberTheme.SAFE
                    )
                    self.status_frame.config(bg=CyberTheme.BG_PANEL)
                    self.character_label.config(text="😊")
                    self.character_status.config(
                        text="All systems operational",
                        fg=CyberTheme.TEXT_SECONDARY
                    )

                # Update stats
                self.stats_labels['Gateway'].config(
                    text=stats.get('gateway', 'N/A')
                )
                self.stats_labels['Network'].config(
                    text=stats.get('network', 'N/A')
                )

                latency = stats.get('latency', -1)
                if latency > 0:
                    lat_color = CyberTheme.SAFE if latency < 50 else CyberTheme.WARNING if latency < 100 else CyberTheme.DANGER
                    self.stats_labels['Latency'].config(
                        text=f"{latency:.1f} ms",
                        fg=lat_color
                    )
                else:
                    self.stats_labels['Latency'].config(text="---", fg=CyberTheme.TEXT_PRIMARY)

                packet_loss = stats.get('packet_loss', 0)
                pl_color = CyberTheme.SAFE if packet_loss < 1 else CyberTheme.WARNING if packet_loss < 5 else CyberTheme.DANGER
                self.stats_labels['Packet Loss'].config(
                    text=f"{packet_loss:.1f}%",
                    fg=pl_color
                )

                # Update graphs
                if HAS_MATPLOTLIB and len(self.latency_data) > 0:
                    x = list(range(len(self.latency_data)))

                    self.latency_line.set_data(x, list(self.latency_data))
                    self.ax1.set_xlim(0, 60)

                    self.packet_loss_line.set_data(x, list(self.packet_loss_data))
                    self.ax2.set_xlim(0, 60)

                    self.canvas.draw_idle()

        except Exception as e:
            print(f"UI update error: {e}")

        # Schedule next update
        self.root.after(1000, self._update_ui)

    def cleanup(self):
        """Cleanup on exit"""
        self.running = False
        print("\n🛑 Shutting down...")
        if hasattr(self.network_monitor, 'stop_monitoring'):
            self.network_monitor.stop_monitoring()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = DDoSGotchiApp(root)

    # Handle window close
    def on_closing():
        app.cleanup()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        on_closing()


if __name__ == '__main__':
    main()
