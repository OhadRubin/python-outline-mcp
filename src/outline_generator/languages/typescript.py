"""TypeScript language configuration for outline generation."""

from typing import List
from ..core import LanguageConfig


class TypeScriptConfig(LanguageConfig):
    """TypeScript language configuration."""
    
    @property
    def language_name(self) -> str:
        """Name of the language for ast-grep."""
        return "typescript"
    
    @property
    def file_extensions(self) -> List[str]:
        """File extensions for TypeScript files."""
        return [".ts", ".tsx"]
    
    @property
    def function_patterns(self) -> List[str]:
        """AST patterns for finding TypeScript functions."""
        return [
            # without return type
            "function $FUNC($$$) { $$$ }",
            "export function $FUNC($$$) { $$$ }",
            "async function $FUNC($$$) { $$$ }",
            "export async function $FUNC($$$) { $$$ }",
            # with return type
            "function $FUNC($$$): $$$ { $$$ }",
            "export function $FUNC($$$): $$$ { $$$ }",
            "async function $FUNC($$$): $$$ { $$$ }",
            "export async function $FUNC($$$): $$$ { $$$ }",
        ]
    
    @property
    def class_patterns(self) -> List[str]:
        """AST patterns for finding TypeScript classes."""
        return [
            "class $CLASS { $$$ }",
            "class $CLASS extends $$$ { $$$ }",
            "export class $CLASS { $$$ }",
            "export class $CLASS extends $$$ { $$$ }",
        ]
    
    @property
    def method_patterns(self) -> List[str]:
        """AST patterns for finding TypeScript methods within classes."""
        return [
            "$METHOD($$$) { $$$ }",
            "$METHOD($$$): $$$ { $$$ }",
            "static $METHOD($$$) { $$$ }",
            "static $METHOD($$$): $$$ { $$$ }",
            "async $METHOD($$$) { $$$ }",
            "async $METHOD($$$): $$$ { $$$ }",
            "public $METHOD($$$) { $$$ }",
            "public $METHOD($$$): $$$ { $$$ }",
            "private $METHOD($$$) { $$$ }",
            "private $METHOD($$$): $$$ { $$$ }",
            "protected $METHOD($$$) { $$$ }",
            "protected $METHOD($$$): $$$ { $$$ }",
        ]