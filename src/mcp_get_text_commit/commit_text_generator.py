"""
Core Commit Text Generator

Основной модуль для объединения всех компонентов генерации commit messages.
"""

from typing import Optional

from mcp.server.fastmcp import Context

from .commit_generator import ConventionalCommitGenerator
from .commit_type_detector import CommitTypeDetector
from .git_analyzer import GitAnalyzer
from .models import GetTextCommitResult, GitAnalysisError, GitCommandError


class CommitTextGenerator:
    """Основной класс для генерации commit messages"""

    @staticmethod
    async def generate(
        working_directory: Optional[str] = None,
        style: str = "conventional",
        logger: Optional[Context] = None
    ) -> GetTextCommitResult:
        """
        Генерирует commit message на основе git изменений
        
        Args:
            working_directory: Путь к git репозиторию
            style: Стиль commit message (только 'conventional' пока)
            logger: Context для логирования
            
        Returns:
            GetTextCommitResult с готовым commit message
        """
        ctx = logger or _DummyContext()
        
        try:
            await ctx.info("Анализ git изменений...")

            if not await GitAnalyzer.is_git_repository(working_directory):
                await ctx.error("Директория не является git репозиторием")
                raise ValueError("Not a git repository")

            analyzer = GitAnalyzer(working_directory)
            git_data = await analyzer.collect_git_data()

            if not git_data["staged_files"]:
                await ctx.warning("Нет staged изменений для коммита")
                return GetTextCommitResult(
                    commit_text="",
                    confidence=0.0,
                    files_analyzed=0,
                    has_changes=False
                )

            await ctx.info(f"Найдено файлов: {len(git_data['staged_files'])}")

            detector = CommitTypeDetector()
            commit_type, type_confidence = detector.detect_commit_type(
                git_data["staged_files"], 
                git_data["staged_diff"]
            )

            await ctx.info(f"Определен тип: {commit_type} (confidence: {type_confidence:.2f})")

            generator = ConventionalCommitGenerator(git_data["project_rules"])
            commit_text = await generator.generate_commit_message(
                commit_type=commit_type,
                staged_files=git_data["staged_files"],
                staged_diff=git_data["staged_diff"],
                confidence=type_confidence,
                ctx=ctx
            )

            await ctx.info("Commit message готов!")

            return GetTextCommitResult(
                commit_text=commit_text,
                confidence=type_confidence,
                files_analyzed=len(git_data["staged_files"]),
                has_changes=True
            )

        except GitCommandError as e:
            await ctx.error(f"Git ошибка: {str(e)}")
            return GetTextCommitResult(
                commit_text="chore: misc changes",
                confidence=0.2,
                files_analyzed=0,
                has_changes=True
            )

        except Exception as e:
            await ctx.error(f"Неожиданная ошибка: {str(e)}")
            return GetTextCommitResult(
                commit_text="chore: update project files",
                confidence=0.1,
                files_analyzed=0,
                has_changes=True
            )


class _DummyContext:
    """Dummy Context для случаев когда нет настоящего логгера"""
    
    async def info(self, message: str):
        print(f"INFO: {message}")
        
    async def warning(self, message: str):
        print(f"WARNING: {message}")
        
    async def error(self, message: str):
        print(f"ERROR: {message}")
        
    async def debug(self, message: str):
        print(f"DEBUG: {message}")
