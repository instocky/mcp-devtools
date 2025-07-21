"""
Unit Tests для Git Commit Intelligence (v2, исправленный)
"""

import pytest
from unittest.mock import AsyncMock, patch

from mcp_get_text_commit.commit_text_generator import CommitTextGenerator
from mcp_get_text_commit.models import GetTextCommitResult, GitCommandError

@pytest.mark.asyncio
async def test_generate_feat_commit():
    """Тест генерации feature коммита (УСПЕШНЫЙ СЦЕНАРИЙ)"""
    with patch('mcp_get_text_commit.git_analyzer.GitAnalyzer.is_git_repository', return_value=True), \
         patch('mcp_get_text_commit.git_analyzer.GitAnalyzer.collect_git_data') as mock_collect:
        mock_collect.return_value = {
            "staged_files": ["src/user_controller.py"],
            "staged_diff": "+def register_user(self):\n+    pass",
            "current_branch": "feature/user-registration",
            "project_rules": None
        }
        result = await CommitTextGenerator.generate(
            working_directory="/test/repo", style="conventional", logger=AsyncMock()
        )
        assert result.commit_text.startswith("feat:")
        assert result.confidence > 0.5
        # ИСПРАВЛЕНО: проверяем само число, а не его длину
        assert result.files_analyzed == 1
        assert result.has_changes is True

@pytest.mark.asyncio
async def test_no_staged_changes():
    """Тест случая без staged изменений"""
    with patch('mcp_get_text_commit.git_analyzer.GitAnalyzer.is_git_repository', return_value=True), \
         patch('mcp_get_text_commit.git_analyzer.GitAnalyzer.collect_git_data') as mock_collect:
        mock_collect.return_value = {"staged_files": [], "staged_diff": ""}
        result = await CommitTextGenerator.generate(working_directory=None, style="conventional")
        assert result.commit_text == ""
        assert result.confidence == 0.0
        # ИСПРАВЛЕНО: проверяем само число, а не его длину
        assert result.files_analyzed == 0
        assert result.has_changes is False

@pytest.mark.asyncio
async def test_docs_only_commit():
    """Тест коммита с изменениями только в документации (УСПЕШНЫЙ СЦЕНАРИЙ)"""
    with patch('mcp_get_text_commit.git_analyzer.GitAnalyzer.is_git_repository', return_value=True), \
         patch('mcp_get_text_commit.git_analyzer.GitAnalyzer.collect_git_data') as mock_collect:
        mock_collect.return_value = {
            "staged_files": ["README.md", "docs/api.md"],
            "staged_diff": "+# New Documentation\n+This is new content",
            "current_branch": "docs/update-readme",
            "project_rules": None
        }
        result = await CommitTextGenerator.generate(
            working_directory="/test/repo", style="conventional", logger=AsyncMock()
        )
        assert result.commit_text.startswith("docs:")
        assert result.confidence > 0.8
        # ИСПРАВЛЕНО: проверяем само число, а не его длину
        assert result.files_analyzed == 2
        assert result.has_changes is True

@pytest.mark.asyncio
async def test_not_git_repository():
    """Тест обработки случая когда директория не является git репозиторием"""
    with patch('mcp_get_text_commit.git_analyzer.GitAnalyzer.is_git_repository', return_value=False):
        result = await CommitTextGenerator.generate(
            working_directory="/not/git/repo", style="conventional", logger=AsyncMock()
        )
        # Ожидаем правильный fallback для этого случая
        assert result.commit_text == "chore: update project files"
        assert result.confidence == 0.1

@pytest.mark.asyncio
async def test_git_command_error():
    """Тест обработки ошибок git команд"""
    with patch('mcp_get_text_commit.git_analyzer.GitAnalyzer.is_git_repository', return_value=True), \
         patch('mcp_get_text_commit.git_analyzer.GitAnalyzer.collect_git_data') as mock_collect:
        mock_collect.side_effect = GitCommandError("Git command failed")
        result = await CommitTextGenerator.generate(
            working_directory="/test/repo", style="conventional", logger=AsyncMock()
        )
        # ИСПРАВЛЕНО: Ожидаем правильный fallback именно для этой ошибки
        assert result.commit_text == "chore: misc changes"
        assert result.confidence == 0.2