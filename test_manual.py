"""
Простой тест для проверки работы MCP сервера
"""

import asyncio
from mcp_get_text_commit.commit_text_generator import CommitTextGenerator


async def test_basic():
    """Простой тест основной функциональности"""
    try:
        print("Тестирование CommitTextGenerator...")
        
        # Тест без git репозитория (должен вернуть fallback)
        result = await CommitTextGenerator.generate(
            working_directory="C:\\not\\a\\git\\repo",
            style="conventional"
        )
        
        print(f"Fallback результат: '{result.commit_text}'")
        print(f"   Confidence: {result.confidence}")
        print(f"   Files analyzed: {result.files_analyzed}")
        print(f"   Has changes: {result.has_changes}")
        
        return True
        
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_real_git():
    """Тест с реальным git репозиторием"""
    try:
        print("Тестирование с реальным git репозиторием...")
        
        # Тест с текущим git репозиторием
        result = await CommitTextGenerator.generate(
            working_directory="C:\\Projects\\MCP\\0720_mcp-devtools\\mcp-get-text-commit",
            style="conventional"
        )
        
        print(f"Real git результат: '{result.commit_text}'")
        print(f"   Confidence: {result.confidence}")
        print(f"   Files analyzed: {result.files_analyzed}")
        print(f"   Has changes: {result.has_changes}")
        
        return True
        
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Основная функция"""
    print("Начинаем тестирование MCP Get Text Commit...")
    
    success1 = await test_basic()
    success2 = await test_real_git()
    
    if success1 and success2:
        print("\nВсе тесты прошли успешно!")
    else:
        print("\nЕсть ошибки в тестах")
    
    return success1 and success2


if __name__ == "__main__":
    asyncio.run(main())
