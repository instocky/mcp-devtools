"""
Unit Tests для Git Commit Intelligence

Тесты основных компонентов генерации commit messages.
"""

import pytest
from unittest.mock import AsyncMock, patch

from mcp_get_text_commit.commit_text_generator import CommitTextGenerator
from mcp_get_text_commit.models import GetTextCommitParams


@pytest.mark.asyncio
async def test_generate_feat_commit():
    """Тест генерации feature коммита"""
    with patch('mcp_get_text_commit.git_analyzer.GitAnalyzer') as mock_analyzer_class:
        # Мокаем класс GitAnalyzer
        mock_analyzer = AsyncMock()
        mock_analyzer_class.return_value = mock_analyzer
        mock_analyzer_class.is_git_repository.return_value = True
        
        mock_analyzer.collect_git_data.return_value = {
            "staged_files": ["src/user_controller.py"],
            "staged_diff": "+def register_user(self):\n+    pass",
            "current_branch": "feature/user-registration", 
            "project_rules": None
        }
        
        result = await CommitTextGenerator.generate(
            working_directory="/test/repo", 
            style="conventional", 
            logger=AsyncMock()
        )
        
        assert result.commit_text.startswith("feat:")
        assert result.confidence > 0.8
        assert result.files_analyzed == 1
        assert result.has_changes is True


@pytest.mark.asyncio
async def test_no_staged_changes():
    """Тест случая без staged изменений"""
    with patch('mcp_get_text_commit.git_analyzer.GitAnalyzer') as mock_analyzer_class:
        mock_analyzer = AsyncMock()
        mock_analyzer_class.return_value = mock_analyzer
        mock_analyzer_class.is_git_repository.return_value = True
        
        mock_analyzer.collect_git_data.return_value = {
            "staged_files": [],
            "staged_diff": "",
            "current_branch": "main",
            "project_rules": None
        }
        
        result = await CommitTextGenerator.generate(
            working_directory=None, 
            style="conventional", 
            logger=AsyncMock()
        )
        
        assert result.commit_text == ""
        assert result.confidence == 0.0
        assert result.files_analyzed == 0
        assert result.has_changes is False


@pytest.mark.asyncio  
async def test_docs_only_commit():
    """Тест коммита с изменениями только в документации"""
    with patch('mcp_get_text_commit.git_analyzer.GitAnalyzer') as mock_analyzer_class:
        mock_analyzer = AsyncMock()
        mock_analyzer_class.return_value = mock_analyzer
        mock_analyzer_class.is_git_repository.return_value = True
        
        mock_analyzer.collect_git_data.return_value = {
            "staged_files": ["README.md", "docs/api.md"],
            "staged_diff": "+# New Documentation\n+This is new content",
            "current_branch": "docs/update-readme",
            "project_rules": None
        }
        
        result = await CommitTextGenerator.generate(
            working_directory="/test/repo",
            style="conventional",
            logger=AsyncMock()
        )
        
        assert result.commit_text.startswith("docs:")
        assert result.confidence > 0.9
        assert result.files_analyzed == 2
        assert result.has_changes is True


@pytest.mark.asyncio
async def test_not_git_repository():
    """Тест обработки случая когда директория не является git репозиторием"""
    with patch('mcp_get_text_commit.git_analyzer.GitAnalyzer') as mock_analyzer_class:
        mock_analyzer_class.is_git_repository.return_value = False
        
        result = await CommitTextGenerator.generate(
            working_directory="/not/git/repo",
            style="conventional", 
            logger=AsyncMock()
        )
        
        # Должен вернуться fallback результат
        assert result.commit_text == "chore: update project files"
        assert result.confidence == 0.1
        assert result.files_analyzed == 0
        assert result.has_changes is True


@pytest.mark.asyncio
async def test_git_command_error():
    """Тест обработки ошибок git команд"""
    from mcp_get_text_commit.models import GitCommandError
    
    with patch('mcp_get_text_commit.git_analyzer.GitAnalyzer') as mock_analyzer_class:
        mock_analyzer = AsyncMock()
        mock_analyzer_class.return_value = mock_analyzer
        mock_analyzer_class.is_git_repository.return_value = True
        
        # Симулируем ошибку git команды
        mock_analyzer.collect_git_data.side_effect = GitCommandError("Git command failed")
        
        result = await CommitTextGenerator.generate(
            working_directory="/test/repo",
            style="conventional",
            logger=AsyncMock()
        )
        
        # Должен вернуться fallback результат
        assert result.commit_text == "chore: misc changes"
        assert result.confidence == 0.2
        assert result.files_analyzed == 0
        assert result.has_changes is True
