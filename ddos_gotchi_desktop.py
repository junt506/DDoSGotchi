#!/usr/bin/env python3
"""
DDoS Gotchi - Desktop Edition
Retro terminal-style DDoS detection with ASCII art Pwnagotchi
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
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


# ASCII Art for Pwnagotchi
PWNAGOTCHI_NORMAL = r"""
    ▄▀▄     ▄▀▄
   ▄█░░▀▀▀▀▀░░█▄
 ▄▀░░░░░░░░░░░▀▄
 █░░█░░░░░░█░░░█
 █░░░▀█▀░▀█▀░░░█
 █░░░░░░░░░░░░░█
  ▀▄░░ ═══ ░░▄▀
    ▀▀▀▀▀▀▀▀▀
  [ ALL  GOOD ]
"""

PWNAGOTCHI_ATTACK = r"""
    ▄▀▄     ▄▀▄
   ▄█░░▀▀▀▀▀░░█▄
 ▄▀░░░░░░░░░░░▀▄
 █░░X░░░░░░X░░░█
 █░░░▄█▄░▄█▄░░░█
 █░░░░░░░░░░░░░█
  ▀▄░░░▀▀▀░░░▄▀
    ▀▀▀▀▀▀▀▀▀
  [ UNDER ATTACK! ]
