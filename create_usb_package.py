#!/usr/bin/env python3
"""
Create USB distribution package for Yalla
Creates a portable USB package with executables for all platforms
"""

import os
import shutil
import platform
from pathlib import Path

def create_usb_package():
    """Create a USB-ready distribution package"""

    # Create USB directory structure
    usb_dir = Path("Yalla-USB")
    usb_dir.mkdir(exist_ok=True)

    # Create subdirectories
    executables_dir = usb_dir / "executables"
    docs_dir = usb_dir / "docs"
    scripts_dir = usb_dir / "scripts"

    executables_dir.mkdir(exist_ok=True)
    docs_dir.mkdir(exist_ok=True)
    scripts_dir.mkdir(exist_ok=True)

    # Copy executables (if they exist)
    if Path("dist").exists():
        for exe_file in Path("dist").glob("*"):
            if exe_file.is_file():
                shutil.copy2(exe_file, executables_dir)

    # Create platform-specific directories
    platforms = ["windows", "macos", "linux"]
    for plat in platforms:
        plat_dir = executables_dir / plat
        plat_dir.mkdir(exist_ok=True)

        # Create placeholder files
        placeholder = plat_dir / f"yalla-{plat}-placeholder.txt"
        placeholder.write_text(f"Yalla executable for {plat} will be placed here.\n"
                             f"Build this using: python build.py {plat}")

    # Create launcher scripts
    create_launcher_scripts(scripts_dir)

    # Create documentation
    create_documentation(docs_dir)

    # Create README for USB package
    create_usb_readme(usb_dir)

    # Create archive
    archive_name = "yalla-usb-package"
    shutil.make_archive(archive_name, 'zip', usb_dir)

    print(f"✅ USB package created: {archive_name}.zip")
    print(f"📁 Package structure:")
    print(f"   Yalla-USB/")
    print(f"   ├── executables/     # Platform executables")
    print(f"   ├── scripts/         # Launcher scripts")
    print(f"   ├── docs/           # Documentation")
    print(f"   └── README.md       # USB usage instructions")

    return True

def create_launcher_scripts(scripts_dir):
    """Create cross-platform launcher scripts"""

    # Windows batch launcher
    windows_launcher = scripts_dir / "run_yalla_windows.bat"
    windows_launcher.write_text("""@echo off
REM Yalla Launcher for Windows
echo Detecting Yalla executable...

if exist "..\\executables\\windows\\yalla.exe" (
    echo Running Windows executable...
    "..\\executables\\windows\\yalla.exe" %*
) else if exist "..\\executables\\yalla.exe" (
    echo Running Windows executable...
    "..\\executables\\yalla.exe" %*
) else (
    echo Error: Yalla executable not found!
    echo Please ensure yalla.exe is in the executables folder.
    pause
)
""")

    # Linux/macOS shell launcher
    unix_launcher = scripts_dir / "run_yalla_unix.sh"
    unix_launcher.write_text("""#!/bin/bash
# Yalla Launcher for Linux/macOS
echo "Detecting Yalla executable..."

# Detect current platform
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
else
    echo "Unsupported platform: $OSTYPE"
    exit 1
fi

# Try platform-specific executable first
if [ -f "../executables/$PLATFORM/yalla" ]; then
    echo "Running $PLATFORM executable..."
    chmod +x "../executables/$PLATFORM/yalla"
    "../executables/$PLATFORM/yalla" "$@"
# Fall back to generic executable
elif [ -f "../executables/yalla" ]; then
    echo "Running generic executable..."
    chmod +x "../executables/yalla"
    "../executables/yalla" "$@"
else
    echo "Error: Yalla executable not found!"
    echo "Please ensure the yalla executable is in the executables folder."
    exit 1
fi
""")

    # Make Unix script executable
    unix_launcher.chmod(0o755)

    # Universal Python launcher (fallback)
    python_launcher = scripts_dir / "run_yalla_python.py"
    python_launcher.write_text("""#!/usr/bin/env python3
# Universal Yalla launcher using system Python
import sys
import os
from pathlib import Path

def main():
    script_dir = Path(__file__).parent
    usb_root = script_dir.parent

    # Check for executable first
    exe_paths = [
        usb_root / "executables" / "yalla.exe",  # Windows
        usb_root / "executables" / "yalla",      # Unix
    ]

    for exe_path in exe_paths:
        if exe_path.exists():
            print(f"Running executable: {exe_path}")
            os.system(f'"{exe_path}" {" ".join(sys.argv[1:])}')
            return

    # Fallback to Python script (if available)
    yalla_script = usb_root / "yalla.py"
    if yalla_script.exists():
        print("Running Python script...")
        os.system(f'python3 "{yalla_script}" {" ".join(sys.argv[1:])}')
        return

    print("Error: No Yalla executable or script found!")
    print("Please ensure Yalla is properly installed in the USB package.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
""")

