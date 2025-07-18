"""Python language configuration for outline generation."""

from typing import List
from ..core import LanguageConfig


class PythonConfig(LanguageConfig):
    """Python language configuration."""
    
    @property
    def language_name(self) -> str:
        """Name of the language for ast-grep."""
        return "python"
    
    @property
    def file_extensions(self) -> List[str]:
        """File extensions for Python files."""
        return [".py"]
    
    @property
    def function_patterns(self) -> List[str]:
        """AST patterns for finding Python functions."""
        return [
            "def $FUNC($$$): $$$",           # Functions without type annotations
            "def $FUNC($$$) -> $$$: $$$"     # Functions with return type annotations
        ]
    
    @property
    def class_patterns(self) -> List[str]:
        """AST patterns for finding Python classes."""
        return [
            "class $CLASS: $$$",             # Classes without inheritance
            "class $CLASS($$$): $$$"         # Classes with inheritance or metaclass
        ]
    
    @property
    def method_patterns(self) -> List[str]:
        """AST patterns for finding Python methods within classes."""
        return [
            "def $METHOD($$$): $$$",         # Methods without type annotations
            "def $METHOD($$$) -> $$$: $$$"   # Methods with return type annotations
        ]