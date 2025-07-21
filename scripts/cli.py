#!/usr/bin/env python3
"""
Интерфейс командной строки (CLI) для генерации сообщений коммитов.

Этот скрипт позволяет генерировать commit message для указанной 
директории или для текущей директории по умолчанию.
"""

import asyncio
import argparse
from pathlib import Path

# Импортируем генератор из установленного пакета
from mcp_get_text_commit.commit_text_generator import CommitTextGenerator

async def main():
    """Основная асинхронная функция CLI."""
    parser = argparse.ArgumentParser(
        description="Генерирует сообщение для коммита на основе staged-изменений в Git."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Путь к Git-репозиторию. По умолчанию - текущая директория."
    )
    parser.add_argument(
        "--style",
        default="conventional",
        help="Стиль коммита (например, 'conventional'). По умолчанию - 'conventional'."
    )
    args = parser.parse_args()

    repo_path = Path(args.directory).resolve()
    print(f"Анализирую staged изменения в: {repo_path}")

    try:
        result = await CommitTextGenerator.generate(
            working_directory=str(repo_path),
            style=args.style
        )
        
        if not result.has_changes:
            print("\nНет staged изменений для анализа.")
            return

        print("\n--- Сгенерированное сообщение ---")
        print(result.commit_text)
        print("---------------------------------")
        print(f"\nУверенность: {result.confidence:.2f}")
        print(f"Проанализировано файлов: {len(result.files_analyzed)}")

    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())