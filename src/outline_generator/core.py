"""Core outline generation functionality."""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

from ast_grep_py import SgRoot

from .utils import format_filename, safe_read_file, format_line_range
from .file_discovery import discover_files


class LanguageConfig(ABC):
    """Abstract base class for language-specific configuration."""
    
    @property
    @abstractmethod
    def language_name(self) -> str:
        """Name of the language for ast-grep."""
        pass
    
    @property
    @abstractmethod
    def file_extensions(self) -> List[str]:
        """File extensions for this language (e.g., ['.py'])."""
        pass
    
    @property
    @abstractmethod
    def function_patterns(self) -> List[str]:
        """AST patterns for finding functions."""
        pass
    
    @property
    @abstractmethod
    def class_patterns(self) -> List[str]:
        """AST patterns for finding classes."""
        pass
    
    @property
    @abstractmethod
    def method_patterns(self) -> List[str]:
        """AST patterns for finding methods within classes."""
        pass


class OutlineGenerator:
    """Generic outline generator that works with any language configuration."""
    
    def __init__(self, language_config: LanguageConfig):
        self.config = language_config
    
    def generate_file_outline(self, file_path: str, show_filename: bool = True, base_path: str = None) -> str:
        """Generate outline showing only functions and classes with methods."""
        content, error = safe_read_file(file_path)
        if error:
            return error
        
        root = SgRoot(content, self.config.language_name)
        node = root.root()
        
        output = []
        
        if show_filename:
            filename_header = format_filename(file_path, show_filename, base_path)
            if filename_header:
                output.append(filename_header)
        
        # Find all functions and classes
        all_functions = self._find_all_by_patterns(node, self.config.function_patterns)
        classes = self._find_all_by_patterns(node, self.config.class_patterns)
        
        # Filter out methods (functions inside classes)
        top_level_functions = self._filter_top_level_functions(all_functions, classes)
        
        # Add top-level functions
        for func in top_level_functions:
            func_name = self._extract_name(func, "FUNC")
            start_line = func.range().start.line + 1
            end_line = func.range().end.line + 1
            output.append(f"⚙️ def {func_name} {format_line_range(start_line, end_line)}")
        
        # Add classes with their methods
        for cls in classes:
            class_name = self._extract_name(cls, "CLASS")
            start_line = cls.range().start.line + 1
            end_line = cls.range().end.line + 1
            output.append(f"🏛️ class {class_name} {format_line_range(start_line, end_line)}")
            
            try:
                methods = self._find_all_by_patterns(cls, self.config.method_patterns)
                for method in methods:
                    method_name = self._extract_name(method, "METHOD")
                    method_start = method.range().start.line + 1
                    method_end = method.range().end.line + 1
                    output.append(f"  🔧 def {method_name} {format_line_range(method_start, method_end)}")
            except Exception:
                # Fallback: try to extract methods manually for JavaScript/JSX
                if self.config.language_name in ["javascript", "typescript"]:
                    methods = self._extract_js_methods_fallback(cls)
                    for method_name, start_line, end_line in methods:
                        output.append(f"  🔧 def {method_name} {format_line_range(start_line, end_line)}")
        
        return "\n".join(output) if output else "📄 No functions or classes found"
    
    def process_folder(self, folder_path: str, recursive: bool = True, filter_gitignore: bool = True) -> str:
        """Process all files of the configured language in a folder."""
        files, status_msg = discover_files(
            folder_path, 
            self.config.file_extensions, 
            recursive, 
            filter_gitignore
        )
        
        if not files:
            return status_msg
        
        output = [status_msg + "\n"]
        
        for file_path in sorted(files):
            try:
                # Use current working directory as base path for relative paths
                outline = self.generate_file_outline(str(file_path), show_filename=True, base_path=os.getcwd())
                output.append(outline)
                output.append("")  # Empty line between files
            except Exception as e:
                output.append(f"❌ Error processing {file_path.name}: {e}")
        
        return "\n".join(output)
    
    def generate_outline(self, path: str, recursive: bool = True, filter_gitignore: bool = True) -> str:
        """Generate outline for a file or directory."""
        if os.path.isfile(path):
            # Use current working directory as base path for relative paths
            return self.generate_file_outline(path, show_filename=True, base_path=os.getcwd())
        elif os.path.isdir(path):
            return self.process_folder(path, recursive=recursive, filter_gitignore=filter_gitignore)
        else:
            return f"❌ Path not found: {path}"
    
    def _find_all_by_patterns(self, node, patterns: List[str]) -> List[Any]:
        """Find all matches for the given patterns."""
        matches = []
        for pattern in patterns:
            found = node.find_all(pattern=pattern)
            matches.extend(found)
        return matches
    
    def _filter_top_level_functions(self, all_functions: List[Any], classes: List[Any]) -> List[Any]:
        """Filter out methods (functions inside classes)."""
        top_level_functions = []
        for func in all_functions:
            func_line = func.range().start.line
            is_method = False
            
            for cls in classes:
                class_start = cls.range().start.line
                class_end = cls.range().end.line
                if class_start < func_line < class_end:
                    is_method = True
                    break
            
            if not is_method:
                top_level_functions.append(func)
        
        return top_level_functions
    
    def _extract_name(self, match: Any, capture_name: str) -> str:
        """Extract the captured name from a match."""
        try:
            return match.get_match(capture_name).text()
        except:
            # Fallback - try to get the text of the match itself
            return str(match)[:50] + "..." if len(str(match)) > 50 else str(match)
    
    def _extract_js_methods_fallback(self, cls) -> List[tuple[str, int, int]]:
        """Fallback method to extract JavaScript methods when patterns fail."""
        methods = []
        try:
            # Get the class text and parse it manually
            class_text = cls.text()
            lines = class_text.split('\n')
            class_start_line = cls.range().start.line
            
            for i, line in enumerate(lines):
                line = line.strip()
                # Look for method patterns manually
                if ('(' in line and '{' in line and 
                    not line.startswith('//') and 
                    not line.startswith('*') and
                    not line.startswith('const ') and
                    not line.startswith('let ') and
                    not line.startswith('var ') and
                    not line.startswith('if ') and
                    not line.startswith('for ') and
                    not line.startswith('while ')):
                    
                    # Extract method name
                    if line.startswith('constructor('):
                        method_name = 'constructor'
                    else:
                        # Find method name before the opening parenthesis
                        paren_idx = line.find('(')
                        if paren_idx > 0:
                            # Look backwards for the method name
                            method_part = line[:paren_idx].strip()
                            words = method_part.split()
                            if words:
                                method_name = words[-1]
                                if method_name not in ['if', 'for', 'while', 'function']:
                                    # Estimate line numbers (rough)
                                    start_line = class_start_line + i + 1
                                    end_line = start_line + 5  # Rough estimate
                                    methods.append((method_name, start_line, end_line))
        except Exception:
            pass
        
        return methods