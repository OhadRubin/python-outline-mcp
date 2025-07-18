#!/usr/bin/env python3
"""Simple Python Function/Class Outline Generator using ast-grep"""

import sys
import os
import subprocess
from pathlib import Path
from ast_grep_py import SgRoot
from fastmcp import FastMCP


def is_git_repo(path: str) -> bool:
    """Check if the given path is within a git repository"""
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=path,
            capture_output=True,
            check=True,
            timeout=5
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return False


def get_git_python_files(path: str, recursive: bool = True) -> list[Path]:
    """Get Python files tracked by git, respecting .gitignore"""
    try:
        cmd = ["git", "ls-files", "*.py"]
        if recursive:
            cmd.append("**/*.py")
        
        result = subprocess.run(
            cmd,
            cwd=path,
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        
        # Convert relative paths to absolute Path objects
        base_path = Path(path)
        return [base_path / file_path for file_path in result.stdout.strip().split('\n') if file_path]
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return []


def generate_outline(file_path: str, show_filename: bool = True):
    """Generate outline showing only functions and classes with methods"""
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except Exception as e:
        return f"❌ Error reading {file_path}: {e}"

    root = SgRoot(content, "python")
    node = root.root()

    output = []
    
    if show_filename:
        output.append(f"📁 {os.path.basename(file_path)}")
        output.append("-" * 40)

    # Find top-level functions (not inside classes) - handle type annotations
    all_functions = node.find_all(pattern="def $FUNC($$$): $$$") + node.find_all(pattern="def $FUNC($$$) -> $$$: $$$")
    classes = node.find_all(pattern="class $CLASS: $$$") + node.find_all(
        pattern="class $CLASS($$$): $$$"
    )

    # Filter out methods (functions inside classes)
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

    # Add top-level functions
    for func in top_level_functions:
        func_name = func.get_match("FUNC").text()
        start_line = func.range().start.line + 1
        end_line = func.range().end.line + 1
        output.append(f"⚙️ def {func_name} ({start_line}-{end_line})")

    # Add classes with their methods
    for cls in classes:
        class_name = cls.get_match("CLASS").text()
        start_line = cls.range().start.line + 1
        end_line = cls.range().end.line + 1
        output.append(f"🏛️ class {class_name} ({start_line}-{end_line})")

        methods = cls.find_all(pattern="def $METHOD($$$): $$$") + cls.find_all(pattern="def $METHOD($$$) -> $$$: $$$")
        for method in methods:
            method_name = method.get_match("METHOD").text()
            method_start = method.range().start.line + 1
            method_end = method.range().end.line + 1
            output.append(f"  🔧 def {method_name} ({method_start}-{method_end})")

    return "\n".join(output) if output else "📄 No functions or classes found"


def process_folder(folder_path: str, recursive: bool = True, filter_gitignore: bool = True) -> str:
    """Process all Python files in a folder"""
    folder = Path(folder_path)

    if not folder.exists():
        return f"❌ Folder not found: {folder_path}"

    if not folder.is_dir():
        return f"❌ Not a directory: {folder_path}"

    # Find Python files - use git if available and filter_gitignore is True
    if filter_gitignore and is_git_repo(str(folder)):
        python_files = get_git_python_files(str(folder), recursive)
        source = "git-tracked"
    else:
        # Fallback to filesystem glob
        if recursive:
            python_files = list(folder.rglob("*.py"))
        else:
            python_files = list(folder.glob("*.py"))
        source = "filesystem"

    if not python_files:
        return f"❌ No Python files found in: {folder_path}"

    output = [f"🔍 Found {len(python_files)} Python files ({source})\n"]

    for py_file in sorted(python_files):
        try:
            outline = generate_outline(str(py_file), show_filename=True)
            output.append(outline)
            output.append("")  # Empty line between files
        except Exception as e:
            output.append(f"❌ Error processing {py_file.name}: {e}")

    return "\n".join(output)


# MCP Server
mcp = FastMCP("Python Outline Generator 🐍")


@mcp.tool
def python_outline(path: str, recursive: bool = True, filter_gitignore: bool = True) -> str:
    """Generate a Python code outline showing functions and classes with line numbers.
    
    Args:
        path: Path to a Python file or directory
        recursive: Search recursively in subdirectories (default: True)
        filter_gitignore: Respect .gitignore when in a git repository (default: True)
        
    Returns:
        Formatted outline showing functions and classes with line ranges
    """
    if os.path.isfile(path):
        return generate_outline(path, show_filename=True)
    elif os.path.isdir(path):
        return process_folder(path, recursive=recursive, filter_gitignore=filter_gitignore)
    else:
        return f"❌ Path not found: {path}"


if __name__ == "__main__":
    mcp.run()  # Default: uses STDIO transport