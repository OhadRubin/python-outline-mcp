"""Java language configuration for outline generation."""

from typing import List
from ..core import LanguageConfig


class JavaConfig(LanguageConfig):
    """Java language configuration."""
    
    @property
    def language_name(self) -> str:
        """Name of the language for ast-grep."""
        return "java"
    
    @property
    def file_extensions(self) -> List[str]:
        """File extensions for Java files."""
        return [".java"]
    
    @property
    def function_patterns(self) -> List[str]:
        """AST patterns for finding Java functions (methods at top-level, which don't exist in Java)."""
        # Java doesn't have top-level functions, only methods inside classes
        return []
    
    @property
    def class_patterns(self) -> List[str]:
        """AST patterns for finding Java classes, interfaces, enums, and records."""
        return [
            "class $CLASS { $$$ }",
            "class $CLASS extends $$$ { $$$ }",
            "class $CLASS implements $$$ { $$$ }",
            "interface $CLASS { $$$ }",
            "interface $CLASS extends $$$ { $$$ }",
            "enum $CLASS { $$$ }",
            "record $CLASS($$$) { $$$ }",          # Java 16+
        ]
    
    @property
    def method_patterns(self) -> List[str]:
        """AST patterns for finding Java methods within classes."""
        return [
            "$RET $METHOD($$$) { $$$ }",
            "public $RET $METHOD($$$) { $$$ }",
            "private $RET $METHOD($$$) { $$$ }",
            "protected $RET $METHOD($$$) { $$$ }",
            "static $RET $METHOD($$$) { $$$ }",
            "public static $RET $METHOD($$$) { $$$ }",
            "private static $RET $METHOD($$$) { $$$ }",
            "$METHOD($$$) { $$$ }",  # constructors
            "public $METHOD($$$) { $$$ }",
            "private $METHOD($$$) { $$$ }",
            "protected $METHOD($$$) { $$$ }",
        ]