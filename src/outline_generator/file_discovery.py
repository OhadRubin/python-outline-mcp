"""File discovery utilities with git integration."""

import subprocess
from pathlib import Path
from typing import List


def is_git_repo(path: str) -> bool:
    """Check if the given path is within a git repository."""
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


def get_git_files_by_extensions(path: str, extensions: List[str], recursive: bool = True) -> List[Path]:
    """Get files tracked by git matching the given extensions, respecting .gitignore."""
    all_files = []
    
    for ext in extensions:
        try:
            pattern = f"*{ext}"
            cmd = ["git", "ls-files", pattern]
            if recursive:
                cmd.append(f"**/{pattern}")
            
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
            files = [base_path / file_path for file_path in result.stdout.strip().split('\n') if file_path]
            all_files.extend(files)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            continue
    
    return all_files


def get_files_by_extensions(path: str, extensions: List[str], recursive: bool = True) -> List[Path]:
    """Get files by extensions using filesystem glob."""
    folder = Path(path)
    all_files = []
    
    for ext in extensions:
        if recursive:
            files = list(folder.rglob(f"*{ext}"))
        else:
            files = list(folder.glob(f"*{ext}"))
        all_files.extend(files)
    
    return all_files


def discover_files(path: str, extensions: List[str], recursive: bool = True, filter_gitignore: bool = True) -> tuple[List[Path], str]:
    """
    Discover files with given extensions in path.
    
    Returns:
        Tuple of (file_list, source_description)
    """
    folder = Path(path)
    
    if not folder.exists():
        return [], f"❌ Folder not found: {path}"
    
    if not folder.is_dir():
        return [], f"❌ Not a directory: {path}"
    
    # Find files - use git if available and filter_gitignore is True
    if filter_gitignore and is_git_repo(str(folder)):
        files = get_git_files_by_extensions(str(folder), extensions, recursive)
        source = "git-tracked"
    else:
        # Fallback to filesystem glob
        files = get_files_by_extensions(str(folder), extensions, recursive)
        source = "filesystem"
    
    if not files:
        ext_str = ", ".join(extensions)
        return [], f"❌ No {ext_str} files found in: {path}"
    
    ext_str = ", ".join(extensions)
    return files, f"🔍 Found {len(files)} {ext_str} files ({source})"