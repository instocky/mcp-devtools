#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы MCP сервера
"""

import sys
from pathlib import Path

# Добавляем src в path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

import asyncio
from mcp_get_text_commit.commit_text_generator import CommitTextGenerator


async def test_basic():
    """Простой тест основной функциональности"""
    try:
        print("🔍 Тестирование CommitTextGenerator...")
        
        # Тест с текущим git репозиторием
        result = await CommitTextGenerator.generate(
            working_directory=str(Path(__file__).parent),
            style="conventional"
        )
        
        print(f"✅ Результат:")
        print(f"   Commit text: '{result.commit_text}'")
        print(f"   Confidence: {result.confidence}")
        print(f"   Files analyzed: {result.files_analyzed}")
        print(f"   Has changes: {result.has_changes}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Основная функция"""
    print("🚀 Начинаем тестирование MCP Get Text Commit...")
    
    success = await test_basic()
    
    if success:
        print("\n✅ Тест прошел успешно!")
    else:
        print("\n❌ Есть ошибки в тесте")
    
    return success


if __name__ == "__main__":
    asyncio.run(main())
