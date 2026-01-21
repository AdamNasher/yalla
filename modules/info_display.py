"""
Info Display Module
Functions to display specific information based on command-line flags
"""

from config import Colors
from modules.system_monitor import get_system_stats, get_memory_info
from modules.network_monitor import get_network_interfaces, get_public_ip
from modules.ui_renderer import format_bytes, format_uptime, create_progress_bar


def display_cpu_info():
    """Display CPU information only"""
    stats = get_system_stats()
    
    print(f"{Colors.DARK_VIOLET}{Colors.BOLD}CPU Information{Colors.RESET}")
    print(f"{Colors.DARK_GREY}{'─' * 50}{Colors.RESET}")
    
    cpu_percent = stats.get('cpu_percent', 0)
    cpu_cores = stats.get('cpu_count', 'N/A')
    
    print(f"CPU Usage: {Colors.RED}{cpu_percent:.1f}%{Colors.RESET} {Colors.DARK_GREY}<- Current processor utilization{Colors.RESET}")
    print(f"CPU Cores: {Colors.BLUE}{cpu_cores}{Colors.RESET} {Colors.DARK_GREY}<- Number of processing units available{Colors.RESET}")
    
    if stats.get('load_avg'):
        load = stats['load_avg']
        print(f"Load Average: {Colors.BLUE}{load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}{Colors.RESET} {Colors.DARK_GREY}<- System load (1min, 5min, 15min){Colors.RESET}")
    
    print(f"\n{create_progress_bar(cpu_percent, 100, '')}")


def display_memory_info():
    """Display memory information only"""
    stats = get_system_stats()
    memory_info = get_memory_info()
    
    print(f"{Colors.DARK_VIOLET}{Colors.BOLD}Memory Information{Colors.RESET}")
    print(f"{Colors.DARK_GREY}{'─' * 50}{Colors.RESET}")
    
    if memory_info:
        mem = memory_info['virtual']
        print(f"Total: {Colors.BLUE}{format_bytes(mem['total'])}{Colors.RESET} {Colors.DARK_GREY}<- Total RAM installed{Colors.RESET}")
        print(f"Used: {Colors.RED}{format_bytes(mem['used'])} ({mem['percent']:.1f}%){Colors.RESET} {Colors.DARK_GREY}<- Currently in use{Colors.RESET}")
        print(f"Available: {Colors.GREEN}{format_bytes(mem['available'])}{Colors.RESET} {Colors.DARK_GREY}<- Free for new processes{Colors.RESET}")
        print(f"\n{create_progress_bar(mem['used'], mem['total'], '')}")
        
        if memory_info.get('swap'):
            swap = memory_info['swap']
            print(f"\n{Colors.DARK_VIOLET}{Colors.BOLD}Swap Memory{Colors.RESET}")
            print(f"{Colors.DARK_GREY}{'─' * 50}{Colors.RESET}")
            print(f"Total: {Colors.BLUE}{format_bytes(swap['total'])}{Colors.RESET} {Colors.DARK_GREY}<- Virtual memory on disk{Colors.RESET}")
            print(f"Used: {Colors.RED}{format_bytes(swap['used'])} ({swap['percent']:.1f}%){Colors.RESET} {Colors.DARK_GREY}<- Currently swapped out{Colors.RESET}")
            print(f"Free: {Colors.GREEN}{format_bytes(swap['free'])}{Colors.RESET} {Colors.DARK_GREY}<- Available swap space{Colors.RESET}")


def display_disk_info():
    """Display disk information only"""
    stats = get_system_stats()
    
    print(f"{Colors.DARK_VIOLET}{Colors.BOLD}Disk Information{Colors.RESET}")
    print(f"{Colors.DARK_GREY}{'─' * 50}{Colors.RESET}")
    
    if stats.get('disk_usage'):
        disk_total = stats.get('disk_total', 0)
        disk_used = stats.get('disk_used', 0)
        disk_percent = stats.get('disk_percent', 0)
        disk_free = stats.get('disk_free', 0)
        
        print(f"Total: {Colors.BLUE}{format_bytes(disk_total)}{Colors.RESET} {Colors.DARK_GREY}<- Total storage capacity{Colors.RESET}")
        print(f"Used: {Colors.RED}{format_bytes(disk_used)} ({disk_percent:.1f}%){Colors.RESET} {Colors.DARK_GREY}<- Space currently occupied{Colors.RESET}")
        print(f"Free: {Colors.GREEN}{format_bytes(disk_free)}{Colors.RESET} {Colors.DARK_GREY}<- Available storage space{Colors.RESET}")
        print(f"\n{create_progress_bar(disk_used, disk_total, '')}")
    else:
        print(f"{Colors.YELLOW}Disk information not available{Colors.RESET}")


def display_private_ip():
    """Display private IP address(es)"""
    interfaces = get_network_interfaces()
    
    print(f"{Colors.DARK_VIOLET}{Colors.BOLD}Private IP Addresses{Colors.RESET}")
    print(f"{Colors.DARK_GREY}{'─' * 50}{Colors.RESET}")
    
    if interfaces:
        for iface in interfaces:
            status = "UP" if iface.get('is_up', False) else "DOWN"
            status_color = Colors.GREEN if iface.get('is_up', False) else Colors.RED
            ip_address = iface['ip']
            interface_name = iface['name']
            
            # Determine if this is the main interface (not loopback)
            is_main = interface_name != 'lo' and iface.get('is_up', False)
            
            if is_main:
                print(f"{interface_name}: {Colors.BLUE}{ip_address}{Colors.RESET} {Colors.DARK_GREY}<- This is your private IP{Colors.RESET} [{status_color}{status}{Colors.RESET}]")
            else:
                print(f"{interface_name}: {Colors.BLUE}{ip_address}{Colors.RESET} {Colors.DARK_GREY}<- Local interface{Colors.RESET} [{status_color}{status}{Colors.RESET}]")
            
            if iface.get('netmask'):
                print(f"  Netmask: {Colors.DARK_GREY}{iface['netmask']}{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}No network interfaces found{Colors.RESET}")


