"""
Network Monitor Module
Collects network statistics: interfaces, connections, I/O
"""

import psutil
import socket
from yalla.config import MAX_NETWORK_CONNECTIONS


def get_network_interfaces():
    """Get all network interfaces with their IP addresses"""
    interfaces = []
    
    try:
        net_if_addrs = psutil.net_if_addrs()
        net_if_stats = psutil.net_if_stats()
        
        for interface_name, addresses in net_if_addrs.items():
            interface_info = {
                'name': interface_name,
                'ip': None,
                'netmask': None,
                'broadcast': None,
                'is_up': False
            }
            
            # Get interface status
            if interface_name in net_if_stats:
                interface_info['is_up'] = net_if_stats[interface_name].isup
                interface_info['speed'] = net_if_stats[interface_name].speed
            
            # Get IPv4 address
            for addr in addresses:
                if addr.family == socket.AF_INET:  # IPv4
                    interface_info['ip'] = addr.address
                    interface_info['netmask'] = addr.netmask
                    if addr.broadcast:
                        interface_info['broadcast'] = addr.broadcast
                    break
            
            # Only include interfaces with IP addresses
            if interface_info['ip']:
                interfaces.append(interface_info)
    
    except Exception as e:
        # Graceful degradation
        pass
    
    return interfaces


def get_network_connections():
    """Get active network connections"""
    connections = []
    
    try:
        # Get all connections
        net_conns = psutil.net_connections(kind='inet')
        
        for conn in net_conns[:MAX_NETWORK_CONNECTIONS]:
            conn_info = {
                'status': conn.status,
                'local_address': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A",
                'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                'family': 'IPv4' if conn.family == socket.AF_INET else 'IPv6',
                'type': 'TCP' if conn.type == socket.SOCK_STREAM else 'UDP'
            }
            connections.append(conn_info)
    
    except (psutil.AccessDenied, PermissionError):
        # Some systems require elevated privileges
        pass
    except Exception:
        # Graceful degradation
        pass
    
    return connections


def get_network_io_stats():
    """Get network I/O statistics per interface"""
    io_stats = {}
    
    try:
        net_io = psutil.net_io_counters(pernic=True)
        
        for interface_name, stats in net_io.items():
            io_stats[interface_name] = {
                'bytes_sent': stats.bytes_sent,
                'bytes_recv': stats.bytes_recv,
                'packets_sent': stats.packets_sent,
                'packets_recv': stats.packets_recv,
                'errin': stats.errin,
                'errout': stats.errout,
                'dropin': stats.dropin,
                'dropout': stats.dropout
            }
    
    except Exception:
        # Graceful degradation
        pass
    
    return io_stats


def get_network_stats():
    """Get all network statistics"""
    stats = {
        'interfaces': get_network_interfaces(),
        'connections': get_network_connections(),
        'io_stats': get_network_io_stats()
    }
    
    return stats


def get_public_ip():
    """Attempt to get public IP address (requires internet)"""
    try:
        import urllib.request
        import json
        
        # Try multiple services
        services = [
            'https://api.ipify.org?format=json',
            'https://httpbin.org/ip',
            'https://api.myip.com'
        ]
        
        for service in services:
            try:
                with urllib.request.urlopen(service, timeout=3) as response:
                    data = json.loads(response.read().decode())
                    if 'ip' in data:
                        return data['ip']
                    elif 'origin' in data:
                        return data['origin']
            except:
                continue
    except:
        pass
    
    return None