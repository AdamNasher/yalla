#!/usr/bin/env python3
"""
Yalla - Interactive Security Dashboard (package)
"""

import sys
import time
import argparse

from .config import REFRESH_INTERVAL
from ._version import __version__
from .modules.system_monitor import get_system_stats
from .modules.network_monitor import get_network_stats
from .modules.ui_renderer import render_dashboard, clear_screen
from .modules.info_display import (
    display_cpu_info, display_memory_info, display_disk_info,
    display_private_ip, display_public_ip, display_network_info,
    display_system_stats, display_uptime
)

# Platform-specific imports
try:
    import select
    import termios
    import tty
    HAS_UNIX_TERMINAL = True
except ImportError:
    HAS_UNIX_TERMINAL = False
    try:
        import msvcrt
    except ImportError:
        msvcrt = None


class Dashboard:
    """Main dashboard controller"""
    
    def __init__(self):
        self.running = True
        self.old_settings = None
        
    def setup_terminal(self):
        """Configure terminal for non-blocking input"""
        if HAS_UNIX_TERMINAL:
            try:
                self.old_settings = termios.tcgetattr(sys.stdin)
                tty.setcbreak(sys.stdin.fileno())
            except:
                pass
    
    def restore_terminal(self):
        """Restore terminal settings"""
        if HAS_UNIX_TERMINAL and self.old_settings:
            try:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
            except:
                pass
    
    def check_input(self):
        """Check for keyboard input (non-blocking)"""
        if HAS_UNIX_TERMINAL:
            try:
                if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                    char = sys.stdin.read(1)
                    if char == 'q' or char == 'Q':
                        return 'quit'
                    elif char == 'r' or char == 'R':
                        return 'refresh'
            except:
                pass
        elif msvcrt:
            # Windows
            try:
                if msvcrt.kbhit():
                    char = msvcrt.getch().decode('utf-8').lower()
                    if char == 'q':
                        return 'quit'
                    elif char == 'r':
                        return 'refresh'
            except:
                pass
        return None
    
    def run(self):
        """Main dashboard loop"""
        self.setup_terminal()
        
        try:
            # Initialize colorama for Windows
            try:
                import colorama
                colorama.init()
            except ImportError:
                pass
            
            while self.running:
                # Check for user input
                action = self.check_input()
                if action == 'quit':
                    break
                
                # Collect data
                system_data = get_system_stats()
                network_data = get_network_stats()
                
                # Render dashboard
                render_dashboard(system_data, network_data)
                
                # Wait for next refresh
                time.sleep(REFRESH_INTERVAL)
        
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            pass
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up terminal and exit"""
        self.restore_terminal()
        clear_screen()
        print("Yalla dashboard closed. Stay secure! 🔒\n")


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Yalla - Interactive Security Dashboard',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  yalla              # Run full interactive dashboard
  yalla -c           # Show CPU info only
  yalla -i           # Show private IP address
  yalla -p           # Show public IP address
  yalla -c -m        # Show CPU and memory info
  yalla -s           # Show system stats summary
        """
    )
    
    # Short flags
    parser.add_argument('-c', '--cpu', action='store_true',
                        help='Display CPU information only')
    parser.add_argument('-m', '--memory', action='store_true',
                        help='Display memory information only')
    parser.add_argument('-d', '--disk', action='store_true',
                        help='Display disk information only')
    parser.add_argument('-i', '--ip', action='store_true',
                        help='Display private IP address(es)')
    parser.add_argument('-p', '--public-ip', action='store_true',
                        help='Display public IP address')
    parser.add_argument('-n', '--network', action='store_true',
                        help='Display network interfaces and connections')
    parser.add_argument('-s', '--stats', action='store_true',
                        help='Display system statistics summary')
    parser.add_argument('-u', '--uptime', action='store_true',
                        help='Display system uptime')

    parser.add_argument('--version', action='version',
                        version=f'%(prog)s {__version__}')
    
    return parser.parse_args()


def main():
    """Entry point"""
    args = parse_arguments()
    
    # Initialize colorama for Windows
    try:
        import colorama
        colorama.init()
    except ImportError:
        pass
    
    # Check if any specific info flags are set
    flags_set = [
        args.cpu, args.memory, args.disk, args.ip,
        args.public_ip, args.network, args.stats, args.uptime
    ]
    
    if any(flags_set):
        # Display specific information based on flags
        if args.cpu:
            display_cpu_info()
            print()  # Add spacing between multiple outputs
        
        if args.memory:
            display_memory_info()
            print()
        
        if args.disk:
            display_disk_info()
            print()
        
        if args.ip:
            display_private_ip()
            print()
        
        if args.public_ip:
            display_public_ip()
            print()
        
        if args.network:
            display_network_info()
            print()
        
        if args.stats:
            display_system_stats()
            print()
        
        if args.uptime:
            display_uptime()
            print()
    else:
        # No flags set, run full interactive dashboard
        dashboard = Dashboard()
        dashboard.run()


if __name__ == "__main__":
    main()
