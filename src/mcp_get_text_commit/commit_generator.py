"""
Message Generation with Context

Модуль для генерации commit messages в формате Conventional Commits.
"""

import re
from pathlib import Path
from typing import List, Optional

from mcp.server.fastmcp import Context


class ConventionalCommitGenerator:
    """Генератор commit messages в формате Conventional Commits"""

    def __init__(self, project_rules: Optional[str] = None):
        self.project_rules = project_rules

    async def generate_commit_message(
        self,
        commit_type: str,
        staged_files: List[str],
        staged_diff: str,
        confidence: float,
        ctx: Context
    ) -> str:
        """Генерирует полный commit message"""
        await ctx.debug(f"Генерация commit message для типа: {commit_type}")
        
        subject = await self._generate_subject(commit_type, staged_files, staged_diff)
        body = await self._generate_body(staged_files, staged_diff) if len(staged_files) > 3 or confidence < 0.7 else None
        footer = await self._generate_footer() if self.project_rules and "TODO.md" in self.project_rules else None

        commit_parts = [subject]
        if body:
            commit_parts.extend(["", body])
        if footer:
            commit_parts.extend(["", footer])

        commit_message = "\n".join(commit_parts)
        await ctx.debug(f"Сгенерированный commit message: {commit_message[:100]}...")
        return commit_message

    async def _generate_subject(self, commit_type: str, staged_files: List[str], staged_diff: str) -> str:
        """Генерирует subject line коммита"""
        key_changes = self._extract_key_changes(staged_diff)
        
        if key_changes:
            description = key_changes[0]
        elif len(staged_files) == 1:
            filename = Path(staged_files[0]).stem
            description = f"update {filename}"
        else:
            description = f"update {len(staged_files)} files"
            
        return f"{commit_type}: {description}"

    async def _generate_body(self, staged_files: List[str], staged_diff: str) -> str:
        """Генерирует body коммита с деталями"""
        changes = self._extract_key_changes(staged_diff)
        return "\n".join(f"- {change}" for change in changes[:5])

    async def _generate_footer(self) -> str:
        """Генерирует footer на основе project rules"""
        return "This addresses the requirements from TODO.md"

    def _extract_key_changes(self, staged_diff: str) -> List[str]:
        """Извлекает ключевые изменения из git diff"""
        changes = []
        patterns = {
            r'\+.*function\s+(\w+)': lambda m: f"add {m.group(1)}() function",
            r'\+.*class\s+(\w+)': lambda m: f"create {m.group(1)} class",
            r'\+.*def\s+(\w+)': lambda m: f"implement {m.group(1)}() method",
            r'\-.*function\s+(\w+)': lambda m: f"remove {m.group(1)}() function",
            r'\+.*import\s+(\w+)': lambda m: f"add {m.group(1)} dependency",
        }
        
        for pattern, formatter in patterns.items():
            for match in re.finditer(pattern, staged_diff, re.IGNORECASE):
                change = formatter(match)
                if change not in changes:
                    changes.append(change)

        if not changes:
            added_lines = len(re.findall(r'^\+[^+]', staged_diff, re.MULTILINE))
            removed_lines = len(re.findall(r'^\-[^-]', staged_diff, re.MULTILINE))
            
            if added_lines > removed_lines * 2:
                changes.append("add new functionality")
            elif removed_lines > added_lines * 2:
                changes.append("remove unused code")
            else:
                changes.append("update implementation")

        return changes[:3]
