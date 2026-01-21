# Yalla - Interactive Security Dashboard

A terminal-based security dashboard with real-time system monitoring, network analysis, and cybersecurity aesthetics. Built for red team enthusiasts and security professionals who want a cool, functional tool that looks impressive on GitHub.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platforms](https://img.shields.io/badge/platforms-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![USB Ready](https://img.shields.io/badge/USB-Ready-orange.svg)
[![Release](https://img.shields.io/github/v/release/yourusername/yalla)](https://github.com/yourusername/yalla/releases)
[![Build](https://img.shields.io/github/actions/workflow/status/yourusername/yalla/build.yml)](https://github.com/yourusername/yalla/actions)

## Features

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
  - Real-time auto-refresh

- **Cross-Platform & Portable**
  - Native support for Windows, macOS, and Linux
  - USB-ready executables (no installation required)
  - Single-file executables with embedded Python runtime
  - Non-blocking keyboard input with platform-specific handling
  - Clean exit handling and modular architecture

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/yalla.git
cd yalla
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make `yalla` command available system-wide (choose one method):

   **Option A: Create symlink in ~/.local/bin (Recommended - No sudo needed)**
   ```bash
   mkdir -p ~/.local/bin
   ln -s /path/to/Yalla/yalla ~/.local/bin/yalla
   ```
   Note: `~/.local/bin` is usually already in your PATH. If not, add it to your shell config.

   **Option B: Create symlink in /usr/local/bin (Requires sudo)**
   ```bash
   sudo ln -s /path/to/Yalla/yalla /usr/local/bin/yalla
   ```

   **Option C: Add alias (Quick setup)**
   ```bash
   # Add to your shell config (~/.zshrc, ~/.bashrc, etc.)
   alias yalla='cd /path/to/Yalla && python3 index.py'
   
   # Then reload your shell
   source ~/.zshrc  # or source ~/.bashrc
   ```

### Portable USB Distribution

For maximum portability, use the pre-built executables that run directly from USB drives:

1. **Download the USB package** from [Releases](https://github.com/yourusername/yalla/releases)

2. **Extract to USB drive** - the entire `Yalla-USB` folder can be copied to any USB drive

3. **Run directly from USB**:
   ```bash
   # Windows
   Yalla-USB/scripts/run_yalla_windows.bat

   # Linux/macOS
   Yalla-USB/scripts/run_yalla_unix.sh

   # Universal (requires Python)
   Yalla-USB/scripts/run_yalla_python.py
   ```

### Platform-Specific Executables

Download pre-built executables for your platform from [Releases](https://github.com/yourusername/yalla/releases):

- **Windows**: `yalla-windows-x86_64.zip` - Extract and run `yalla.exe`
- **macOS**: `yalla-darwin-x86_64.tar.gz` - Extract and run `yalla`
- **Linux**: `yalla-linux-x86_64.tar.gz` - Extract and run `yalla`

No installation required - these are fully self-contained executables.

### Building from Source

To build executables for your platform:

```bash
# Install build dependencies
pip install pyinstaller psutil colorama

# Build for current platform
python build.py

# Build for specific platform (limited cross-compilation support)
python build.py windows    # Windows executable
python build.py linux      # Linux executable
python build.py darwin     # macOS executable

# Create USB distribution package
python create_usb_package.py
```

## Usage

### Interactive Dashboard Mode

Run the full interactive dashboard:
```bash
yalla
```

Or run directly:
```bash
python index.py
```

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

## Configuration

Edit `config.py` to customize:

- Refresh interval
- Color themes
- Display preferences
- Threshold values for warnings/critical alerts

## Platform Compatibility

Yalla is fully cross-platform and tested on:

### ✅ Supported Platforms

| Platform | Version | Architecture | Status |
|----------|---------|--------------|---------|
| **Windows** | 7 SP1+ | x86_64 | ✅ Full Support |
| **macOS** | 10.12+ | x86_64, ARM64 | ✅ Full Support |
| **Linux** | Kernel 3.2+ | x86_64, ARM64 | ✅ Full Support |

### 🔧 System Requirements

- **RAM**: 100 MB free
- **Disk**: 50 MB free space
- **Python**: 3.7+ (for source installation)
- **Permissions**: System monitoring access (may require admin/sudo)

### 🚨 Security Considerations

- Yalla requires system monitoring permissions
- On some systems, you may need to run as administrator or grant specific permissions
- No data is transmitted - all monitoring is local

### 🛠️ Troubleshooting

**Permission Issues**:
- Windows: Run as Administrator
- macOS: Grant "System Events" permission in Security & Privacy
- Linux: Use `sudo` or configure polkit

**Display Issues**:
- Ensure terminal supports UTF-8 encoding
- Use a monospace font for best results

## Project Structure

```
Yalla/
├── index.py                 # Main entry point
├── _version.py              # Version information
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── build.py                 # Cross-platform build script
├── release.py               # Release automation helper
├── create_usb_package.py    # USB distribution creator
├── yalla.spec              # PyInstaller configuration
├── CHANGELOG.md            # Release notes and history
├── README.md               # This documentation
├── .gitignore              # Git ignore rules
├── .github/
│   └── workflows/
│       └── build.yml       # CI/CD for automated builds
└── modules/
    ├── __init__.py
    ├── system_monitor.py   # Cross-platform system metrics
    ├── network_monitor.py  # Network statistics & interfaces
    ├── ui_renderer.py      # Terminal UI with ASCII art
    └── info_display.py     # Command-line info functions
```

## Dependencies

### Runtime Dependencies
- **psutil** - Cross-platform system and process utilities
- **colorama** - Cross-platform colored terminal text

### Build Dependencies (Optional)
- **pyinstaller** - Creates standalone executables
- **setuptools** - Python package management
- **wheel** - Python package distribution

## USB Distribution

Yalla includes a complete USB-ready distribution system:

### USB Package Structure
```
Yalla-USB/
├── executables/
│   ├── windows/yalla.exe     # Windows executable
│   ├── macos/yalla          # macOS executable
│   └── linux/yalla          # Linux executable
├── scripts/
│   ├── run_yalla_windows.bat # Windows launcher
│   ├── run_yalla_unix.sh     # Unix launcher
│   └── run_yalla_python.py   # Universal Python launcher
├── docs/
│   ├── platform_requirements.md
│   └── troubleshooting.md
└── README.md                 # USB usage instructions
```

### Key Features
- **Zero Installation**: Runs directly from USB on any supported platform
- **Platform Detection**: Automatically selects the correct executable
- **Fallback Support**: Includes Python launcher for systems without pre-built binaries
- **Comprehensive Docs**: Platform requirements and troubleshooting guides
- **Launcher Scripts**: One-click execution with automatic platform detection

### Distribution Benefits
- **Portable Security Toolkit**: Carry your monitoring tools anywhere
- **Air-Gapped Systems**: Works on isolated networks without internet access
- **Multi-Platform Coverage**: Single USB works across Windows, macOS, and Linux
- **Version Consistency**: All platforms run the same version simultaneously

## Releases & Distribution

### Automated Releases

Yalla uses GitHub Actions for automated cross-platform builds and releases:

- **Trigger**: Push a version tag (e.g., `v1.1.0`)
- **Builds**: Automatic compilation for Windows, macOS, and Linux
- **Assets**: All executables and USB packages uploaded automatically
- **Release Notes**: Auto-generated from commit messages

### Creating a Release

#### Option 1: Automated (Recommended)
```bash
# Use the release helper script
python release.py 1.1.0

# This will:
# - Update version numbers
# - Update changelog
# - Create git commit and tag
# - Trigger GitHub Actions release
```

#### Option 2: Manual Process
```bash
# Update version
echo '__version__ = "1.1.0"' > _version.py

# Update CHANGELOG.md (move unreleased items to new version)

# Commit and tag
git add .
git commit -m "Release v1.1.0"
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin main --tags
```

### Release Assets

Each release includes:
- `yalla-linux-x86_64.tar.gz` - Linux executable (~15MB)
- `yalla-windows-x86_64.zip` - Windows executable (~20MB)
- `yalla-darwin-x86_64.tar.gz` - macOS executable (~15MB)
- `yalla-usb-package.zip` - Complete USB distribution (~50MB)

## Future Enhancements

- Port scanner integration
- Vulnerability scanner
- Log file monitoring
- Alert system for anomalies
- Export functionality (JSON/CSV)
- Customizable widgets
- Plugin system for third-party modules
- Web-based dashboard option
- Docker container support

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

MIT License - feel free to use this project for your resume, portfolio, or personal use.

## Author

Built with ❤️ for the cybersecurity community

---

**Note**: This tool is for educational and monitoring purposes. Always ensure you have proper authorization before monitoring systems or networks.
