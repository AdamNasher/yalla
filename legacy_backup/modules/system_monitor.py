"""
System Monitor Module
Collects system metrics: CPU, memory, disk, processes, uptime
"""

import psutil
import time
from config import SHOW_PROCESS_COUNT, SHOW_UPTIME, SHOW_DISK_STATS


def get_system_stats():
    """Collect all system statistics"""
    stats = {}
    
    try:
        # CPU Usage
        stats['cpu_percent'] = psutil.cpu_percent(interval=0.1)
        
        # Memory Usage
        memory = psutil.virtual_memory()
        stats['memory_total'] = memory.total
        stats['memory_used'] = memory.used
        stats['memory_available'] = memory.available
        stats['memory_percent'] = memory.percent
        
        # Disk Usage - Cross-platform
        if SHOW_DISK_STATS:
            try:
                import platform
                system = platform.system()

                if system == 'Windows':
                    # On Windows, check C: drive first, then other drives
                    import os
                    drives = ['C:\\']
                    # Add other possible drives
                    for letter in 'DEFGHIJKLMNOPQRSTUVWXYZ':
                        drive = f'{letter}:\\'
                        if os.path.exists(drive):
                            drives.append(drive)
                            break  # Just use the first available drive after C:

                    disk_path = drives[0] if drives else 'C:\\'
                else:
                    # Unix-like systems (Linux, macOS)
                    disk_path = '/'

                disk = psutil.disk_usage(disk_path)
                stats['disk_total'] = disk.total
                stats['disk_used'] = disk.used
                stats['disk_free'] = disk.free
                stats['disk_percent'] = disk.percent
                stats['disk_usage'] = True
            except (PermissionError, OSError, ImportError):
                stats['disk_usage'] = False
        
        # Process Count
        if SHOW_PROCESS_COUNT:
            try:
                stats['process_count'] = len(psutil.pids())
            except:
                stats['process_count'] = 0
        
        # System Uptime
        if SHOW_UPTIME:
            try:
                boot_time = psutil.boot_time()
                stats['uptime'] = time.time() - boot_time
            except:
                stats['uptime'] = 0
        
        # CPU Count
        stats['cpu_count'] = psutil.cpu_count()
        
        # Load Average (Unix-like systems)
        try:
            stats['load_avg'] = psutil.getloadavg()
        except AttributeError:
            # Windows doesn't have load average
            stats['load_avg'] = None
        
    except Exception as e:
        # Graceful degradation
        stats['error'] = str(e)
        stats['cpu_percent'] = 0
        stats['memory_total'] = 0
        stats['memory_used'] = 0
    
    return stats


def get_top_processes(limit=5):
    """Get top processes by CPU usage"""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x.get('cpu_percent', 0) or 0, reverse=True)
        return processes[:limit]
    except:
        return []


def get_memory_info():
    """Get detailed memory information"""
    try:
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'virtual': {
                'total': memory.total,
                'used': memory.used,
                'available': memory.available,
                'percent': memory.percent
            },
            'swap': {
                'total': swap.total,
                'used': swap.used,
                'free': swap.free,
                'percent': swap.percent
            }
        }
    except:
        return None
