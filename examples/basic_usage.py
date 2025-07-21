"""
Пример 1: Базовое использование CommitTextGenerator.

Этот скрипт показывает, как программно сгенерировать сообщение
коммита для текущей директории.

Для запуска этого примера убедитесь, что пакет установлен:
pip install -e .
"""

import asyncio
from pathlib import Path
from mcp_get_text_commit.commit_text_generator import CommitTextGenerator

async def run_example():
    """Генерация сообщения для текущей директории."""
    print("=== Пример: генерация для текущей директории ===")
    
    # Определяем рабочую директорию (где находится этот скрипт)
    current_directory = Path(__file__).parent

    try:
        result = await CommitTextGenerator.generate(
            working_directory=str(current_directory),
            style="conventional"
        )
        
        print("\nСгенерированный commit message:")
        print("-" * 50)
        print(result.commit_text)
        print("-" * 50)
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(run_example())