#!/usr/bin/env python3
"""Multi-Language Outline Generator MCP Server using refactored structure."""

import sys
from pathlib import Path

# Add src to path so we can import our modules
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from fastmcp import FastMCP
from outline_generator.cli import get_language_config, LANGUAGE_CONFIGS
from outline_generator.core import OutlineGenerator

# MCP Server
mcp = FastMCP("Multi-Language Outline Generator 🔍")


@mcp.tool
def generate_outline(path: str, language: str = "python", recursive: bool = True, filter_gitignore: bool = True) -> str:
    """Generate a code outline showing functions and classes with line numbers.
    
    Args:
        path: Path to a source file or directory
        language: Programming language (python, js, ts, cpp, java, etc.)
        recursive: Search recursively in subdirectories (default: True)
        filter_gitignore: Respect .gitignore when in a git repository (default: True)
        
    Returns:
        Formatted outline showing functions and classes with line ranges
    """
    try:
        language_config = get_language_config(language)
        generator = OutlineGenerator(language_config)
        return generator.generate_outline(
            path=path,
            recursive=recursive,
            filter_gitignore=filter_gitignore
        )
    except Exception as e:
        return f"❌ Error: {e}"


@mcp.tool
def list_supported_languages() -> str:
    """List all supported programming languages.
    
    Returns:
        List of supported languages and their aliases
    """
    langs = list(LANGUAGE_CONFIGS.keys())
    return f"Supported languages: {', '.join(sorted(langs))}"


if __name__ == "__main__":
    mcp.run()  # Default: uses STDIO transport