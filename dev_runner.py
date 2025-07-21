#!/usr/bin/env python3
"""
Development runner для MCP Get Text Commit

Запускает MCP сервер в development режиме для тестирования с Claude Desktop.
"""

import logging
import sys

# Настройка логирования для development
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp-dev.log'),
        logging.StreamHandler(sys.stderr)
    ]
)

if __name__ == "__main__":
    from mcp_get_text_commit.server import main
    main()
