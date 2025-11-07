#!/usr/bin/env python3
"""
Network Condition Simulator for DDoS Gotchi Testing
This script simulates various network conditions for testing the DDoS Gotchi
without requiring actual DDoS attacks.
"""

import subprocess
import time
import sys
import random
import signal
import os

class NetworkSimulator:
    """Simulates network conditions using tc (traffic control) on Linux"""
    
    def __init__(self, interface="lo"):
        self.interface = interface
        self.original_state = None
        
        # Check if running on Linux
        if sys.platform not in ['linux', 'linux2']:
            print("Warning: Traffic control (tc) is only available on Linux.")
            print("This simulator will only work properly on Linux systems.")
            
        # Check if tc is available
        try:
            subprocess.run(['tc', '-Version'], capture_output=True, check=True)
        except:
            print("Error: 'tc' command not found. Install it with:")
            print("  Ubuntu/Debian: sudo apt install iproute2")
            print("  RHEL/CentOS: sudo yum install iproute")
            sys.exit(1)
            
        # Register cleanup handler
        signal.signal(signal.SIGINT, self.cleanup_handler)
        signal.signal(signal.SIGTERM, self.cleanup_handler)
    
    def cleanup_handler(self, signum, frame):
        """Handle cleanup on exit"""
        print("\nCleaning up network conditions...")
        self.reset_conditions()
        sys.exit(0)
    
    def reset_conditions(self):
        """Reset network to normal conditions"""
        print("Resetting network conditions...")
        try:
            # Delete any existing qdisc
            subprocess.run(
                ['sudo', 'tc', 'qdisc', 'del', 'dev', self.interface, 'root'],
                capture_output=True
            )
            print("Network conditions reset to normal")
        except:
            pass
    
    def apply_conditions(self, latency=0, jitter=0, loss=0):
        """Apply network conditions using tc"""
        # Reset first
        self.reset_conditions()
        
        if latency == 0 and loss == 0:
            return
        
        try:
            # Build tc command
            cmd = ['sudo', 'tc', 'qdisc', 'add', 'dev', self.interface, 'root', 'netem']
            
            if latency > 0:
                cmd.extend(['delay', f'{latency}ms'])
                if jitter > 0:
                    cmd.append(f'{jitter}ms')
            
            if loss > 0:
                cmd.extend(['loss', f'{loss}%'])
            
            # Apply conditions
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Applied: Latency={latency}ms, Jitter={jitter}ms, Loss={loss}%")
            else:
                print(f"Error applying conditions: {result.stderr}")
        except Exception as e:
            print(f"Error: {e}")
    
    def simulate_normal(self):
        """Simulate normal network conditions"""
        print("\n=== Simulating NORMAL conditions ===")
        self.apply_conditions(latency=5, jitter=1, loss=0)
    
    def simulate_alert(self):
        """Simulate slight degradation"""
        print("\n=== Simulating ALERT conditions ===")
        self.apply_conditions(latency=30, jitter=10, loss=2)
    
    def simulate_attack(self):
        """Simulate active DDoS attack"""
        print("\n=== Simulating ACTIVE ATTACK conditions ===")
        self.apply_conditions(latency=100, jitter=50, loss=10)
    
    def simulate_severe_attack(self):
        """Simulate severe DDoS attack"""
        print("\n=== Simulating SEVERE ATTACK conditions ===")
        self.apply_conditions(latency=300, jitter=100, loss=30)
    
    def simulate_progressive_attack(self, duration=60):
        """Simulate a progressive attack that gets worse over time"""
        print(f"\n=== Simulating PROGRESSIVE ATTACK over {duration} seconds ===")
        
        steps = 5
        step_duration = duration // steps
        
        for i in range(steps):
            progress = (i + 1) / steps
            latency = int(5 + (295 * progress))  # 5ms to 300ms
            jitter = int(1 + (99 * progress))     # 1ms to 100ms
            loss = int(0 + (30 * progress))       # 0% to 30%
            
            print(f"\nStage {i+1}/{steps}:")
            self.apply_conditions(latency, jitter, loss)
            time.sleep(step_duration)
    
    def simulate_fluctuating(self, duration=120):
        """Simulate fluctuating network conditions"""
        print(f"\n=== Simulating FLUCTUATING conditions for {duration} seconds ===")
        
        start_time = time.time()
        while time.time() - start_time < duration:
            # Random conditions
            latency = random.randint(5, 150)
            jitter = random.randint(0, 50)
            loss = random.randint(0, 15)
            
            self.apply_conditions(latency, jitter, loss)
            
            # Hold for random duration
            hold_time = random.randint(5, 15)
            print(f"Holding for {hold_time} seconds...")
            time.sleep(hold_time)


