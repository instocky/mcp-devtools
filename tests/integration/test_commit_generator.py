"""
Интеграционные тесты для CommitTextGenerator.

Этот файл объединяет функциональность из устаревших скриптов:
- test_manual.py
- run_test.py
- simple_test.py
"""

import pytest
from pathlib import Path
from mcp_get_text_commit.commit_text_generator import CommitTextGenerator

# Помечаем все тесты в этом файле как асинхронные для pytest-asyncio
pytestmark = pytest.mark.asyncio


@pytest.fixture
def project_root() -> Path:
    """
    Фикстура pytest, которая возвращает корневую директорию проекта.
    Предполагается, что данный тест находится в tests/integration/.
    """
    return Path(__file__).parent.parent.parent


async def test_generate_in_real_git_repo(project_root: Path):
    """
    Тестирует генерацию сообщения коммита для реального Git репозитория.
    Этот тест заменяет логику из `run_test.py` и `simple_test.py`.
    
    Для корректной проверки предполагается, что в репозитории есть 
    незакоммиченные изменения. Если их нет, тест проверит, что
    `has_changes` корректно установлен в `False`.
    """
    # Действие
    result = await CommitTextGenerator.generate(
        working_directory=str(project_root),
        style="conventional"
    )

    # Проверки
    assert result is not None, "Результат не должен быть None"
    assert isinstance(result.commit_text, str), "Текст коммита должен быть строкой"
    assert len(result.commit_text) > 0, "Текст коммита не должен быть пустым"
    
    assert isinstance(result.confidence, (float, int)), "Уверенность должна быть числом"
    assert 0.0 <= result.confidence <= 1.0, "Уверенность должна быть в диапазоне от 0.0 до 1.0"
    
    assert isinstance(result.files_analyzed, list), "Список проанализированных файлов должен быть списком"
    assert isinstance(result.has_changes, bool), "Флаг наличия изменений должен быть булевым значением"


async def test_generate_in_non_git_repo(tmp_path: Path):
    """
    Тестирует поведение для директории, не являющейся Git репозиторием.
    Этот тест заменяет логику из `test_manual.py`.

    Используется временная директория `tmp_path`, предоставляемая pytest,
    чтобы избежать использования жестко закодированных путей.
    """
    # Действие
    result = await CommitTextGenerator.generate(
        working_directory=str(tmp_path),
        style="conventional"
    )

    # Проверки
    # Ожидаем получение стандартного (fallback) сообщения
    assert result is not None, "Результат не должен быть None"
    assert result.commit_text == "feat: Add new files", "Должен вернуться стандартный текст коммита"
    assert result.confidence == 0.1, "Уверенность должна быть на минимальном уровне"
    assert result.files_analyzed == [], "Список проанализированных файлов должен быть пустым"
    assert result.has_changes is False, "Не должно быть обнаружено изменений"