def create_documentation(docs_dir):
    """Create documentation files"""

    # Platform requirements
    requirements = docs_dir / "platform_requirements.md"
    requirements.write_text("""# Yalla Platform Requirements

## Windows
- Windows 7 SP1 or later
- No additional dependencies (fully portable)

## macOS
- macOS 10.12 Sierra or later
- No additional dependencies (fully portable)

## Linux
- Kernel 3.2 or later
- glibc 2.17 or later
- No additional dependencies (fully portable)

## Hardware Requirements
- 100 MB free RAM
- 50 MB free disk space
- Terminal/console access

## Security Note
Yalla requires system monitoring permissions to display hardware statistics.
On some systems, you may need to grant permissions or run as administrator.
""")

    # Troubleshooting
    troubleshooting = docs_dir / "troubleshooting.md"
    troubleshooting.write_text("""# Troubleshooting Yalla

## Common Issues

### "Permission denied" or "Access denied"
**Cause**: System monitoring requires elevated permissions
**Solution**:
- Windows: Run as Administrator
- macOS/Linux: Use `sudo` or grant permissions

### "Command not found" or "File not found"
**Cause**: Executable not in correct location
**Solution**:
- Ensure executable is in the `executables/` folder
- Use the provided launcher scripts

### Blank or garbled display
**Cause**: Terminal encoding issues
**Solution**:
- Windows: Use Command Prompt or PowerShell with UTF-8 support
- Linux/macOS: Ensure UTF-8 locale is set

### No network information displayed
**Cause**: Network monitoring permissions
**Solution**:
- Grant network access permissions
- Some corporate networks may restrict monitoring

## Getting Help

If you encounter issues not covered here:
1. Check the platform requirements
2. Try running with administrator/root privileges
3. Verify the executable integrity
4. Contact support with system details
""")

def create_usb_readme(usb_dir):
    """Create USB package README"""

    readme = usb_dir / "README.md"
    readme.write_text("""# Yalla - Portable Security Dashboard

A cross-platform security monitoring dashboard that runs directly from USB.

## Quick Start

### Windows
1. Insert USB drive
2. Run `scripts\\run_yalla_windows.bat`
3. Or directly run `executables\\windows\\yalla.exe`

### Linux/macOS
1. Insert USB drive
2. Run `scripts/run_yalla_unix.sh`
3. Or directly run `executables/linux/yalla` or `executables/macos/yalla`

### Universal (Python required)
1. Ensure Python 3.7+ is installed
2. Run `scripts/run_yalla_python.py`

## Features

- **Real-time CPU monitoring**
- **Memory usage statistics**
- **Disk space analysis**
- **Network interface detection**
- **Active connection monitoring**
- **System uptime tracking**
- **Process counting**

## Controls

- `q` - Quit the dashboard
- `r` - Refresh data manually
- `Ctrl+C` - Force quit

## Platform Support

- ✅ Windows 7+ (32-bit & 64-bit)
- ✅ macOS 10.12+ (Intel & Apple Silicon)
- ✅ Linux (Ubuntu 16.04+, CentOS 7+, etc.)

## Security Note

Yalla requires system monitoring permissions. You may need to:
- Run as Administrator (Windows)
- Use `sudo` (Linux/macOS)
- Grant accessibility permissions (macOS)

## Troubleshooting

See `docs/troubleshooting.md` for common issues and solutions.

## Build Your Own

To build executables for your platform:

```bash
# Install dependencies
pip install pyinstaller psutil colorama

# Build for current platform
python build.py

# Build for specific platform (cross-compilation limited)
python build.py windows  # or linux, darwin
```

## License

MIT License - See project repository for details.

---
**Yalla** - Stay secure, stay informed! 🔒
""")

if __name__ == "__main__":
    create_usb_package()