"""


class RetroTheme:
    """Retro terminal color scheme"""
    BG = '#000000'
    TEXT = '#00FF00'
    TEXT_DIM = '#008800'
    HIGHLIGHT = '#00FFFF'
    DANGER = '#FF0000'
    WARNING = '#FFFF00'
    BORDER = '#00FF00'


class DDoSGotchiApp:
    """Main desktop application"""

    def __init__(self, root):
        self.root = root
        self.root.title("▂▃▅▇ DDoS GOTCHI ▇▅▃▂")
        self.root.geometry("1000x800")
        self.root.configure(bg=RetroTheme.BG)

        # Initialize monitoring
        print("🚀 Initializing DDoS Gotchi Desktop...")
        self.network_monitor = NetworkMonitor()
        self.attack_detector = AttackDetector()

        # Data storage
        self.latency_data = deque(maxlen=100)
        self.packet_loss_data = deque(maxlen=100)
        self.time_data = deque(maxlen=100)

        # Connection log
        self.connection_log = deque(maxlen=100)

        # State
        self.running = True

        # Build UI
        self._setup_ui()

        # Start monitoring thread
        self.monitor_thread = Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

        # Start UI update loop
        self._update_ui()

    def _setup_ui(self):
        """Setup the retro terminal UI"""
        # Set retro font
        retro_font = ('Courier New', 10, 'bold')
        title_font = ('Courier New', 14, 'bold')
        ascii_font = ('Courier New', 8)

        # Main container
        main_frame = tk.Frame(self.root, bg=RetroTheme.BG, highlightbackground=RetroTheme.BORDER,
                             highlightthickness=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Header
        header = tk.Label(
            main_frame,
            text="║▌│█║▌│ DDoS GOTCHI v3.0 │▌║█│▌║",
            font=title_font,
            fg=RetroTheme.HIGHLIGHT,
            bg=RetroTheme.BG
        )
        header.pack(pady=(10, 5))

        # Top section: ASCII Art + Status
        top_section = tk.Frame(main_frame, bg=RetroTheme.BG)
        top_section.pack(fill=tk.BOTH, padx=10, pady=5)

        # Left: ASCII Pwnagotchi
        ascii_frame = tk.Frame(top_section, bg=RetroTheme.BG, highlightbackground=RetroTheme.BORDER,
                               highlightthickness=1)
        ascii_frame.pack(side=tk.LEFT, padx=(0, 10))

        self.ascii_label = tk.Label(
            ascii_frame,
            text=PWNAGOTCHI_NORMAL,
            font=ascii_font,
            fg=RetroTheme.TEXT,
            bg=RetroTheme.BG,
            justify=tk.LEFT
        )
        self.ascii_label.pack(padx=10, pady=10)

        # Right: Network Stats
        stats_frame = tk.Frame(top_section, bg=RetroTheme.BG, highlightbackground=RetroTheme.BORDER,
                               highlightthickness=1)
        stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            stats_frame,
            text=">>> NETWORK STATUS",
            font=title_font,
            fg=RetroTheme.HIGHLIGHT,
            bg=RetroTheme.BG
        ).pack(anchor=tk.W, padx=10, pady=(5, 2))

        self.stats_text = tk.Text(
            stats_frame,
            height=10,
            font=retro_font,
            fg=RetroTheme.TEXT,
            bg=RetroTheme.BG,
            insertbackground=RetroTheme.TEXT,
            relief=tk.FLAT
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.stats_text.config(state=tk.DISABLED)

        # Middle: Real-time Graphs
        if HAS_MATPLOTLIB:
            graph_frame = tk.Frame(main_frame, bg=RetroTheme.BG, highlightbackground=RetroTheme.BORDER,
                                   highlightthickness=1)
            graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

            tk.Label(
                graph_frame,
                text=">>> REAL-TIME METRICS",
                font=title_font,
                fg=RetroTheme.HIGHLIGHT,
                bg=RetroTheme.BG
            ).pack(anchor=tk.W, padx=10, pady=(5, 0))

            # Create matplotlib figure
            self.fig = Figure(figsize=(10, 3), facecolor=RetroTheme.BG)

            # Latency graph
            self.ax1 = self.fig.add_subplot(121)
            self.ax1.set_facecolor(RetroTheme.BG)
            self.ax1.set_title('LATENCY (ms)', color=RetroTheme.TEXT, fontfamily='monospace', fontsize=10)
            self.ax1.tick_params(colors=RetroTheme.TEXT_DIM, labelsize=8)
            self.ax1.spines['bottom'].set_color(RetroTheme.TEXT_DIM)
            self.ax1.spines['top'].set_color(RetroTheme.TEXT_DIM)
            self.ax1.spines['right'].set_color(RetroTheme.TEXT_DIM)
            self.ax1.spines['left'].set_color(RetroTheme.TEXT_DIM)
            self.ax1.grid(True, color=RetroTheme.TEXT_DIM, linestyle=':', linewidth=0.5, alpha=0.3)
            self.latency_line, = self.ax1.plot([], [], color=RetroTheme.TEXT, linewidth=2)
            self.ax1.set_ylim(0, 100)
            self.ax1.set_xlim(0, 100)

            # Packet loss graph
            self.ax2 = self.fig.add_subplot(122)
            self.ax2.set_facecolor(RetroTheme.BG)
            self.ax2.set_title('PACKET LOSS (%)', color=RetroTheme.TEXT, fontfamily='monospace', fontsize=10)
            self.ax2.tick_params(colors=RetroTheme.TEXT_DIM, labelsize=8)
            self.ax2.spines['bottom'].set_color(RetroTheme.TEXT_DIM)
            self.ax2.spines['top'].set_color(RetroTheme.TEXT_DIM)
            self.ax2.spines['right'].set_color(RetroTheme.TEXT_DIM)
            self.ax2.spines['left'].set_color(RetroTheme.TEXT_DIM)
            self.ax2.grid(True, color=RetroTheme.TEXT_DIM, linestyle=':', linewidth=0.5, alpha=0.3)
            self.packet_loss_line, = self.ax2.plot([], [], color=RetroTheme.DANGER, linewidth=2)
            self.ax2.set_ylim(0, 100)
            self.ax2.set_xlim(0, 100)

            self.fig.tight_layout()

            # Embed in tkinter
            self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Bottom: Live Connection Log
        log_frame = tk.Frame(main_frame, bg=RetroTheme.BG, highlightbackground=RetroTheme.BORDER,
                             highlightthickness=1)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(
            log_frame,
            text=">>> LIVE CONNECTION LOG",
            font=title_font,
            fg=RetroTheme.HIGHLIGHT,
            bg=RetroTheme.BG
        ).pack(anchor=tk.W, padx=10, pady=(5, 0))

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            font=retro_font,
            fg=RetroTheme.TEXT,
            bg=RetroTheme.BG,
            insertbackground=RetroTheme.TEXT,
            relief=tk.FLAT
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Footer
        footer = tk.Label(
            main_frame,
            text="[CTRL+C to EXIT] │ Network Monitor Active",
            font=retro_font,
            fg=RetroTheme.TEXT_DIM,
            bg=RetroTheme.BG
        )
        footer.pack(pady=5)

    def _log(self, message, color=None):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_line)
        if color:
            # Color the last line
            line_start = self.log_text.index("end-2c linestart")
            line_end = self.log_text.index("end-1c")
            tag_name = f"color_{color}"
            self.log_text.tag_add(tag_name, line_start, line_end)
            self.log_text.tag_config(tag_name, foreground=color)
        self.log_text.see(tk.END)  # Auto-scroll

    def _monitor_loop(self):
        """Background monitoring thread"""
        self._log("System initialized", RetroTheme.HIGHLIGHT)
        self._log(f"Monitoring gateway: Detecting...", RetroTheme.TEXT)

        last_state = None
        connection_check_counter = 0

        while self.running:
            try:
                # Get network stats
                stats = self.network_monitor.get_current_stats()
                attack_info = self.attack_detector.detect(stats)

                # Store for UI
                self.latest_stats = stats
                self.latest_attack = attack_info

                # Log state changes
                current_state = "attack" if attack_info.get('attack_detected') else "normal"
                if current_state != last_state:
                    if current_state == "attack":
                        self._log(f"⚠️  ATTACK DETECTED: {attack_info.get('attack_type', 'Unknown')}",
                                 RetroTheme.DANGER)
                    else:
                        self._log("✓ Network normal", RetroTheme.TEXT)
                    last_state = current_state

                # Update graph data
                if stats.get('connected'):
                    latency = stats.get('latency', -1)
                    self.latency_data.append(max(0, latency) if latency > 0 else 0)
                    self.packet_loss_data.append(stats.get('packet_loss', 0))

                # Log network activity every 10 seconds
                connection_check_counter += 1
                if connection_check_counter % 10 == 0:
                    gateway = stats.get('gateway', 'N/A')
                    latency = stats.get('latency', -1)
                    if latency > 0:
                        self._log(f"→ {gateway} | Latency: {latency:.1f}ms", RetroTheme.TEXT_DIM)

                time.sleep(1)

            except Exception as e:
                self._log(f"✗ Monitor error: {e}", RetroTheme.DANGER)
                time.sleep(1)

    def _update_ui(self):
        """Update UI elements"""
        if not self.running:
            return

        try:
            if hasattr(self, 'latest_stats') and hasattr(self, 'latest_attack'):
                stats = self.latest_stats
                attack = self.latest_attack

                is_attack = attack.get('attack_detected', False)

                # Update ASCII art
                if is_attack:
                    self.ascii_label.config(text=PWNAGOTCHI_ATTACK, fg=RetroTheme.DANGER)
                else:
                    self.ascii_label.config(text=PWNAGOTCHI_NORMAL, fg=RetroTheme.TEXT)

                # Update stats
                self.stats_text.config(state=tk.NORMAL)
                self.stats_text.delete('1.0', tk.END)

                status = "🚨 UNDER ATTACK" if is_attack else "✓ NORMAL"
                status_color = RetroTheme.DANGER if is_attack else RetroTheme.TEXT

                stats_display = f"""