def display_public_ip():
    """Display public IP address"""
    print(f"{Colors.DARK_VIOLET}{Colors.BOLD}Public IP Address{Colors.RESET}")
    print(f"{Colors.DARK_GREY}{'─' * 50}{Colors.RESET}")
    
    print(f"{Colors.BLUE}Fetching public IP...{Colors.RESET}")
    public_ip = get_public_ip()
    
    if public_ip:
        print(f"Public IP: {Colors.BLUE}{public_ip}{Colors.RESET} {Colors.DARK_GREY}<- This is your public IP{Colors.RESET}")
    else:
        print(f"{Colors.RED}Could not retrieve public IP address{Colors.RESET}")
        print(f"{Colors.DARK_GREY}(Check internet connection){Colors.RESET}")


def display_network_info():
    """Display network interfaces and connections"""
    from modules.network_monitor import get_network_stats
    
    network_data = get_network_stats()
    
    print(f"{Colors.DARK_VIOLET}{Colors.BOLD}Network Information{Colors.RESET}")
    print(f"{Colors.DARK_GREY}{'─' * 50}{Colors.RESET}")
    
    if network_data.get('interfaces'):
        print(f"\n{Colors.BLUE}{Colors.BOLD}Interfaces:{Colors.RESET} {Colors.DARK_GREY}<- Network adapters on your system{Colors.RESET}")
        for iface in network_data.get('interfaces', []):
            status = "UP" if iface.get('is_up', False) else "DOWN"
            status_color = Colors.GREEN if iface.get('is_up', False) else Colors.RED
            ip_address = iface['ip']
            interface_name = iface['name']
            
            if interface_name != 'lo' and iface.get('is_up', False):
                print(f"  {interface_name}: {Colors.BLUE}{ip_address}{Colors.RESET} {Colors.DARK_GREY}<- Your private IP{Colors.RESET} [{status_color}{status}{Colors.RESET}]")
            else:
                print(f"  {interface_name}: {Colors.BLUE}{ip_address}{Colors.RESET} [{status_color}{status}{Colors.RESET}]")
    
    if network_data.get('connections'):
        conn_count = len(network_data.get('connections', []))
        print(f"\n{Colors.BLUE}{Colors.BOLD}Active Connections: {conn_count}{Colors.RESET} {Colors.DARK_GREY}<- Current network sessions{Colors.RESET}")
        for conn in network_data.get('connections', [])[:10]:
            status = conn.get('status', 'UNKNOWN')
            status_color = Colors.BLUE if status == 'ESTABLISHED' else Colors.YELLOW
            local = conn.get('local_address', 'N/A')
            remote = conn.get('remote_address', 'N/A')
            print(f"  {status_color}{status}{Colors.RESET} {local} → {remote}")


def display_system_stats():
    """Display system statistics summary"""
    stats = get_system_stats()
    
    print(f"{Colors.DARK_VIOLET}{Colors.BOLD}System Statistics{Colors.RESET}")
    print(f"{Colors.DARK_GREY}{'─' * 50}{Colors.RESET}")
    
    cpu_percent = stats.get('cpu_percent', 0)
    cpu_cores = stats.get('cpu_count', 'N/A')
    memory_percent = stats.get('memory_percent', 0)
    memory_used = format_bytes(stats.get('memory_used', 0))
    memory_total = format_bytes(stats.get('memory_total', 0))
    
    print(f"CPU: {Colors.RED}{cpu_percent:.1f}%{Colors.RESET} ({Colors.BLUE}{cpu_cores} cores{Colors.RESET}) {Colors.DARK_GREY}<- Processor usage{Colors.RESET}")
    print(f"Memory: {Colors.RED}{memory_percent:.1f}%{Colors.RESET} ({memory_used} / {memory_total}) {Colors.DARK_GREY}<- RAM utilization{Colors.RESET}")
    
    if stats.get('disk_usage'):
        disk_percent = stats.get('disk_percent', 0)
        disk_used = format_bytes(stats.get('disk_used', 0))
        disk_total = format_bytes(stats.get('disk_total', 0))
        print(f"Disk: {Colors.RED}{disk_percent:.1f}%{Colors.RESET} ({disk_used} / {disk_total}) {Colors.DARK_GREY}<- Storage usage{Colors.RESET}")
    
    if stats.get('uptime'):
        uptime_str = format_uptime(stats.get('uptime', 0))
        print(f"Uptime: {Colors.BLUE}{uptime_str}{Colors.RESET} {Colors.DARK_GREY}<- System running time{Colors.RESET}")
    
    if stats.get('process_count'):
        process_count = stats.get('process_count', 0)
        print(f"Processes: {Colors.BLUE}{process_count}{Colors.RESET} {Colors.DARK_GREY}<- Running programs{Colors.RESET}")


def display_uptime():
    """Display system uptime"""
    stats = get_system_stats()
    
    print(f"{Colors.DARK_VIOLET}{Colors.BOLD}System Uptime{Colors.RESET}")
    print(f"{Colors.DARK_GREY}{'─' * 50}{Colors.RESET}")
    
    if stats.get('uptime'):
        uptime_str = format_uptime(stats.get('uptime', 0))
        print(f"Uptime: {Colors.BLUE}{uptime_str}{Colors.RESET} {Colors.DARK_GREY}<- Time since last reboot{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}Uptime information not available{Colors.RESET}")
