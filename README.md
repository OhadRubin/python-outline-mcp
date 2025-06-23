# Python Outline MCP Tool 🐍

A single-serving MCP (Model Context Protocol) tool that generates Python code outlines using ast-grep.

## Features

- 🚀 Fast outline generation using ast-grep
- 📁 Works on single files or entire directories  
- 🔧 Handles type annotations (`-> str`, `-> int`, etc.)
- 📍 Shows line number ranges for functions and classes
- 🏛️ Hierarchical display (classes with their methods)

## Usage

### As MCP Server
```bash
python outline.py
```

### Example Output
```
📁 example.py
----------------------------------------
⚙️ def helper_function (15-20)
🏛️ class MyClass (25-45)
  🔧 def __init__ (28-32)
  🔧 def process (35-42)
```

## MCP Tool
The tool exposes a single MCP function:

- `python_outline(path: str, recursive: bool = True) -> str`

## Requirements
- Python 3.7+
- ast-grep-py
- fastmcp

## Installation
```bash
pip install ast-grep-py fastmcp
```