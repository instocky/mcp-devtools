"""
Интеграционные тесты для MCP Get Text Commit

Объединяет функциональность из test_manual.py, run_test.py и simple_test.py
для комплексного тестирования с реальными git репозиториями.
"""

import asyncio
import pytest
from pathlib import Path
from mcp_get_text_commit.commit_text_generator import CommitTextGenerator


class TestCommitGeneratorIntegration:
    """Интеграционные тесты для CommitTextGenerator"""

    @pytest.mark.asyncio
    async def test_fallback_with_invalid_directory(self):
        """Тест fallback функциональности с несуществующей директорией"""
        result = await CommitTextGenerator.generate(
            working_directory="C:\\not\\a\\git\\repo",
            style="conventional"
        )
        
        assert result.commit_text == "chore: update project files"
        assert result.confidence == 0.1
        assert result.files_analyzed == 0
        assert result.has_changes is True

    @pytest.mark.asyncio
    async def test_with_current_project_directory(self):
        """Тест с текущим проектом"""
        project_root = Path(__file__).parent.parent.parent
        
        result = await CommitTextGenerator.generate(
            working_directory=str(project_root),
            style="conventional"
        )
        
        # Результат может быть разным в зависимости от состояния репозитория
        assert isinstance(result.commit_text, str)
        assert isinstance(result.confidence, float)
        assert isinstance(result.files_analyzed, int)
        assert isinstance(result.has_changes, bool)
        assert 0.0 <= result.confidence <= 1.0

    @pytest.mark.asyncio
    async def test_with_specific_git_repo_path(self):
        """Тест с конкретным путем к git репозиторию"""
        # Используем путь, который был в оригинальном test_manual.py
        test_repo_path = "C:\\Projects\\MCP\\0720_mcp-devtools\\mcp-get-text-commit"
        
        if Path(test_repo_path).exists():
            result = await CommitTextGenerator.generate(
                working_directory=test_repo_path,
                style="conventional"
            )
            
            assert isinstance(result.commit_text, str)
            assert isinstance(result.confidence, float)
            assert isinstance(result.files_analyzed, int)
            assert isinstance(result.has_changes, bool)
            assert 0.0 <= result.confidence <= 1.0
        else:
            pytest.skip(f"Test repository path {test_repo_path} does not exist")

    @pytest.mark.asyncio
    async def test_different_commit_styles(self):
        """Тест различных стилей коммитов"""
        styles = ["conventional", "angular", "atom", "gitmoji"]
        project_root = Path(__file__).parent.parent.parent
        
        for style in styles:
            result = await CommitTextGenerator.generate(
                working_directory=str(project_root),
                style=style
            )
            
            assert isinstance(result.commit_text, str)
            assert isinstance(result.confidence, float)
            assert 0.0 <= result.confidence <= 1.0

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Тест обработки ошибок"""
        # Тест с None в качестве working_directory
        result = await CommitTextGenerator.generate(
            working_directory=None,
            style="conventional"
        )
        
        # Должен обрабатываться корректно и возвращать fallback
        assert isinstance(result.commit_text, str)
        assert isinstance(result.confidence, float)
        assert result.confidence >= 0.0


async def manual_test_basic():
    """Простой тест основной функциональности (из test_manual.py)"""
    try:
        print("🔍 Тестирование CommitTextGenerator...")
        
        # Тест без git репозитория (должен вернуть fallback)
        result = await CommitTextGenerator.generate(
            working_directory="C:\\not\\a\\git\\repo",
            style="conventional"
        )
        
        print(f"✅ Fallback результат: '{result.commit_text}'")
        print(f"   Confidence: {result.confidence}")
        print(f"   Files analyzed: {result.files_analyzed}")
        print(f"   Has changes: {result.has_changes}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False


async def manual_test_real_git():
    """Тест с реальным git репозиторием (из test_manual.py)"""
    try:
        print("\n🔍 Тестирование с реальным git репозиторием...")
        
        # Тест с текущим git репозиторием
        project_root = Path(__file__).parent.parent.parent
        result = await CommitTextGenerator.generate(
            working_directory=str(project_root),
            style="conventional"
        )
        
        print(f"✅ Real git результат: '{result.commit_text}'")
        print(f"   Confidence: {result.confidence}")
        print(f"   Files analyzed: {result.files_analyzed}")
        print(f"   Has changes: {result.has_changes}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_manual_tests():
    """Запуск ручных тестов для отладки"""
    print("🚀 Начинаем ручное тестирование MCP Get Text Commit...")
    
    success1 = await manual_test_basic()
    success2 = await manual_test_real_git()
    
    if success1 and success2:
        print("\n✅ Все ручные тесты прошли успешно!")
    else:
        print("\n❌ Есть ошибки в ручных тестах")
    
    return success1 and success2


if __name__ == "__main__":
    # Запуск ручных тестов для отладки
    asyncio.run(run_manual_tests())
