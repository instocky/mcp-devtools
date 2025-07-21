"""
MCP Get Text Commit - Git Commit Intelligence

Модуль для анализа git изменений и генерации качественных commit messages
в формате Conventional Commits через Model Context Protocol.
"""

__version__ = "0.3.0"
__author__ = "MCP DevTools"
__email__ = "dev@mcptools.com"

from .server import create_server, main

__all__ = ["create_server", "main", "__version__"]
