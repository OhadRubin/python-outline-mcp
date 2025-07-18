"""General utility functions for outline generation."""

import os


def format_line_range(start_line: int, end_line: int) -> str:
    """Format line range for display."""
    return f"({start_line}-{end_line})"


def format_filename(file_path: str, show_filename: bool = True) -> str:
    """Format filename for display in outline."""
    if not show_filename:
        return ""
    
    filename = os.path.basename(file_path)
    header = f"📁 {filename}"
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