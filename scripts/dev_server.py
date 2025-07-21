#!/usr/bin/env python3
"""
Основной скрипт для запуска MCP Get Text Commit сервера в режиме разработки.

Этот скрипт настраивает логирование и запускает сервер.
Предполагается, что пакет установлен в режиме редактирования (`pip install -e .`),
поэтому нет необходимости в манипуляциях с sys.path.
"""

import logging
import sys

# Настройка логирования для разработки
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp-dev.log'), # Логи будут сохраняться в файл
        logging.StreamHandler(sys.stdout)   # и выводиться в консоль
    ]
)

# Импортируем функцию для создания сервера из установленного пакета
from mcp_get_text_commit.server import create_server

if __name__ == "__main__":
    # Создаем и запускаем сервер
    server = create_server()
    logging.info(f"Starting MCP server '{server.name}'...")
    server.run()