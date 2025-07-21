# PRD: get_text_commit - One-Click Git Commit Intelligence (Python MCP SDK)

## 📋 Executive Summary

**Продукт:** MCP сервер `get_text_commit` на базе Python MCP SDK  
**Версия:** v0.3.0  
**Философия:** One Tool, One Job - максимальная простота и производительность через FastMCP  
**Приоритет:** Критический

Единственный MCP инструмент на базе **FastMCP**, который анализирует git изменения и возвращает готовый текст commit message в соответствии с Conventional Commits стандартом проекта.

## 🎯 Цели и Решение

Инструмент `get_text_commit` решает проблему ручного и трудоемкого создания commit-сообщений. Он автоматизирует этот процесс, предоставляя разработчикам качественные, стандартизированные сообщения для коммитов одним действием.

**Решение на базе Python MCP SDK:**

- **Использование FastMCP:** Декларативный подход для быстрой разработки.
- **Официальный Python MCP SDK:** **Продукт полностью разработан на официальном фреймворке [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk), что обеспечивает полную совместимость, доступ к последним обновлениям протокола и всей экосистеме MCP.**
- **Автоматическая генерация схем и валидация:** Pydantic-модели для строгой типизации и надежности API.
- **Встроенные dev tools:** Инструменты `mcp dev` и `mcp install` для ускорения разработки и интеграции.
- **Простая интеграция с Claude Desktop:** Установка и использование в один клик.

## 🏗️ Архитектура на базе Python MCP SDK

### Core FastMCP Server

```python
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field
from typing import Optional

# Создаем MCP сервер
mcp = FastMCP("Git Commit Intelligence")

class GetTextCommitParams(BaseModel):
    """Параметры для генерации commit message"""
    working_directory: Optional[str] = Field(
        default=None,
        description="Путь к git репозиторию (по умолчанию: текущая директория)"
    )
    style: Optional[str] = Field(
        default="conventional",
        description="Стиль commit message (пока только 'conventional')"
    )

class GetTextCommitResult(BaseModel):
    """Результат генерации commit message"""
    commit_text: str = Field(description="Готовый к использованию commit message")
    confidence: float = Field(
        ge=0.0, le=1.0,
        description="Уверенность алгоритма в качестве предложения"
    )
    files_analyzed: int = Field(
        ge=0,
        description="Количество проанализированных файлов"
    )
    has_changes: bool = Field(description="Есть ли staged изменения")

@mcp.tool()
async def get_text_commit(
    params: GetTextCommitParams,
    ctx: Context
) -> GetTextCommitResult:
    """
    Анализирует git изменения и генерирует готовый commit message
    в соответствии с Conventional Commits стандартом.
    """
    await ctx.info("Начинаю анализ git изменений...")

    try:
        # Основная логика генерации
        result = await CommitTextGenerator.generate(
            working_directory=params.working_directory,
            style=params.style,
            logger=ctx
        )

        await ctx.info(f"Проанализировано файлов: {result.files_analyzed}")

        return result

    except Exception as e:
        await ctx.error(f"Ошибка генерации commit message: {str(e)}")
        # Graceful fallback
        return GetTextCommitResult(
            commit_text="chore: misc changes",
            confidence=0.2,
            files_analyzed=0,
            has_changes=True
        )
```

### Git Analysis Engine

```python
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class GitAnalyzer:
    """Модуль анализа git изменений с использованием asyncio"""

    def __init__(self, working_directory: Optional[str] = None):
        self.working_directory = Path(working_directory) if working_directory else Path.cwd()

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
            return rules_path.read_text(encoding='utf-8')
        return None
```

### Commit Type Detection with Pattern Matching

