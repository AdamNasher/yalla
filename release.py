#!/usr/bin/env python3
"""
Yalla Release Helper Script
Automates the release process for creating new versions
"""

import os
import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime

def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=check,
                              capture_output=True, text=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()

def get_current_version():
    """Get current version from _version.py"""
    with open('_version.py', 'r') as f:
        content = f.read()
        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        return match.group(1) if match else None

def update_version(new_version):
    """Update version in _version.py"""
    with open('_version.py', 'r') as f:
        content = f.read()

    # Update version
    content = re.sub(
        r'__version__\s*=\s*["\']([^"\']+)["\']',
        f'__version__ = "{new_version}"',
        content
    )

    with open('_version.py', 'w') as f:
        f.write(content)

    print(f"✅ Updated version to {new_version}")

def update_changelog(version):
    """Update CHANGELOG.md with new version section"""
    today = datetime.now().strftime('%Y-%m-%d')

    with open('CHANGELOG.md', 'r') as f:
        content = f.read()

    # Find the unreleased section
    unreleased_pattern = r'## \[Unreleased\]\n\n(.*?)(?=\n## \[\d+\.\d+\.\d+\])'
    match = re.search(unreleased_pattern, content, re.DOTALL)

    if match:
        unreleased_content = match.group(1).strip()
        new_version_section = f'## [{version}] - {today}\n\n{unreleased_content}\n\n## [Unreleased]\n\n### Added\n### Changed\n### Fixed'

        # Replace unreleased section with new version
        content = re.sub(unreleased_pattern, new_version_section, content, flags=re.DOTALL)

        with open('CHANGELOG.md', 'w') as f:
            f.write(content)

        print(f"✅ Updated changelog for version {version}")
    else:
        print("⚠️  Could not find [Unreleased] section in CHANGELOG.md")

def create_git_tag(version):
    """Create and push git tag"""
    tag_name = f'v{version}'

    # Create annotated tag
    success, output = run_command(f'git tag -a {tag_name} -m "Release {tag_name}"')
    if not success:
        print(f"❌ Failed to create tag: {output}")
        return False

    # Push tag
    success, output = run_command(f'git push origin {tag_name}')
    if not success:
        print(f"❌ Failed to push tag: {output}")
        return False

    print(f"✅ Created and pushed tag {tag_name}")
    return True

def validate_version(version):
    """Validate semantic version format"""
    if not re.match(r'^\d+\.\d+\.\d+$', version):
        print("❌ Invalid version format. Use: MAJOR.MINOR.PATCH (e.g., 1.2.3)")
        return False
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python release.py <version>")
        print("Example: python release.py 1.1.0")
        sys.exit(1)

    new_version = sys.argv[1]

    if not validate_version(new_version):
        sys.exit(1)

    current_version = get_current_version()
    print(f"Current version: {current_version}")
    print(f"New version: {new_version}")

    # Confirm
    response = input(f"Create release {new_version}? (y/N): ").lower().strip()
    if response not in ['y', 'yes']:
        print("Aborted.")
        sys.exit(0)

    # Update version
    update_version(new_version)

    # Update changelog
    update_changelog(new_version)

    # Stage changes
    run_command('git add _version.py CHANGELOG.md')

    # Commit
    run_command(f'git commit -m "Release v{new_version}"')

    # Create and push tag
    if create_git_tag(new_version):
        print("\n🎉 Release created successfully!")
        print(f"GitHub Actions will now build and create the release automatically.")
        print(f"Check: https://github.com/yourusername/yalla/releases")
    else:
        print("\n❌ Release process completed but tag creation failed.")
        print("You may need to create the tag manually.")

if __name__ == "__main__":
    main()