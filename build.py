#!/usr/bin/env python3
"""
Yalla Build Script
Creates cross-platform executables using PyInstaller
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True,
                              capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def build_executable(target_os=None, clean=True):
    """Build executable for specified platform"""

    if target_os is None:
        target_os = platform.system().lower()

    print(f"Building Yalla for {target_os}...")

    # Clean previous builds
    if clean:
        print("Cleaning previous builds...")
        os.system("rm -rf dist/ build/ *.spec")

    # Base PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (but we'll override for CLI tools)
        "--name=yalla",
        "--hidden-import=colorama",
        "--hidden-import=psutil",
    ]

    # Platform-specific settings
    if target_os == "windows":
        cmd.extend([
            "--hidden-import=msvcrt",  # Windows terminal handling
            "--hidden-import=ctypes.wintypes",
        ])
        exe_name = "yalla.exe"
    elif target_os == "darwin":  # macOS
        cmd.extend([
            "--hidden-import=termios",
            "--hidden-import=tty",
            "--hidden-import=select",
        ])
        exe_name = "yalla"
    else:  # Linux and others
        cmd.extend([
            "--hidden-import=termios",
            "--hidden-import=tty",
            "--hidden-import=select",
        ])
        exe_name = "yalla"

    # For CLI tools, we actually want a console window
    if "--windowed" in cmd:
        cmd.remove("--windowed")

    cmd.append("index.py")

    print(f"Running: {' '.join(cmd)}")
    success, output = run_command(" ".join(cmd))

    if success:
        print(f"✅ Build successful! Executable created: dist/{exe_name}")

        # Create platform-specific archive
        archive_name = f"yalla-{target_os}-{platform.machine()}"
        if target_os == "windows":
            archive_name += ".zip"
            run_command(f"cd dist && zip -r ../{archive_name} {exe_name}")
        else:
            archive_name += ".tar.gz"
            run_command(f"cd dist && tar -czf ../{archive_name} {exe_name}")

        print(f"📦 Archive created: {archive_name}")
        return True
    else:
        print(f"❌ Build failed: {output}")
        return False

def build_all_platforms():
    """Build for all supported platforms (when running on respective OS)"""
    current_os = platform.system().lower()

    print(f"Building for current platform: {current_os}")
    success = build_executable(current_os)

    if success:
        print(f"🎉 Yalla executable created for {current_os}!")
        print("To build for other platforms, run this script on those systems")
        print("or use cross-compilation tools.")

    return success

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_os = sys.argv[1].lower()
        build_executable(target_os)
    else:
        build_all_platforms()