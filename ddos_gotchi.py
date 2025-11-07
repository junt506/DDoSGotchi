#!/usr/bin/env python3
"""
DDoS Gotchi - A cybersecurity virtual pet that detects DDoS attacks
Inspired by Pwnagotchi with Fancygotchi's cyber theme
Educational/Lab Use Only
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
from collections import deque
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re

# Constants
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
FPS = 30
MATRIX_GREEN = (0, 255, 65)  # Lime green #00FF41
DARK_GREEN = (0, 128, 32)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# ASCII Art Faces
FACES = {
    'happy': [
        "  (⌐■_■)  ",
        "          ",
        "  \\___/   "
    ],
    'alert': [
        "  (⌐■_◉)  ",
        "          ",
        "   ___    "
    ],
    'under_attack': [
        "  (✖╭╮✖)  ",
        "          ",
        "   ~~~    "
    ],
    'stressed': [
        "  (⊙﹏⊙)  ",
        "          ",
        "  /___\\   "
    ],
    'disconnected': [
        "  (×_×)   ",
        "          ",
        "   ---    "
    ]
}

# Quotes for each state
QUOTES = {
    'happy': [
        "Living my best life in the 45.33 subnet",
        "I'm such a sigma right now",
        "Zero DDoS, infinite vibes",
        "Just a gotchi in the cyber-verse",
        "They see me pinging, they ain't flooding",
        "Connection so stable I could retire",
        "No attack? No problem! *sunglasses emoji energy*",
        "Chilling in the lab, dodging DDoS like Neo",
        "This network is my safe space",
        "Ping: low. Vibes: high.",
        "Monitoring the net, feeling blessed",
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
        "MIRAI IS AT IT AGAIN",
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


class MatrixRain:
    """Handles the Matrix-style digital rain effect background"""
    
    def __init__(self, width, height, font):
        self.width = width
        self.height = height
        self.font = font
        self.char_size = font.get_height()
        self.columns = width // (self.char_size - 5)
        self.drops = [random.randint(-height, 0) for _ in range(self.columns)]
        self.chars = []
        
        # Generate random characters for the rain
        self.matrix_chars = list("アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン")
        self.matrix_chars += list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        
        for _ in range(self.columns):
            column_chars = [random.choice(self.matrix_chars) for _ in range(height // self.char_size + 1)]
            self.chars.append(column_chars)
    
    def update(self):
        """Update the rain animation"""
        for i in range(self.columns):
            # Move drops down
            self.drops[i] += 1
            
            # Reset drop if it goes off screen
            if self.drops[i] * self.char_size > self.height and random.random() > 0.95:
                self.drops[i] = 0
                # Randomize characters when resetting
                self.chars[i] = [random.choice(self.matrix_chars) for _ in range(len(self.chars[i]))]
            
            # Occasionally change a character
            if random.random() > 0.98:
                char_index = random.randint(0, len(self.chars[i]) - 1)
                self.chars[i][char_index] = random.choice(self.matrix_chars)
    
    def draw(self, surface):
        """Draw the rain effect"""
        for i in range(self.columns):
            for j in range(len(self.chars[i])):
                y = (self.drops[i] + j) * self.char_size
                if 0 <= y <= self.height:
                    # Calculate fade based on position
                    fade = max(0, 1 - (j / 20))
                    color = (0, int(255 * fade), int(65 * fade))
                    
                    # Draw character
                    char_surface = self.font.render(self.chars[i][j], True, color)
                    x = i * (self.char_size - 5)
                    surface.blit(char_surface, (x, y))


class NetworkMonitor:
    """Monitors network statistics and detects anomalies"""
    
    def __init__(self, target_network="45.33.0", gateway="45.33.0.1"):
        self.target_network = target_network
        self.gateway = gateway
        self.latency_history = deque(maxlen=10)
        self.packet_loss_history = deque(maxlen=10)
        self.connected = False
        self.current_ssid = None
        self.interface = self._get_wifi_interface()
        
    def _get_wifi_interface(self):
        """Find the wireless interface"""
        interfaces = netifaces.interfaces()
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
        """Check if connected to WiFi and get SSID"""
        try:
            # Try to get SSID using iwgetid (Linux)
            if platform.system() == "Linux":
                try:
                    result = subprocess.run(['iwgetid', '-r'], 
                                         capture_output=True, 
                                         text=True, 
                                         timeout=2)
                    if result.returncode == 0:
                        self.current_ssid = result.stdout.strip()
                        self.connected = bool(self.current_ssid)
                        return self.connected
                except:
                    pass
            
            # Fallback: Check if we have an IP in the target network
            if self.interface:
                addrs = netifaces.ifaddresses(self.interface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        ip = addr['addr']
                        if ip.startswith(self.target_network):
                            self.connected = True
                            self.current_ssid = "Network: " + self.target_network
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
    
    def get_latency(self) -> float:
        """Measure latency to gateway using ping"""
        if not self.connected:
            return -1
        
        try:
            # Use ping command (cross-platform)
            if platform.system() == "Windows":
                cmd = ['ping', '-n', '1', '-w', '1000', self.gateway]
            else:
                cmd = ['ping', '-c', '1', '-W', '1', self.gateway]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
            
            if result.returncode == 0:
                # Parse ping output for latency
                output = result.stdout
                
                # Linux/Mac pattern
                match = re.search(r'time=(\d+\.?\d*)\s*ms', output)
                if match:
                    latency = float(match.group(1))
                    self.latency_history.append(latency)
                    return latency
                
                # Windows pattern
                match = re.search(r'Average = (\d+)ms', output)
                if match:
                    latency = float(match.group(1))
                    self.latency_history.append(latency)
                    return latency
        except Exception as e:
            print(f"Latency check error: {e}")
        
        return -1
    
    def get_packet_loss(self) -> float:
        """Measure packet loss percentage"""
        if not self.connected:
            return 100.0
        
        try:
            # Send 5 packets to get better loss measurement
            if platform.system() == "Windows":
                cmd = ['ping', '-n', '5', '-w', '1000', self.gateway]
            else:
                cmd = ['ping', '-c', '5', '-W', '1', '-i', '0.2', self.gateway]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
            output = result.stdout
            
            # Parse packet loss
            # Linux/Mac: "5 packets transmitted, 5 received, 0% packet loss"
            match = re.search(r'(\d+)%\s*(packet\s*)?loss', output)
            if match:
                loss = float(match.group(1))
                self.packet_loss_history.append(loss)
                return loss
            
            # Windows: "Lost = 0 (0% loss)"
            match = re.search(r'\((\d+)% loss\)', output)
            if match:
                loss = float(match.group(1))
                self.packet_loss_history.append(loss)
                return loss
                
        except Exception as e:
            print(f"Packet loss check error: {e}")
        
        return 0.0 if self.connected else 100.0
    
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
            'gateway': self.gateway
        }
        
        if self.connected:
            latency = self.get_latency()
            packet_loss = self.get_packet_loss()
            
            stats['latency'] = latency
            stats['packet_loss'] = packet_loss
            
            # Calculate averages for smoothing
            if self.latency_history:
                stats['avg_latency'] = sum(self.latency_history) / len(self.latency_history)
            else:
                stats['avg_latency'] = latency
                
            if self.packet_loss_history:
                stats['avg_packet_loss'] = sum(self.packet_loss_history) / len(self.packet_loss_history)
            else:
                stats['avg_packet_loss'] = packet_loss
        
        return stats


class StateManager:
    """Manages gotchi states based on network conditions"""
    
    def __init__(self):
        self.states = ['happy', 'alert', 'under_attack', 'stressed', 'disconnected']
        self.current_state = 'disconnected'
        self.state_history = deque(maxlen=5)
        self.last_quote_change = time.time()
        self.current_quote = ""
        self.quote_interval = 15  # seconds between quote changes
        
    def determine_state(self, stats: Dict) -> str:
        """Determine state based on network statistics"""
        if not stats['connected']:
            new_state = 'disconnected'
        else:
            # Use averaged values for stability
            latency = stats.get('avg_latency', -1)
            packet_loss = stats.get('avg_packet_loss', 0)
            
            if latency < 0:
                new_state = 'disconnected'
            elif latency < 10 and packet_loss < 1:
                new_state = 'happy'
            elif latency < 50 and packet_loss < 5:
                new_state = 'alert'
            elif latency < 200 and packet_loss < 20:
                new_state = 'under_attack'
            else:
                new_state = 'stressed'
        
        # Add to history for smoothing
        self.state_history.append(new_state)
        
        # Use most common state in recent history (prevents flicker)
        from collections import Counter
        state_counts = Counter(self.state_history)
        smoothed_state = state_counts.most_common(1)[0][0]
        
        # Update current state
        if smoothed_state != self.current_state:
            self.current_state = smoothed_state
            self.current_quote = self.get_random_quote(smoothed_state)
            self.last_quote_change = time.time()
        elif time.time() - self.last_quote_change > self.quote_interval:
            # Change quote periodically
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
    """Handles the cyber-themed UI rendering"""
    
    def __init__(self, screen, font, big_font, small_font):
        self.screen = screen
        self.font = font
        self.big_font = big_font
        self.small_font = small_font
        self.matrix_rain = MatrixRain(WINDOW_WIDTH, WINDOW_HEIGHT, small_font)
        self.frame_count = 0
        self.blink_timer = 0
        
    def render_background(self):
        """Render the Matrix rain background"""
        self.screen.fill(BLACK)
        self.matrix_rain.update()
        self.matrix_rain.draw(self.screen)
        
        # Add subtle scanlines for extra cyber effect
        if self.frame_count % 2 == 0:
            for y in range(0, WINDOW_HEIGHT, 4):
                pygame.draw.line(self.screen, (0, 20, 5), (0, y), (WINDOW_WIDTH, y), 1)
    
    def render_gotchi(self, face: List[str], state: str):
        """Render the gotchi face and container"""
        # Draw container box
        box_width = 300
        box_height = 150
        box_x = (WINDOW_WIDTH - box_width) // 2
        box_y = 100
        
        # Create semi-transparent background
        box_surface = pygame.Surface((box_width, box_height))
        box_surface.set_alpha(200)
        box_surface.fill(BLACK)
        self.screen.blit(box_surface, (box_x, box_y))
        
        # Draw border
        border_color = MATRIX_GREEN if state != 'disconnected' else RED
        pygame.draw.rect(self.screen, border_color, 
                        (box_x - 2, box_y - 2, box_width + 4, box_height + 4), 2)
        
        # Draw double border for cyber effect
        pygame.draw.rect(self.screen, DARK_GREEN, 
                        (box_x - 4, box_y - 4, box_width + 8, box_height + 8), 1)
        
        # Render face (with blink animation for happy state)
        face_to_render = face.copy()
        if state == 'happy' and self.blink_timer > 28:
            face_to_render[0] = "  (⌐-_-)  "  # Blinking
        
        y_offset = box_y + 30
        for line in face_to_render:
            text_surface = self.big_font.render(line, True, border_color)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 30
        
        # Render "DDOS GOTCHI" title
        title = "[ DDOS GOTCHI ]"
        title_surface = self.font.render(title, True, MATRIX_GREEN)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, box_y + box_height - 20))
        self.screen.blit(title_surface, title_rect)
        
        # Add glitch effect for attack states
        if state in ['under_attack', 'stressed'] and random.random() > 0.9:
            glitch_surface = pygame.Surface((box_width, box_height))
            glitch_surface.set_alpha(50)
            glitch_surface.fill((random.randint(0, 255), 0, 0))
            self.screen.blit(glitch_surface, (box_x + random.randint(-5, 5), box_y + random.randint(-5, 5)))
    
    def render_stats(self, stats: Dict, state: str):
        """Render network statistics"""
        y_offset = 280
        
        # Connection status
        connected_color = MATRIX_GREEN if stats['connected'] else RED
        status_symbol = "●" if stats['connected'] else "○"
        status_text = f"STATUS: {status_symbol} {'CONNECTED' if stats['connected'] else 'DISCONNECTED'}"
        self._render_text(status_text, connected_color, WINDOW_WIDTH // 2, y_offset)
        y_offset += 30
        
        # Network info
        if stats['connected']:
            network_text = f"NETWORK: {stats.get('ssid', 'Unknown')}"
            self._render_text(network_text, MATRIX_GREEN, WINDOW_WIDTH // 2, y_offset)
            y_offset += 30
            
            # Latency
            latency = stats.get('latency', -1)
            if latency >= 0:
                latency_color = self._get_stat_color(latency, 10, 50, 200)
                latency_text = f"LATENCY: {latency:.1f}ms"
                if latency > 999:
                    latency_text = "LATENCY: TIMEOUT"
                self._render_text(latency_text, latency_color, WINDOW_WIDTH // 2, y_offset)
                y_offset += 30
            
            # Packet loss
            packet_loss = stats.get('packet_loss', 0)
            loss_color = self._get_stat_color(packet_loss, 1, 5, 20)
            packet_text = f"PACKETS: {100 - packet_loss:.1f}% OK"
            self._render_text(packet_text, loss_color, WINDOW_WIDTH // 2, y_offset)
            y_offset += 30
        
        # Threat level indicator
        if state != 'disconnected':
            self._render_threat_level(state, WINDOW_WIDTH // 2, y_offset + 20)
    
    def _render_threat_level(self, state: str, x: int, y: int):
        """Render a visual threat level indicator"""
        threat_levels = {
            'happy': (0, "SECURE"),
            'alert': (1, "CAUTION"),
            'under_attack': (2, "DANGER"),
            'stressed': (3, "CRITICAL")
        }
        
        level, label = threat_levels.get(state, (0, "UNKNOWN"))
        
        # Draw threat level bars
        bar_width = 40
        bar_height = 10
        total_width = bar_width * 4 + 30
        start_x = x - total_width // 2
        
        for i in range(4):
            color = MATRIX_GREEN if i <= level else DARK_GREEN
            if level >= 2 and i <= level:
                color = RED if level == 3 else (255, 165, 0)  # Orange for danger
            
            pygame.draw.rect(self.screen, color, 
                           (start_x + i * (bar_width + 10), y, bar_width, bar_height))
        
        # Draw label
        label_text = f"THREAT: {label}"
        label_color = MATRIX_GREEN if level == 0 else (RED if level >= 2 else (255, 165, 0))
        self._render_text(label_text, label_color, x, y + 20)
    
    def render_quote(self, quote: str):
        """Render the current quote"""
        # Create quote box
        max_width = WINDOW_WIDTH - 100
        words = quote.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = self.font.render(test_line, True, MATRIX_GREEN)
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
        
        # Render quote lines
        y_offset = WINDOW_HEIGHT - 100
        for line in lines:
            self._render_text(f'"{line}"', MATRIX_GREEN, WINDOW_WIDTH // 2, y_offset)
            y_offset += 25
    
    def _render_text(self, text: str, color: Tuple[int, int, int], x: int, y: int):
        """Helper to render centered text"""
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def _get_stat_color(self, value: float, good: float, warn: float, bad: float) -> Tuple[int, int, int]:
        """Get color based on stat thresholds"""
        if value <= good:
            return MATRIX_GREEN
        elif value <= warn:
            return (255, 255, 0)  # Yellow
        elif value <= bad:
            return (255, 165, 0)  # Orange
        else:
            return RED
    
    def update(self):
        """Update UI animations"""
        self.frame_count += 1
        self.blink_timer = (self.blink_timer + 1) % 30  # Blink cycle


class DDoSGotchi:
    """Main application class"""
    
    def __init__(self):
        pygame.init()
        
        # Set up display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("DDoS Gotchi - Cyber Security Pet")
        
        # Load fonts
        try:
            self.small_font = pygame.font.Font(pygame.font.match_font('couriernew', 'courier', 'monospace'), 12)
            self.font = pygame.font.Font(pygame.font.match_font('couriernew', 'courier', 'monospace'), 16)
            self.big_font = pygame.font.Font(pygame.font.match_font('couriernew', 'courier', 'monospace'), 24)
        except:
            self.small_font = pygame.font.Font(None, 12)
            self.font = pygame.font.Font(None, 16)
            self.big_font = pygame.font.Font(None, 24)
        
        # Initialize components
        self.network_monitor = NetworkMonitor()
        self.state_manager = StateManager()
        self.ui = CyberUI(self.screen, self.font, self.big_font, self.small_font)
        
        # Threading for network monitoring
        self.running = True
        self.stats = {}
        self.monitor_thread = threading.Thread(target=self.monitor_network, daemon=True)
        self.monitor_thread.start()
        
        # Statistics tracking
        self.start_time = time.time()
        self.total_attacks = 0
        self.last_state = 'disconnected'
        
        self.clock = pygame.time.Clock()
    
    def monitor_network(self):
        """Background thread for network monitoring"""
        while self.running:
            try:
                # Check connection first
                self.network_monitor.check_wifi_connection()
                
                # Get stats
                self.stats = self.network_monitor.get_network_stats()
                
                # Sleep before next check
                time.sleep(2)
            except Exception as e:
                print(f"Monitor thread error: {e}")
                time.sleep(5)
    
    def run(self):
        """Main game loop"""
        print("DDoS Gotchi starting...")
        print("Monitoring for DDoS attacks on the network...")
        
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        # Force quote change
                        self.state_manager.last_quote_change = 0
            
            # Update state
            if self.stats:
                state = self.state_manager.determine_state(self.stats)
                
                # Track attacks
                if state in ['under_attack', 'stressed'] and self.last_state not in ['under_attack', 'stressed']:
                    self.total_attacks += 1
                self.last_state = state
            else:
                state = 'disconnected'
            
            # Get current visuals
            face = self.state_manager.get_face_for_state(state)
            quote = self.state_manager.get_current_quote()
            
            # Render everything
            self.ui.render_background()
            self.ui.render_gotchi(face, state)
            self.ui.render_stats(self.stats, state)
            self.ui.render_quote(quote)
            
            # Update animations
            self.ui.update()
            
            # Show runtime and attack count
            runtime = int(time.time() - self.start_time)
            runtime_text = f"Runtime: {runtime//3600:02d}:{(runtime%3600)//60:02d}:{runtime%60:02d} | Attacks Detected: {self.total_attacks}"
            text_surface = self.font.render(runtime_text, True, DARK_GREEN)
            self.screen.blit(text_surface, (10, WINDOW_HEIGHT - 20))
            
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
