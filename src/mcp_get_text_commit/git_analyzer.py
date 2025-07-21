"""
Git Analysis Engine (v4, production-ready)

Модуль для асинхронного анализа git изменений с использованием subprocess.
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, Optional

from .models import GitAnalysisError, GitCommandError


class GitAnalyzer:
    """Модуль анализа git изменений с использованием asyncio"""

    def __init__(self, working_directory: Optional[str] = None):
        self.working_directory = Path(working_directory) if working_directory else Path.cwd()

    @staticmethod
    async def is_git_repository(working_directory: Optional[str] = None) -> bool:
        """Проверяет, является ли директория git репозиторием."""
        work_dir = Path(working_directory) if working_directory else Path.cwd()
        
        try:
            process = await asyncio.create_subprocess_exec(
                "git", "rev-parse", "--git-dir",
                cwd=work_dir,
                stdin=asyncio.subprocess.DEVNULL, # Явно закрываем stdin
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
            # БЫЛО: self._run_git_command("diff --cached --name-only"),
            self._run_git_command("diff --name-only"),  # Убрали --cached

            # БЫЛО: self._run_git_command("diff --cached"),
            self._run_git_command("diff"),  # Убрали --cached
            
            self._run_git_command("rev-parse --abbrev-ref HEAD"),
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
        """Выполнение git команды асинхронно."""
        command_list = command.split()
        
        process = await asyncio.create_subprocess_exec(
            "git", *command_list,
            cwd=self.working_directory,
            stdin=asyncio.subprocess.DEVNULL, # Явно закрываем stdin
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error_message = stderr.decode('utf-8', errors='ignore').strip()
            raise GitCommandError(f"Git command failed: {error_message}")

        return stdout.decode('utf-8', errors='ignore').strip()

    async def _read_project_rules(self) -> Optional[str]:
        """Чтение rules.md для контекста проекта."""
        rules_path = self.working_directory / "rules.md"
        if rules_path.exists():
            try:
                return rules_path.read_text(encoding='utf-8')
            except Exception:
                return None
        return None