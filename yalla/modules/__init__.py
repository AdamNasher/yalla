"""yalla.modules package"""
from .system_monitor import get_system_stats, get_top_processes, get_memory_info
from .network_monitor import get_network_stats, get_public_ip
from .ui_renderer import render_dashboard, clear_screen
from .info_display import (
    display_cpu_info, display_memory_info, display_disk_info,
    display_private_ip, display_public_ip, display_network_info,
    display_system_stats, display_uptime
)
