"""General utility functions for outline generation."""

import os


def format_line_range(start_line: int, end_line: int) -> str:
    """Format line range for display."""
    return f"({start_line}-{end_line})"


def format_filename(file_path: str, show_filename: bool = True, base_path: str = None) -> str:
    """Format filename for display in outline."""
    if not show_filename:
        return ""
    
    if base_path:
        try:
            # Show relative path from base directory
            display_path = os.path.relpath(file_path, base_path)
            # Avoid showing "./" prefix for files in current directory
            if display_path.startswith("./"):
                display_path = display_path[2:]
        except ValueError:
            # Fallback to basename if relative path calculation fails
            display_path = os.path.basename(file_path)
    else:
        display_path = os.path.basename(file_path)
    
    header = f"📁 {display_path}"
    separator = "-" * 40
    return f"{header}\n{separator}"


def safe_read_file(file_path: str) -> tuple[str, str | None]:
    """Safely read a file, returning content and error message if any."""
    try:
        with open(file_path, "r") as f:
            content = f.read()
        return content, None
    except Exception as e:
        return "", f"❌ Error reading {file_path}: {e}"