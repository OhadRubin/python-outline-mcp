"""Command-line interface for the outline generator."""

import argparse
import sys
from typing import Dict, Type

from .core import OutlineGenerator, LanguageConfig
from .languages.python import PythonConfig
from .languages.javascript import JavaScriptConfig
from .languages.typescript import TypeScriptConfig
from .languages.cpp import CppConfig
from .languages.java import JavaConfig


# Registry of available language configurations
LANGUAGE_CONFIGS: Dict[str, Type[LanguageConfig]] = {
    "python": PythonConfig,
    "py": PythonConfig,  # Alias
    "javascript": JavaScriptConfig,
    "js": JavaScriptConfig,  # Alias
    "jsx": JavaScriptConfig,  # Alias
    "typescript": TypeScriptConfig,
    "ts": TypeScriptConfig,  # Alias
    "tsx": TypeScriptConfig,  # Alias
    "cpp": CppConfig,
    "c++": CppConfig,  # Alias
    "cxx": CppConfig,  # Alias
    "java": JavaConfig,
}


def get_language_config(language: str) -> LanguageConfig:
    """Get the language configuration for the specified language."""
    config_class = LANGUAGE_CONFIGS.get(language.lower())
    if not config_class:
        available = ", ".join(LANGUAGE_CONFIGS.keys())
        raise ValueError(f"Unsupported language '{language}'. Available: {available}")
    return config_class()


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate code outline showing functions and classes with line numbers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --lang python src/
  %(prog)s --lang py myfile.py --no-recursive
  %(prog)s --lang python . --no-gitignore
        """
    )
    
    parser.add_argument(
        "path",
        help="Path to a source file or directory"
    )
    
    parser.add_argument(
        "--lang", "--language", "-l",
        dest="language",
        default="python",
        help="Programming language (default: python). Available: " + ", ".join(LANGUAGE_CONFIGS.keys())
    )
    
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Don't search recursively in subdirectories"
    )
    
    parser.add_argument(
        "--no-gitignore",
        action="store_true",
        help="Don't respect .gitignore when in a git repository"
    )
    
    return parser


def main(args=None):
    """Main CLI entry point."""
    parser = create_parser()
    opts = parser.parse_args(args)
    
    try:
        # Get language configuration
        language_config = get_language_config(opts.language)
        
        # Create outline generator
        generator = OutlineGenerator(language_config)
        
        # Generate outline
        result = generator.generate_outline(
            path=opts.path,
            recursive=not opts.no_recursive,
            filter_gitignore=not opts.no_gitignore
        )
        
        print(result)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())