STATUS:        {status}
GATEWAY:       {stats.get('gateway', 'N/A')}
NETWORK:       {stats.get('network', 'N/A')}
IP ADDRESS:    {stats.get('ip_address', 'N/A')}
LATENCY:       {stats.get('latency', -1):.1f} ms
PACKET LOSS:   {stats.get('packet_loss', 0):.1f} %
"""
                if is_attack:
                    stats_display += f"""
ATTACK TYPE:   {attack.get('attack_type', 'Unknown')}
CONFIDENCE:    {attack.get('confidence', 0):.0f}%
"""

                self.stats_text.insert('1.0', stats_display)
                self.stats_text.config(state=tk.DISABLED)

                # Update graphs
                if HAS_MATPLOTLIB and len(self.latency_data) > 0:
                    x = list(range(len(self.latency_data)))

                    self.latency_line.set_data(x, list(self.latency_data))
                    self.ax1.set_xlim(0, 100)
                    max_lat = max(self.latency_data) if self.latency_data else 100
                    self.ax1.set_ylim(0, max(100, max_lat * 1.2))

                    self.packet_loss_line.set_data(x, list(self.packet_loss_data))
                    self.ax2.set_xlim(0, 100)

                    self.canvas.draw_idle()

        except Exception as e:
            print(f"UI update error: {e}")

        # Schedule next update
        self.root.after(1000, self._update_ui)

    def cleanup(self):
        """Cleanup on exit"""
        self.running = False
        self._log("Shutting down...", RetroTheme.WARNING)
        if hasattr(self.network_monitor, 'stop_monitoring'):
            self.network_monitor.stop_monitoring()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = DDoSGotchiApp(root)

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