```python
from dataclasses import dataclass
from typing import List, Pattern
import re

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
            patterns=[re.compile(r'class\s+\w+.*{', re.IGNORECASE), re.compile(r'function\s+\w+.*{', re.IGNORECASE), re.compile(r'def\s+\w+.*:', re.IGNORECASE), re.compile(r'new.*Controller', re.IGNORECASE)],
            file_patterns=[re.compile(r'Controller\.php$'), re.compile(r'Model\.php$'), re.compile(r'Service\.py$')],
            keywords=['add', 'create', 'implement', 'introduce'],
            priority=3
        ),
        "fix": CommitTypePattern(
            patterns=[re.compile(r'fix|bug|error|correct', re.IGNORECASE), re.compile(r'null\s+check', re.IGNORECASE), re.compile(r'exception.*handling', re.IGNORECASE)],
            file_patterns=[],
            keywords=['fix', 'resolve', 'correct', 'repair', 'patch'],
            priority=4
        ),
        "docs": CommitTypePattern(
            patterns=[],
            file_patterns=[re.compile(r'\.md$'), re.compile(r'README'), re.compile(r'TODO'), re.compile(r'CHANGELOG')],
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
            file_patterns=[re.compile(r'composer\.json$'), re.compile(r'package\.json$'), re.compile(r'pyproject\.toml$'), re.compile(r'requirements\.txt$'), re.compile(r'\.env'), re.compile(r'config/')],
            keywords=['chore', 'update', 'maintain'],
            priority=0
        )
    }

    def detect_commit_type(self, staged_files: List[str], staged_diff: str) -> Tuple[str, float]:
        """Определяет тип коммита на основе файлов и diff"""
        scores = {commit_type: self._calculate_type_score(commit_type, pattern, staged_files, staged_diff) for commit_type, pattern in self.COMMIT_TYPES.items()}
        if self._is_docs_only(staged_files):
            return "docs", 0.95
        best_type = max(scores.items(), key=lambda x: x[1])
        return best_type[0], min(best_type[1], 0.95)

    def _calculate_type_score(self, commit_type: str, pattern: CommitTypePattern, staged_files: List[str], staged_diff: str) -> float:
        """Вычисляет score для конкретного типа коммита"""
        score = sum(0.3 for regex in pattern.patterns if regex.search(staged_diff))
        score += sum(0.4 for file_path in staged_files for file_regex in pattern.file_patterns if file_regex.search(file_path))
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
```

### Message Generation with Context

```python
from mcp.server.fastmcp import Context

class ConventionalCommitGenerator:
    """Генератор commit messages в формате Conventional Commits"""

    def __init__(self, project_rules: Optional[str] = None):
        self.project_rules = project_rules

    async def generate_commit_message(self, commit_type: str, staged_files: List[str], staged_diff: str, confidence: float, ctx: Context) -> str:
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
```

## 🚀 Deployment и Development

### Development Workflow с MCP SDK

```bash
# Инициализация проекта
uv init mcp-get-text-commit
cd mcp-get-text-commit

# Установка зависимостей
uv add "mcp[cli]"
uv add --dev pytest pytest-asyncio mypy black isort

# Development сервер с live reload
uv run mcp dev src/mcp_get_text_commit/server.py

# Тестирование в MCP Inspector
mcp dev src/mcp_get_text_commit/server.py --with-editable .

# Установка в Claude Desktop
mcp install src/mcp_get_text_commit/server.py --name "Git Commit Intelligence"
```

### Server Entry Point

```python
# src/mcp_get_text_commit/server.py
import asyncio
from mcp.server.fastmcp import FastMCP
from .commit_text_generator import setup_commit_tools

def create_server() -> FastMCP:
    """Создает и настраивает MCP сервер"""

    mcp = FastMCP(
        name="Git Commit Intelligence",
        dependencies=["gitpython>=3.1.0"]
    )

    setup_commit_tools(mcp)
    return mcp

def main():
    """Entry point для CLI"""
    mcp = create_server()
    mcp.run()

if __name__ == "__main__":
    main()
```

### Error Handling с Context API

