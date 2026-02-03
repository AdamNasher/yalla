import subprocess
import sys
from yalla._version import __version__


def test_version_module_invocation():
    """Smoke test: `python -m yalla --version` should print the package version"""
    cp = subprocess.run([sys.executable, '-m', 'yalla', '--version'], capture_output=True, text=True)
    assert cp.returncode == 0
    assert __version__ in cp.stdout
