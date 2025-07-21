#!/usr/bin/env python3
"""
Dev runner для MCP Get Text Commit сервера

Standalone entry point для dev mode без проблем с relative imports.
"""

import sys
from pathlib import Path

# Добавляем src в path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Импортируем сервер
from mcp_get_text_commit.server import create_server

# Создаем server объект для MCP dev
mcp = create_server()

if __name__ == "__main__":
    mcp.run()
