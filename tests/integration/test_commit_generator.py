"""
Интеграционные тесты для CommitTextGenerator (v2, исправленный)
"""
import pytest
from pathlib import Path
from mcp_get_text_commit.commit_text_generator import CommitTextGenerator

pytestmark = pytest.mark.asyncio

@pytest.fixture
def project_root() -> Path:
    """Фикстура pytest, которая возвращает корневую директорию проекта."""
    return Path(__file__).parent.parent.parent

async def test_generate_in_real_git_repo(project_root: Path):
    """Тестирует генерацию сообщения коммита для реального Git репозитория."""
    result = await CommitTextGenerator.generate(
        working_directory=str(project_root),
        style="conventional"
    )
    assert result is not None, "Результат не должен быть None"
    if result.has_changes:
        print(f"Обнаружены изменения, сгенерирован коммит: '{result.commit_text}'")
        assert len(result.commit_text) > 0
        # ИСПРАВЛЕНО: проверяем само число, а не его длину
        assert result.files_analyzed > 0
    else:
        print("Изменения не обнаружены, коммит не сгенерирован.")
        assert result.commit_text == ""
        assert result.confidence == 0.0
        # ИСПРАВЛЕНО: проверяем само число, а не его длину
        assert result.files_analyzed == 0

async def test_generate_in_non_git_repo(tmp_path: Path):
    """Тестирует поведение для директории, не являющейся Git репозиторием."""
    result = await CommitTextGenerator.generate(
        working_directory=str(tmp_path),
        style="conventional"
    )
    assert result is not None
    assert result.commit_text == "chore: update project files"
    assert result.confidence == 0.1
    assert result.has_changes is True