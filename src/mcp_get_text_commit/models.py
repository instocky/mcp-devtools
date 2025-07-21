"""
Модели данных для MCP Get Text Commit

Определяет Pydantic модели для входных параметров и результатов генерации commit messages.
"""

from typing import Optional
from pydantic import BaseModel, Field


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
    
    commit_text: str = Field(
        description="Готовый к использованию commit message"
    )
    confidence: float = Field(
        ge=0.0, le=1.0,
        description="Уверенность алгоритма в качестве предложения"
    )
    files_analyzed: int = Field(
        ge=0,
        description="Количество проанализированных файлов"
    )
    has_changes: bool = Field(
        description="Есть ли staged изменения"
    )


class GitAnalysisError(Exception):
    """Исключение при анализе git данных"""
    pass


class GitCommandError(Exception):
    """Исключение при выполнении git команд"""
    pass
