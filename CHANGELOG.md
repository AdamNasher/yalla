# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Cross-platform support for Windows, macOS, and Linux
- USB-ready portable distribution with auto-launcher scripts
- PyInstaller build system for creating standalone executables
- GitHub Actions CI/CD for automated cross-platform builds
- Comprehensive platform compatibility documentation

### Changed
- Improved ASCII banner with proper alignment
- Enhanced disk monitoring with cross-platform drive detection
- Updated UI with cleaner, more professional styling

### Fixed
- Platform-specific disk monitoring issues
- Terminal alignment problems across different screen sizes
- Color rendering inconsistencies

## [1.0.0] - 2024-01-XX

### Added
- Interactive security dashboard with real-time monitoring
- System monitoring: CPU, memory, disk usage, and processes
- Network monitoring: interfaces, connections, and I/O statistics
- Command-line interface with multiple display options
- Color-coded progress bars and status indicators
- ASCII art banner with cybersecurity theme
- Modular architecture for easy extension

### Technical Features
- Cross-platform terminal UI with colorama
- Non-blocking keyboard input handling
- Configurable refresh intervals and thresholds
- Platform-specific terminal compatibility (Unix/Windows)

---

## Release Process

### Creating a New Release

1. **Update Version**:
   ```bash
   # Update _version.py
   __version__ = "1.1.0"
   ```

2. **Update Changelog**:
   - Move unreleased changes to new version section
   - Add release date

3. **Create Git Tag**:
   ```bash
   git add .
   git commit -m "Release v1.1.0"
   git tag -a v1.1.0 -m "Release v1.1.0"
   git push origin main --tags
   ```

4. **Automated Release**:
   - GitHub Actions will automatically build all platforms
   - Create release with uploaded assets
   - Generate release notes from commits

### Release Assets

Each release includes:
- `yalla-linux-x86_64.tar.gz` - Linux executable
- `yalla-windows-x86_64.zip` - Windows executable
- `yalla-darwin-x86_64.tar.gz` - macOS executable
- `yalla-usb-package.zip` - Complete USB distribution package

### Version Numbering

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)