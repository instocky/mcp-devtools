"""
Commit Type Detection with Pattern Matching

Модуль для определения типа коммита на основе анализа изменений файлов и diff.
"""

import re
from dataclasses import dataclass
from typing import List, Pattern, Tuple


@dataclass
class CommitTypePattern:
    """Паттерн для определения типа коммита"""
    patterns: List[Pattern]
    file_patterns: List[Pattern]
    keywords: List[str]
    priority: int = 1


class CommitTypeDetector:
    """Детектор типа коммита с использованием pattern matching"""

    COMMIT_TYPES = {
        "feat": CommitTypePattern(
            patterns=[
                re.compile(r'class\s+\w+.*{', re.IGNORECASE),
                re.compile(r'function\s+\w+.*{', re.IGNORECASE),
                re.compile(r'def\s+\w+.*:', re.IGNORECASE),
                re.compile(r'new.*Controller', re.IGNORECASE)
            ],
            file_patterns=[
                re.compile(r'Controller\.php$'),
                re.compile(r'Model\.php$'),
                re.compile(r'Service\.py$')
            ],
            keywords=['add', 'create', 'implement', 'introduce'],
            priority=3
        ),
        "fix": CommitTypePattern(
            patterns=[
                re.compile(r'fix|bug|error|correct', re.IGNORECASE),
                re.compile(r'null\s+check', re.IGNORECASE),
                re.compile(r'exception.*handling', re.IGNORECASE)
            ],
            file_patterns=[],
            keywords=['fix', 'resolve', 'correct', 'repair', 'patch'],
            priority=4
        ),
        "docs": CommitTypePattern(
            patterns=[],
            file_patterns=[
                re.compile(r'\.md$'),
                re.compile(r'README'),
                re.compile(r'TODO'),
                re.compile(r'CHANGELOG')
            ],
            keywords=['docs', 'documentation', 'readme'],
            priority=5
        ),
        "refactor": CommitTypePattern(
            patterns=[re.compile(r'rename|move|extract|optimize', re.IGNORECASE)],
            file_patterns=[],
            keywords=['refactor', 'restructure', 'reorganize', 'optimize'],
            priority=2
        ),
        "style": CommitTypePattern(
            patterns=[re.compile(r'formatting|whitespace|PSR-12', re.IGNORECASE)],
            file_patterns=[],
            keywords=['style', 'format', 'whitespace'],
            priority=1
        ),
        "chore": CommitTypePattern(
            patterns=[],
            file_patterns=[
                re.compile(r'composer\.json$'),
                re.compile(r'package\.json$'),
                re.compile(r'pyproject\.toml$'),
                re.compile(r'requirements\.txt$'),
                re.compile(r'\.env'),
                re.compile(r'config/')
            ],
            keywords=['chore', 'update', 'maintain'],
            priority=0
        )
    }

    def detect_commit_type(self, staged_files: List[str], staged_diff: str) -> Tuple[str, float]:
        """Определяет тип коммита на основе файлов и diff"""
        scores = {
            commit_type: self._calculate_type_score(commit_type, pattern, staged_files, staged_diff)
            for commit_type, pattern in self.COMMIT_TYPES.items()
        }
        
        if self._is_docs_only(staged_files):
            return "docs", 0.95
            
        best_type = max(scores.items(), key=lambda x: x[1])
        return best_type[0], min(best_type[1], 0.95)

    def _calculate_type_score(
        self, 
        commit_type: str, 
        pattern: CommitTypePattern, 
        staged_files: List[str], 
        staged_diff: str
    ) -> float:
        """Вычисляет score для конкретного типа коммита"""
        score = sum(0.3 for regex in pattern.patterns if regex.search(staged_diff))
        
        score += sum(
            0.4 for file_path in staged_files 
            for file_regex in pattern.file_patterns 
            if file_regex.search(file_path)
        )
        
        diff_lower = staged_diff.lower()
        score += sum(0.2 for keyword in pattern.keywords if keyword in diff_lower)
        
        score += pattern.priority * 0.1
        return min(score, 1.0)

    def _is_docs_only(self, staged_files: List[str]) -> bool:
        """Проверяет, что изменения только в документации"""
        if not staged_files:
            return False
            
        doc_pattern = re.compile(r'\.(md|txt|rst)$|README|TODO|CHANGELOG', re.IGNORECASE)
        return all(doc_pattern.search(file_path) for file_path in staged_files)