def run_scenario(simulator, scenario):
    """Run a specific test scenario"""
    scenarios = {
        '1': ('Normal Network', simulator.simulate_normal, 30),
        '2': ('Alert Condition', simulator.simulate_alert, 30),
        '3': ('Active Attack', simulator.simulate_attack, 30),
        '4': ('Severe Attack', simulator.simulate_severe_attack, 30),
        '5': ('Progressive Attack', lambda: simulator.simulate_progressive_attack(60), 60),
        '6': ('Fluctuating Conditions', lambda: simulator.simulate_fluctuating(120), 120),
        '7': ('Complete Cycle', None, 0),  # Special case
    }
    
    if scenario == '7':
        # Run complete cycle
        print("\n=== Running COMPLETE CYCLE ===")
        print("This will simulate all conditions in sequence")
        
        # Normal -> Alert -> Attack -> Severe -> Recovery
        simulator.simulate_normal()
        time.sleep(20)
        
        simulator.simulate_alert()
        time.sleep(20)
        
        simulator.simulate_attack()
        time.sleep(20)
        
        simulator.simulate_severe_attack()
        time.sleep(20)
        
        print("\n=== Simulating RECOVERY ===")
        simulator.simulate_attack()
        time.sleep(10)
        
        simulator.simulate_alert()
        time.sleep(10)
        
        simulator.simulate_normal()
        time.sleep(20)
    else:
        name, func, duration = scenarios[scenario]
        func()
        if duration > 0:
            print(f"\nHolding conditions for {duration} seconds...")
            print("Press Ctrl+C to stop")
            time.sleep(duration)


def main():
    print("""
╔══════════════════════════════════════════════╗
║     DDoS Gotchi Network Condition Simulator   ║
╚══════════════════════════════════════════════╝

This tool simulates various network conditions to test DDoS Gotchi
without requiring actual DDoS attacks.

⚠️  REQUIREMENTS:
- Linux OS (uses 'tc' traffic control)
- Run with sudo for network control
- DDoS Gotchi should be running

Select a scenario to simulate:
1. Normal Network (Happy state)
2. Alert Condition (Slight degradation)
3. Active Attack (DDoS simulation)
4. Severe Attack (Critical condition)
5. Progressive Attack (Gradual degradation)
6. Fluctuating Conditions (Random changes)
7. Complete Cycle (All states in sequence)
0. Reset and Exit
""")
    
    # Check if running with sudo
    if os.geteuid() != 0:
        print("❌ This script requires sudo privileges to control network conditions.")
        print("Please run: sudo python3 test_simulator.py")
        sys.exit(1)
    
    # Get network interface
    print("\nAvailable network interfaces:")
    try:
        result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True)
        interfaces = []
        for line in result.stdout.split('\n'):
            if ':' in line and not line.startswith(' '):
                parts = line.split(':')
                if len(parts) >= 2:
                    iface = parts[1].strip()
                    if iface and iface != 'lo':
                        interfaces.append(iface)
                        print(f"  - {iface}")
    except:
        interfaces = []
    
    if interfaces:
        print("\nEnter interface name (or press Enter for 'lo' loopback):")
        iface = input("> ").strip()
        if not iface:
            iface = 'lo'
    else:
        iface = 'lo'
    
    simulator = NetworkSimulator(iface)
    
    while True:
        print("\nSelect scenario (0-7):")
        choice = input("> ").strip()
        
        if choice == '0':
            simulator.reset_conditions()
            print("Exiting...")
            break
        elif choice in ['1', '2', '3', '4', '5', '6', '7']:
            try:
                run_scenario(simulator, choice)
            except KeyboardInterrupt:
                print("\n\nScenario interrupted")
            finally:
                simulator.reset_conditions()
        else:
            print("Invalid choice. Please select 0-7")
    
    # Final cleanup
    simulator.reset_conditions()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSimulator interrupted")
        NetworkSimulator().reset_conditions()
    except Exception as e:
        print(f"\nError: {e}")
        NetworkSimulator().reset_conditions()
