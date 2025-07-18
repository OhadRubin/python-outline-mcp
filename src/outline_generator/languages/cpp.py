"""C++ language configuration for outline generation."""

from typing import List
from ..core import LanguageConfig


class CppConfig(LanguageConfig):
    """C++ language configuration."""
    
    @property
    def language_name(self) -> str:
        """Name of the language for ast-grep."""
        return "cpp"
    
    @property
    def file_extensions(self) -> List[str]:
        """File extensions for C++ files."""
        return [".cpp", ".cc", ".cxx", ".hpp", ".hh", ".h"]
    
    @property
    def function_patterns(self) -> List[str]:
        """AST patterns for finding C++ functions."""
        return [
            "$RET $FUNC($$$) { $$$ }",
            "$FUNC($$$) { $$$ }",                        # constructors / destructors
            "template <$$$> $RET $FUNC($$$) { $$$ }",
            "template <$$$> $FUNC($$$) { $$$ }",
        ]
    
    @property
    def class_patterns(self) -> List[str]:
        """AST patterns for finding C++ classes and structs."""
        return [
            "class $CLASS { $$$ }",
            "struct $CLASS { $$$ }",
        ]
    
    @property
    def method_patterns(self) -> List[str]:
        """AST patterns for finding C++ methods within classes."""
        return [
            "$RET $METHOD($$$) { $$$ }",
            "$METHOD($$$) { $$$ }",
            "~$METHOD($$$) { $$$ }",                    # destructor
        ]