```python
@mcp.tool()
async def get_text_commit(
    params: GetTextCommitParams,
    ctx: Context
) -> GetTextCommitResult:
    """Основной инструмент с расширенным error handling"""

    try:
        await ctx.info("🔍 Анализ git изменений...")

        if not await GitAnalyzer.is_git_repository(params.working_directory):
            await ctx.error("❌ Директория не является git репозиторием")
            raise ValueError("Not a git repository")

        analyzer = GitAnalyzer(params.working_directory)
        git_data = await analyzer.collect_git_data()

        if not git_data["staged_files"]:
            await ctx.warning("⚠️ Нет staged изменений для коммита")
            return GetTextCommitResult(commit_text="", confidence=0.0, files_analyzed=0, has_changes=False)

        await ctx.info(f"📁 Найдено файлов: {len(git_data['staged_files'])}")

        detector = CommitTypeDetector()
        commit_type, type_confidence = detector.detect_commit_type(git_data["staged_files"], git_data["staged_diff"])

        await ctx.info(f"🏷️ Определен тип: {commit_type} (confidence: {type_confidence:.2f})")

        generator = ConventionalCommitGenerator(git_data["project_rules"])
        commit_text = await generator.generate_commit_message(
            commit_type=commit_type,
            staged_files=git_data["staged_files"],
            staged_diff=git_data["staged_diff"],
            confidence=type_confidence,
            ctx=ctx
        )

        await ctx.info("✅ Commit message готов!")

        return GetTextCommitResult(
            commit_text=commit_text,
            confidence=type_confidence,
            files_analyzed=len(git_data["staged_files"]),
            has_changes=True
        )

    except GitCommandError as e:
        await ctx.error(f"Git ошибка: {str(e)}")
        return GetTextCommitResult(commit_text="chore: misc changes", confidence=0.2, files_analyzed=0, has_changes=True)

    except Exception as e:
        await ctx.error(f"Неожиданная ошибка: {str(e)}")
        return GetTextCommitResult(commit_text="chore: update project files", confidence=0.1, files_analyzed=0, has_changes=True)
```

## 🧪 Testing Strategy

### Unit Tests with pytest-asyncio

```python
# tests/test_commit_generator.py
import pytest
from unittest.mock import AsyncMock, patch
from mcp_get_text_commit.commit_text_generator import CommitTextGenerator
from mcp_get_text_commit.server import GetTextCommitParams

@pytest.mark.asyncio
async def test_generate_feat_commit():
    """Тест генерации feature коммита"""
    params = GetTextCommitParams(working_directory="/test/repo")
    with patch('mcp_get_text_commit.git_analyzer.GitAnalyzer') as mock_analyzer:
        mock_analyzer.return_value.collect_git_data.return_value = {
            "staged_files": ["src/user_controller.py"],
            "staged_diff": "+def register_user(self):\n+    pass",
            "current_branch": "feature/user-registration",
            "project_rules": None
        }
        result = await CommitTextGenerator.generate(working_directory="/test/repo", style="conventional", logger=AsyncMock())
        assert result.commit_text.startswith("feat:")
        assert result.confidence > 0.8
        assert result.files_analyzed == 1
        assert result.has_changes is True

@pytest.mark.asyncio
async def test_no_staged_changes():
    """Тест случая без staged изменений"""
    params = GetTextCommitParams()
    with patch('mcp_get_text_commit.git_analyzer.GitAnalyzer') as mock_analyzer:
        mock_analyzer.return_value.collect_git_data.return_value = {
            "staged_files": [], "staged_diff": "", "current_branch": "main", "project_rules": None
        }
        result = await CommitTextGenerator.generate(working_directory=None, style="conventional", logger=AsyncMock())
        assert result.commit_text == ""
        assert result.confidence == 0.0
        assert result.files_analyzed == 0
        assert result.has_changes is False
```

### Integration Tests

```python
# tests/test_integration.py
import pytest
import tempfile
import subprocess
from pathlib import Path
from mcp_get_text_commit.server import create_server

@pytest.mark.asyncio
async def test_real_git_repository():
    """Интеграционный тест с реальным git репозиторием"""
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir)
        subprocess.run(["git", "init"], cwd=repo_path, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_path)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path)
        test_file = repo_path / "test.py"
        test_file.write_text("def hello():\n    print('Hello, world!')")
        subprocess.run(["git", "add", "test.py"], cwd=repo_path, check=True)

        mcp = create_server()
        # Симуляция вызова инструмента (требует MCP client)
```

## 📊 Performance Benchmarks

### Async Performance Targets

- **Cold Start**: < 500ms
- **Warm Execution**: < 200ms
- **Large Repositories** (< 1000 файлов): < 3s
- **Memory Usage**: < 50MB

### Optimization Strategies

