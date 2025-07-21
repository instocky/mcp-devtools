"""
Git Analysis Engine

Модуль для асинхронного анализа git изменений с использованием subprocess.
"""

import asyncio
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

from .models import GitAnalysisError, GitCommandError


class GitAnalyzer:
    """Модуль анализа git изменений с использованием asyncio"""

    def __init__(self, working_directory: Optional[str] = None):
        self.working_directory = Path(working_directory) if working_directory else Path.cwd()

    @staticmethod
    async def is_git_repository(working_directory: Optional[str] = None) -> bool:
        """Проверяет, является ли директория git репозиторием"""
        work_dir = Path(working_directory) if working_directory else Path.cwd()
        
        try:
            process = await asyncio.create_subprocess_exec(
                "git", "rev-parse", "--git-dir",
                cwd=work_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await process.communicate()
            return process.returncode == 0
            
        except Exception:
            return False

    async def collect_git_data(self) -> Dict:
        """Параллельный сбор git данных для максимальной производительности"""

        tasks = [
            self._run_git_command("diff --cached --name-only"),
            self._run_git_command("diff --cached"),
            self._run_git_command("branch --show-current"),
            self._read_project_rules()
        ]

        try:
            staged_files, staged_diff, current_branch, project_rules = await asyncio.gather(*tasks)

            return {
                "staged_files": staged_files.strip().split('\n') if staged_files.strip() else [],
                "staged_diff": staged_diff,
                "current_branch": current_branch.strip(),
                "project_rules": project_rules
            }
        except Exception as e:
            raise GitAnalysisError(f"Failed to collect git data: {str(e)}")

    async def _run_git_command(self, command: str) -> str:
        """Выполнение git команды асинхронно"""
        process = await asyncio.create_subprocess_exec(
            "git", *command.split(),
            cwd=self.working_directory,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise GitCommandError(f"Git command failed: {stderr.decode()}")

        return stdout.decode()

    async def _read_project_rules(self) -> Optional[str]:
        """Чтение rules.md для контекста проекта"""
        rules_path = self.working_directory / "rules.md"
        if rules_path.exists():
            try:
                return rules_path.read_text(encoding='utf-8')
            except Exception:
                # Если не удается прочитать файл, возвращаем None
                return None
        return None
