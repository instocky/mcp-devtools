#!/usr/bin/env python3
"""
Анализ commit message для основной директории проекта
"""

import sys
from pathlib import Path

# Добавляем src в path из подпроекта  
src_path = Path(__file__).parent / "mcp-get-text-commit" / "src"
sys.path.insert(0, str(src_path))

import asyncio
from mcp_get_text_commit.commit_text_generator import CommitTextGenerator


async def analyze_main_project():
    """Анализ основной директории проекта"""
    print("=== GET_TEXT_COMMIT для основной директории ===")
    print("Анализирую staged изменения в C:\\Projects\\MCP\\0720_mcp-devtools...")
    
    try:
        result = await CommitTextGenerator.generate(
            working_directory="C:\\Projects\\MCP\\0720_mcp-devtools",
            style="conventional"
        )
        
        print(f"\nГенерированный commit message:")
        print("=" * 60)
        print(result.commit_text)
        print("=" * 60)
        print(f"\nМетаданные:")
        print(f"  Confidence: {result.confidence:.2f}")
        print(f"  Files analyzed: {result.files_analyzed}")
        print(f"  Has changes: {result.has_changes}")
        
        if result.has_changes:
            print(f"\nГотов для использования:")
            print(f"git commit -m \"{result.commit_text.replace(chr(10), '\\n')}\"")
        else:
            print(f"\nНет staged изменений для коммита")
            
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(analyze_main_project())
