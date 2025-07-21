"""
Пример 2: Использование CommitTextGenerator с указанием конкретного пути.

Этот скрипт показывает, как сгенерировать сообщение для коммита,
указав путь к другому репозиторию.

Для запуска этого примера убедитесь, что пакет установлен:
pip install -e .
"""

import asyncio
from mcp_get_text_commit.commit_text_generator import CommitTextGenerator

async def run_example_for_path():
    """Анализ конкретной директории."""
    print("=== Пример: генерация для конкретного пути ===")
    
    # !!! ВАЖНО !!!
    # Замените этот путь на путь к вашему локальному репозиторию.
    path_to_your_repo = "C:/Projects/MyOtherProject"
    
    print(f"Анализирую staged изменения в: {path_to_your_repo}")

    try:
        result = await CommitTextGenerator.generate(
            working_directory=path_to_your_repo,
            style="conventional"
        )
        
        print("\nСгенерированный commit message:")
        print("-" * 60)
        print(result.commit_text)
        print("-" * 60)
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(run_example_for_path())