"""
Setup configuration for Yalla
"""

from setuptools import setup, find_packages

# Read version without importing the package (avoids import-time side effects during builds)
def read_version():
    import os
    version_ns = {}
    version_path = os.path.join(os.path.dirname(__file__), "yalla", "_version.py")
    with open(version_path, "r", encoding="utf-8") as f:
        exec(f.read(), version_ns)
    return version_ns.get("__version__", "0.0.0")

__version__ = read_version()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="yalla",
    version=__version__,
    author="Adam Nasher",
    description="Interactive Security Dashboard - Red Team Edition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AdamNasher/yalla",
    packages=find_packages(include=["yalla", "yalla.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "yalla=yalla.index:main",
        ],
    },
    include_package_data=True,
)
