"""JavaScript language configuration for outline generation."""

from typing import List
from ..core import LanguageConfig


class JavaScriptConfig(LanguageConfig):
    """JavaScript language configuration."""
    
    @property
    def language_name(self) -> str:
        """Name of the language for ast-grep."""
        return "javascript"
    
    @property
    def file_extensions(self) -> List[str]:
        """File extensions for JavaScript files."""
        return [".js", ".jsx"]
    
    @property
    def function_patterns(self) -> List[str]:
        """AST patterns for finding JavaScript functions."""
        return [
            "function $FUNC($$$) { $$$ }",
            "export function $FUNC($$$) { $$$ }",
            "async function $FUNC($$$) { $$$ }",
            "export async function $FUNC($$$) { $$$ }",
            "const $FUNC = ($$$) => { $$$ }",
            "const $FUNC = () => { $$$ }",
        ]
    
    @property
    def class_patterns(self) -> List[str]:
        """AST patterns for finding JavaScript classes."""
        return [
            "class $CLASS { $$$ }",
            "class $CLASS extends $$$ { $$$ }",
            "export class $CLASS { $$$ }",
            "export class $CLASS extends $$$ { $$$ }",
        ]
    
    @property
    def method_patterns(self) -> List[str]:
        """AST patterns for finding JavaScript methods within classes."""
        # These patterns work for JavaScript/JSX methods
        return [
            "constructor($$$) { $$$ }",
            "$METHOD($$$) { $$$ }",
        ]