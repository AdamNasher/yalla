"""
Configuration settings for Yalla Security Dashboard
"""

# Refresh interval in seconds
REFRESH_INTERVAL = 1.5

# Color theme settings
class Colors:
    """Terminal color codes - Dark violet/red/dark grey/blue theme"""
    # Primary theme colors
    DARK_VIOLET = '\033[38;5;92m'  # Dark violet (256 color mode)
    DARK_VIOLET_ALT = '\033[35m'   # Magenta fallback
    RED = '\033[91m'               # Bright red
    RED_ALT = '\033[31m'           # Standard red
    DARK_GREY = '\033[90m'         # Dark grey
    DARK_GREY_ALT = '\033[38;5;240m'  # Dark grey (256 color mode)
    BLUE = '\033[94m'              # Bright blue
    BLUE_ALT = '\033[34m'          # Standard blue
    CYAN_BLUE = '\033[96m'         # Cyan-blue
    
    # Bright variants
    BRIGHT_RED = '\033[1;91m'
    BRIGHT_BLUE = '\033[1;94m'
    BRIGHT_VIOLET = '\033[1;35m'
    
    # Status colors (using theme)
    GREEN = '\033[92m'             # Keep green for normal status
    YELLOW = '\033[93m'            # Keep yellow for warnings
    
    # Reset
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

# Thresholds for color coding
CPU_WARNING_THRESHOLD = 70
CPU_CRITICAL_THRESHOLD = 90
MEMORY_WARNING_THRESHOLD = 75
MEMORY_CRITICAL_THRESHOLD = 90

# Display preferences
SHOW_PROCESS_COUNT = True
SHOW_UPTIME = True
SHOW_DISK_STATS = True
MAX_NETWORK_CONNECTIONS = 10
MAX_PROCESSES_DISPLAY = 5

# Progress bar settings
PROGRESS_BAR_LENGTH = 30
PROGRESS_BAR_FILLED = '█'
PROGRESS_BAR_EMPTY = '░'
