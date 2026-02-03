"""
UI Renderer for Yalla Security Dashboard
Handles ASCII art, colors, progress bars, and terminal layout
"""

import os
import sys
from yalla.config import Colors, PROGRESS_BAR_LENGTH, PROGRESS_BAR_FILLED, PROGRESS_BAR_EMPTY
from yalla.config import CPU_WARNING_THRESHOLD, CPU_CRITICAL_THRESHOLD
from yalla.config import MEMORY_WARNING_THRESHOLD, MEMORY_CRITICAL_THRESHOLD


def get_terminal_size():
    """Get terminal width and height"""
    try:
        import shutil
        size = shutil.get_terminal_size()
        # Ensure minimum width for proper rendering
        width = max(size.columns, 80)
        height = max(size.lines, 24)
        return width, height
    except:
        return 80, 24


def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')


def get_ascii_banner():
    """Generate ASCII art banner"""
    width = get_terminal_size()[0] - 4
    width = max(width, 64)  # Minimum width for the banner

    # Create a clean YALLA banner - all lines exactly 55 characters
    banner_lines = [
        f"{Colors.DARK_VIOLET}  ██╗   ██╗  █████╗  ██╗     ██╗      █████╗  {Colors.RESET}",  # 55 chars total
        f"{Colors.DARK_VIOLET}  ╚██╗ ██╔╝ ██╔══██╗ ██║     ██║     ██╔══██╗ {Colors.RESET}",  # 55 chars total
        f"{Colors.DARK_VIOLET}   ╚████╔╝  ███████║ ██║     ██║     ███████║{Colors.RESET}",   # 55 chars total
        f"{Colors.DARK_VIOLET}    ╚██╔╝   ██╔══██║ ██║     ██║     ██╔══██║ {Colors.RESET}",  # 55 chars total
        f"{Colors.DARK_VIOLET}     ██║    ██║  ██║ ███████╗ ███████╗ ██║  ██║{Colors.RESET}", # 55 chars total
        f"{Colors.DARK_VIOLET}     ╚═╝    ╚═╝  ╚═╝ ╚══════╝ ╚══════╝ ╚═╝  ╚═╝{Colors.RESET}", # 55 chars total
    ]

    # Center each line - all lines are now exactly 55 characters total
    ascii_width = 55
    centered_banner = []
    for line in banner_lines:
        padding = max(0, (width - ascii_width) // 2)
        centered_banner.append(' ' * padding + line)

    subtitle = f"{Colors.RED}🔒 Security Dashboard | Red Team Edition 🔒{Colors.RESET}"
    subtitle_padding = max(0, (width - 44) // 2)  # Approximate subtitle length

    banner = f"""
{Colors.DARK_VIOLET}◆{'━' * (width - 2)}◆{Colors.RESET}
{chr(10).join(centered_banner)}
{Colors.DARK_GREY}{' ' * subtitle_padding}{subtitle}
{Colors.DARK_VIOLET}◆{'━' * (width - 2)}◆{Colors.RESET}
"""
    return banner


def get_color_for_percentage(value, warning_threshold, critical_threshold):
    """Get color based on percentage value"""
    if value >= critical_threshold:
        return Colors.RED
    elif value >= warning_threshold:
        return Colors.YELLOW
    else:
        return Colors.GREEN


def create_progress_bar(value, max_value=100, label=""):
    """Create a visual progress bar"""
    if max_value == 0:
        percentage = 0
    else:
        percentage = min(100, (value / max_value) * 100)
    
    filled_length = int(PROGRESS_BAR_LENGTH * percentage / 100)
    bar = PROGRESS_BAR_FILLED * filled_length + PROGRESS_BAR_EMPTY * (PROGRESS_BAR_LENGTH - filled_length)
    
    color = get_color_for_percentage(percentage, CPU_WARNING_THRESHOLD, CPU_CRITICAL_THRESHOLD)
    
    return f"{label}{color}{bar}{Colors.RESET} {color}{percentage:.1f}%{Colors.RESET}"


def format_bytes(bytes_value):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def format_uptime(seconds):
    """Format uptime in seconds to human readable format"""
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


def create_section(title, content, color=Colors.DARK_VIOLET):
    """Create a simple section with symbols"""
    width = get_terminal_size()[0] - 4
    width = max(width, 60)

    # Use different symbols for different section types
    symbol = "●" if "System" in title else "▲" if "Network" in title else "◆"

    # Simple header with symbol and title
    header = f"{color}{symbol} {Colors.BOLD}{title}{Colors.RESET}"
    separator = f"{Colors.DARK_GREY}{'─' * width}{Colors.RESET}"

    return f"{header}\n{separator}\n{content}\n"


def render_dashboard(system_data, network_data):
    """Render the complete dashboard"""
    clear_screen()
    
    # Banner
    print(get_ascii_banner())
    
    # System Information Section
    cpu_percent = system_data.get('cpu_percent', 0)
    memory_used = system_data.get('memory_used', 0)
    memory_total = system_data.get('memory_total', 0)
    memory_percent = (memory_used / memory_total * 100) if memory_total > 0 else 0

    # Initialize disk variables
    disk_used = system_data.get('disk_used', 0)
    disk_total = system_data.get('disk_total', 0)

    sys_content = f"""  {Colors.BOLD}CPU Usage:{Colors.RESET} {Colors.DARK_GREY}<- Current processor utilization{Colors.RESET}
    {create_progress_bar(cpu_percent, 100, '')}

  {Colors.BOLD}Memory:{Colors.RESET} {format_bytes(memory_used)} / {format_bytes(memory_total)} {Colors.DARK_GREY}<- RAM usage{Colors.RESET}
    {create_progress_bar(memory_used, memory_total, '')}

  {Colors.BOLD}Disk Usage:{Colors.RESET} {format_bytes(disk_used)} / {format_bytes(disk_total)} {Colors.DARK_GREY}<- Storage usage{Colors.RESET}
    {create_progress_bar(disk_used, disk_total, '')}

"""

    if system_data.get('uptime'):
        uptime_str = format_uptime(system_data.get('uptime', 0))
        sys_content += f"""  {Colors.BOLD}Uptime:{Colors.RESET} {uptime_str} {Colors.DARK_GREY}<- Time since last reboot{Colors.RESET}

"""

    if system_data.get('process_count'):
        process_count = system_data.get('process_count', 0)
        sys_content += f"""  {Colors.BOLD}Running Processes:{Colors.RESET} {process_count} {Colors.DARK_GREY}<- Active programs{Colors.RESET}
"""
    
    sys_section = create_section("System Information", sys_content, Colors.DARK_VIOLET)
    print(sys_section)

    # Network Information Section
    net_content = ""
    
    if network_data.get('interfaces'):
        net_content += f"""  {Colors.BOLD}Network Interfaces:{Colors.RESET} {Colors.DARK_GREY}<- Your network adapters{Colors.RESET}
"""
        for iface in network_data.get('interfaces', [])[:5]:
            ip = iface.get('ip', 'N/A')
            name = iface.get('name', 'Unknown')
            is_main = name != 'lo' and iface.get('is_up', False)
            note = " <- Your private IP" if is_main else ""
            net_content += f"""    {Colors.RED}●{Colors.RESET} {name}: {Colors.BLUE}{ip}{Colors.RESET}{Colors.DARK_GREY}{note}{Colors.RESET}
"""

    if network_data.get('connections'):
        conn_count = len(network_data.get('connections', []))
        net_content += f"""  {Colors.BOLD}Active Connections:{Colors.RESET} {conn_count} {Colors.DARK_GREY}<- Current network sessions{Colors.RESET}
"""
        for conn in network_data.get('connections', [])[:5]:
            status = conn.get('status', 'UNKNOWN')
            laddr = conn.get('local_address', 'N/A')
            raddr = conn.get('remote_address', 'N/A')
            status_color = Colors.BLUE if status == 'ESTABLISHED' else Colors.YELLOW
            net_content += f"""    {status_color}{status}{Colors.RESET} {laddr} → {raddr}
"""

    if network_data.get('io_stats'):
        for iface_name, stats in list(network_data.get('io_stats', {}).items())[:3]:
            sent = format_bytes(stats.get('bytes_sent', 0))
            recv = format_bytes(stats.get('bytes_recv', 0))
            net_content += f"""  {Colors.BOLD}{iface_name}:{Colors.RESET} ↑ {Colors.RED}{sent}{Colors.RESET} ↓ {Colors.BLUE}{recv}{Colors.RESET} {Colors.DARK_GREY}<- Network traffic{Colors.RESET}
"""

    if not net_content:
        net_content = f"""  {Colors.YELLOW}No network data available{Colors.RESET}
"""
    
    net_section = create_section("Network Information", net_content, Colors.BLUE)
    print(net_section)

    # Footer
    width = get_terminal_size()[0] - 4
    width = max(width, 60)
    footer_text = "Press 'q' to quit | 'r' to refresh | Auto-refresh every 1.5s"
    centered_footer = footer_text.center(width)
    separator = f"{Colors.DARK_GREY}{'═' * width}{Colors.RESET}"

    print(separator)
    print(f"{Colors.BLUE}{centered_footer}{Colors.RESET}")
    print(separator)