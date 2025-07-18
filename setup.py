#!/usr/bin/env python3
"""Setup script for Multi-Language Outline Generator."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = []
requirements_file = this_directory / "requirements.txt"
if requirements_file.exists():
    requirements = requirements_file.read_text().strip().split('\n')

setup(
    name="outline-generator",
    version="1.0.0",
    description="Multi-language code outline generator using ast-grep",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/mcp_outline",
    
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    install_requires=requirements,
    
    entry_points={
        "console_scripts": [
            "outline=outline_generator.cli:main",
        ],
    },
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
    ],
    
    python_requires=">=3.7",
    
    keywords="outline ast-grep code-analysis python javascript typescript cpp java",
    
    project_urls={
        "Bug Reports": "https://github.com/yourusername/mcp_outline/issues",
        "Source": "https://github.com/yourusername/mcp_outline",
    },
)