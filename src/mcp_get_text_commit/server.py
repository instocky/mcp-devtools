"""
MCP Server для Git Commit Intelligence

Основной FastMCP сервер для анализа git изменений и генерации commit messages.
"""

from mcp.server.fastmcp import FastMCP, Context
from .models import GetTextCommitParams, GetTextCommitResult
from .commit_text_generator import CommitTextGenerator


# Создаем MCP сервер
mcp = FastMCP("Git Commit Intelligence")


@mcp.tool()
async def get_text_commit(
    params: GetTextCommitParams,
    ctx: Context
) -> GetTextCommitResult:
    """
    Анализирует git изменения и генерирует готовый commit message
    в соответствии с Conventional Commits стандартом.
    
    Args:
        params: Параметры генерации (рабочая директория, стиль)
        ctx: Контекст для логирования
        
    Returns:
        GetTextCommitResult с готовым commit message и метаданными
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
        
        if result.has_changes:
            await ctx.info("Commit message готов!")
        else:
            await ctx.warning("Нет изменений для коммита")

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


def create_server() -> FastMCP:
    """Создает и настраивает MCP сервер"""
    return mcp


def main():
    """Entry point для CLI"""
    mcp.run()


if __name__ == "__main__":
    main()
