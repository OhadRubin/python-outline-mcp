#!/usr/bin/env python3
"""Entry point for the refactored outline generator CLI."""

import sys
from pathlib import Path

# Add src to path so we can import our modules
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from outline_generator.cli import main

if __name__ == "__main__":
    sys.exit(main())