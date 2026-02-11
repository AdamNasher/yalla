# Yalla - Interactive Security Dashboard

A terminal-based security dashboard with real-time system monitoring, network analysis, and cybersecurity aesthetics. Built for red team enthusiasts and security professionals who want a cool, functional tool that looks impressive on GitHub.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platforms](https://img.shields.io/badge/platforms-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
[![Release](https://img.shields.io/github/v/release/AdamNasher/yalla)](https://github.com/AdamNasher/yalla/releases)
[![Build Status](https://img.shields.io/badge/status-active-brightgreen.svg)](https://github.com/AdamNasher/yalla)

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/AdamNasher/yalla.git
cd yalla
pip install -r requirements.txt

# Run the dashboard
python -m yalla
```

That's it! You'll see a beautiful real-time security dashboard in your terminal.

## 📊 Features

- **Real-time System Monitoring**
  - CPU usage with visual progress bars
  - Memory statistics (used/total/percentage)
  - Disk usage monitoring
  - Running processes count
  - System uptime display

- **Network Analysis**
  - Network interface enumeration with IP addresses
  - Active network connections monitoring
  - Network I/O statistics (bytes sent/received)
  - Connection state tracking

- **Cybersecurity Aesthetics**
  - ASCII art banner with red team theme
  - Color-coded metrics (green/yellow/red thresholds)
  - Terminal-based UI with borders and sections
  - Real-time auto-refresh (1.5 seconds)

- **Cross-Platform & Portable**
  - Windows, macOS, and Linux support
  - Single package installation
  - Command-line interface with multiple display options
  - Non-blocking keyboard input
  - Clean, modular architecture

## 📦 Installation

### Option 1: Quick Install (Recommended)

```bash
git clone https://github.com/AdamNasher/yalla.git
cd yalla
pip install -r requirements.txt
python -m yalla
```

### Option 2: Install as Package

```bash
git clone https://github.com/AdamNasher/yalla.git
cd yalla
pip install -e .
yalla  # Now available as a command
```

### Option 3: Pre-built Executables

Download from [Releases](https://github.com/AdamNasher/yalla/releases):
- **Windows**: `yalla-windows-x86_64.zip`
- **macOS**: `yalla-darwin-x86_64.tar.gz`
- **Linux**: `yalla-linux-x86_64.tar.gz`

Extract and run directly - no Python installation needed!

**Controls (Interactive Mode)**:
- **q** - Quit the dashboard
- **r** - Manual refresh (auto-refreshes every 1.5 seconds)
- **Ctrl+C** - Emergency exit

### Command-Line Options

Get specific information using flags:

```bash
# CPU information only
yalla -c
yalla --cpu

# Memory information only
yalla -m
yalla --memory

# Disk information only
yalla -d
yalla --disk

# Private IP address(es)
yalla -i
yalla --ip

# Public IP address
yalla -p
yalla --public-ip

# Network interfaces and connections
yalla -n
yalla --network

# System statistics summary
yalla -s
yalla --stats

# System uptime
yalla -u
yalla --uptime

# Combine multiple flags
yalla -c -m          # CPU and memory info
yalla -i -p           # Private and public IP
yalla -c -m -d        # CPU, memory, and disk
```

**Available Short Flags**:
- `-c, --cpu` - Display CPU information only
- `-m, --memory` - Display memory information only
- `-d, --disk` - Display disk information only
- `-i, --ip` - Display private IP address(es)
- `-p, --public-ip` - Display public IP address
- `-n, --network` - Display network interfaces and connections
- `-s, --stats` - Display system statistics summary
- `-u, --uptime` - Display system uptime
- `-h, --help` - Show help message

### Command-Line Options

Get specific information without the interactive dashboard:

```bash
# Display CPU information
python -m yalla -c

# Display memory information
python -m yalla -m

# Display disk information
python -m yalla -d

# Display private IP address
python -m yalla -i

# Display public IP address
python -m yalla -p

# Display network interfaces and connections
python -m yalla -n

# Display system statistics summary
python -m yalla -s

# Display system uptime
python -m yalla -u

# Combine multiple options
python -m yalla -c -m -d    # CPU, memory, disk info
python -m yalla -i -p        # Private and public IP
```

## ⚙️ Configuration

Edit `yalla/config.py` to customize:

- **Refresh interval** (default: 1.5 seconds)
- **Color themes** (dark violet, red, blue)
- **Display preferences** (which metrics to show)
- **Threshold values** (warning/critical levels)

## 📋 Requirements

### Minimum

- Python 3.7+
- 100 MB free RAM
- 50 MB disk space

### Permissions

- System monitoring access
- May require `sudo`/Administrator on some systems

## ✅ Platform Support

| Platform | Version | Architecture | Status |
|----------|---------|--------------|---------|
| **Windows** | 7 SP1+ | x86_64 | ✅ Full Support |
| **macOS** | 10.12+ | x86_64, ARM64 | ✅ Full Support |
| **Linux** | Kernel 3.2+ | x86_64, ARM64 | ✅ Full Support |

## 📁 Project Structure

```
yalla/
├── yalla/
│   ├── __init__.py
│   ├── __main__.py
│   ├── index.py              # Main entry point
│   ├── config.py             # Configuration
│   ├── _version.py           # Version info
│   └── modules/
│       ├── system_monitor.py # CPU, memory, disk metrics
│       ├── network_monitor.py # Network interfaces & connections
│       ├── ui_renderer.py     # Terminal UI & ASCII art
│       └── info_display.py    # CLI display functions
├── tests/                    # Test suite
├── build.py                  # Build executables
├── setup.py                  # Package setup
├── pyproject.toml            # Project metadata
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## 🔧 Building Executables

To create standalone executables for distribution:

```bash
# Install build dependencies
pip install pyinstaller

# Build for your current platform
python build.py

# Build for specific platform
python build.py linux
python build.py windows
python build.py darwin
```

## 📝 License

MIT License - feel free to use for your resume, portfolio, or personal projects.

## 👤 Author

**Adam Nasher** - Built with ❤️ for the cybersecurity community

---

**Disclaimer**: This tool is for educational and authorized monitoring purposes only. Always ensure you have proper authorization before monitoring systems or networks.
