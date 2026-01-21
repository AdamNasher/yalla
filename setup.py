"""
Setup configuration for Yalla
"""

from setuptools import setup, find_packages
from _version import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="yalla",
    version=__version__,
    author="Your Name",
    description="Interactive Security Dashboard - Red Team Edition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/yalla",
    packages=find_packages(),
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
            "yalla=index:main",
        ],
    },
    include_package_data=True,
)