```python
# Кэширование результатов анализа
from functools import lru_cache
from typing import Dict, Any

class OptimizedGitAnalyzer(GitAnalyzer):
    """Оптимизированная версия с кэшированием"""

    @lru_cache(maxsize=100)
    def _cached_file_analysis(self, file_content_hash: str) -> Dict[str, Any]:
        """Кэшированный анализ файлов по хэшу контента"""
        pass

    async def collect_git_data_optimized(self) -> Dict:
        """Оптимизированный сбор данных с параллельным выполнением"""
        diff_cmd = "diff --cached --stat"
        stat_result = await self._run_git_command(diff_cmd)
        if "files changed" in stat_result:
            changed_files = int(stat_result.split()[0])
            if changed_files > 50:
                return await self._collect_lightweight_data()
        return await self.collect_git_data()
```

## 🔧 Configuration и Extensibility

### Settings через Environment Variables

```python
import os
from pydantic import BaseSettings

class MCPCommitSettings(BaseSettings):
    """Настройки MCP сервера"""
    max_files_analysis: int = 100
    diff_size_limit: int = 10000
    confidence_threshold: float = 0.5
    enable_project_rules: bool = True
    debug_mode: bool = False

    class Config:
        env_prefix = "MCP_COMMIT_"
        env_file = ".env"

# Использование в сервере
settings = MCPCommitSettings()
if settings.debug_mode:
    await ctx.debug("Debug mode включен")
```

## 🎯 Success Metrics

### Technical KPIs

- ✅ **Простота API:** 1 FastMCP tool для единой точки входа.
- ✅ **Производительность:** ~50% быстрее выполнение через async/await.
- ✅ **Типобезопасность:** 100% валидация через Pydantic.
- ✅ **Скорость разработки:** ~70% сокращение времени разработки благодаря MCP SDK.
- ✅ **Надежность:** Graceful handling ошибок через Context API.

### Quality Metrics

- ✅ **Высокий Confidence Rate:** >80% случаев с confidence > 0.8.
- ✅ **Соответствие Conventional Commits:** 100% соответствие формату.
- ✅ **Качество интеграции:** Бесшовная интеграция с Claude Desktop.
- ✅ **Developer Experience:** `mcp dev` с hot reload для быстрой итерации.

## 💡 Advanced Features Roadmap

### v0.4.0 - Enhanced Intelligence (1-2 недели)

- 🔄 **Семантический анализ:** Анализ бизнес-логики через AST-парсинг.
- 🔄 **Поддержка нескольких языков:** Специфика для Python/JS/PHP/Go.
- 🔄 **Интеграция с контекстом проекта:** TODO.md, CHANGELOG.md.
- 🔄 **Кастомизация шаблонов:** Поддержка пользовательских шаблонов коммитов.

### v0.5.0 - Team Intelligence (2-3 недели)

- 🔄 **Обучение на данных команды:** Адаптация к паттернам коммитов команды.
- 🔄 **Пакетная обработка:** Анализ нескольких веток/PR.
- 🔄 **Интеграционные хуки:** Webhook для CI/CD.

### v1.0.0 - Production Ready (1 месяц)

- 🔄 **Enterprise-функции:** Поддержка нескольких репозиториев, дашборды.
- 🔄 **Оптимизация производительности:** Инкрементальный анализ.
- 🔄 **Мониторинг и аналитика:** Метрики качества коммитов.

## 🎉 Conclusion

Данный PRD описывает комплексную стратегию разработки инструмента **Git Commit Intelligence** с использованием **Python MCP SDK**.

### ✅ Ключевые преимущества

1.  **Простота API** с FastMCP.
2.  **Автоматическая типизация** с Pydantic.
3.  **Встроенные dev tools** (`mcp dev`, `mcp install`).
4.  **Высокая производительность** за счет async/await.
5.  **Профессиональная обработка ошибок** через Context API.
6.  **Бесшовная интеграция с Claude** через официальный протокол.

### 🚀 Готовность к реализации

- **Детальная архитектура** с примерами кода.
- **Комплексная стратегия тестирования**.
- **План развертывания** с мониторингом.
- **Целевые метрики** производительности.

**Статус документа:** ✅ **Ready for Implementation**  
**Приоритет:** **Critical**  
**Timeline:** **1-2 недели** для базовой реализации.
