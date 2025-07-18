# Multi-Language Outline MCP Tool 🔍

A powerful MCP (Model Context Protocol) tool that generates code outlines for multiple programming languages using ast-grep.

## Features

- 🚀 Fast outline generation using ast-grep
- 🌍 **Multi-language support**: Python, JavaScript, TypeScript, C++, Java
- 📁 Works on single files or entire directories  
- 🔧 Language-specific parsing and structure detection
- 📍 Shows line number ranges for functions and classes
- 🏛️ Hierarchical display (classes with their methods)
- 🗂️ Git integration - respects .gitignore when available
- 🔄 Recursive directory scanning

## Supported Languages

- **Python** (`.py`) - `python`, `py`
- **JavaScript** (`.js`, `.jsx`) - `javascript`, `js`, `jsx`  
- **TypeScript** (`.ts`, `.tsx`) - `typescript`, `ts`, `tsx`
- **C++** (`.cpp`, `.cc`, `.cxx`, `.hpp`, `.hh`, `.h`) - `cpp`, `c++`, `cxx`
- **Java** (`.java`) - `java`

## Usage

### As CLI Tool

After installation, use the `outline` command:

```bash
# Basic usage - analyze Python files in current directory
outline -l py .

# Analyze specific file with language detection
outline --lang javascript src/component.js

# Analyze directory recursively for TypeScript files
outline -l ts src/

# Analyze without respecting .gitignore
outline --lang python --no-gitignore .

# Non-recursive analysis
outline --lang cpp --no-recursive src/

# Get help
outline --help
```

**Available options:**
- `--lang, --language, -l`: Specify language (python, js, ts, cpp, java, etc.)
- `--no-recursive`: Don't search subdirectories
- `--no-gitignore`: Don't respect .gitignore files

### As MCP Server

1. Clone the repo and install requirements:

```bash
git clone <repo-url>
cd mcp_outline
pip install -r requirements.txt
```

2. Add to Claude Code MCP:

```bash
claude mcp add -s user outline "python" "/path/to/mcp_outline/outline_mcp.py"
```

### Example Output

**Python:**

```text
📁 example.py
----------------------------------------
⚙️ def helper_function (15-20)
🏛️ class MyClass (25-45)
  🔧 def __init__ (28-32)
  🔧 def process (35-42)
```

**JavaScript:**

```text
📁 component.js
----------------------------------------
⚙️ def handleClick (5-8)
🏛️ class Button (10-25)
  🔧 def constructor (12-16)
  🔧 def render (18-24)
```

**C++:**

```text
📁 calculator.cpp
----------------------------------------
⚙️ def calculateSum (8-12)
🏛️ class Calculator (15-35)
  🔧 def add (18-22)
  🔧 def multiply (24-28)
```

## MCP Tool Functions

The tool exposes two MCP functions:

- `generate_outline(path: str, language: str = "python", recursive: bool = True, filter_gitignore: bool = True) -> str`
- `list_supported_languages() -> str`

## Requirements

- Python 3.7+
- ast-grep-py
- fastmcp

## Installation

### For CLI Usage

Install the package to get the `outline` command:

```bash
# Clone and install in development mode
git clone <repo-url>
cd mcp_outline
pip install -e .

# Now you can use the outline command
outline --help
outline -l python src/
```

### For MCP Server Only

```bash
pip install -r requirements.txt
```