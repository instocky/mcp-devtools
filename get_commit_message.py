#!/usr/bin/env python3
"""
Прямое тестирование get_text_commit для текущих изменений
"""

import sys
from pathlib import Path

# Добавляем src в path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

import asyncio
from mcp_get_text_commit.commit_text_generator import CommitTextGenerator


async def main():
    """Генерация commit message для текущих staged изменений"""
    print("=== GET_TEXT_COMMIT ===")
    print("Анализирую staged изменения...")
    
    try:
        result = await CommitTextGenerator.generate(
            working_directory=str(Path(__file__).parent),
            style="conventional"
        )
        
        print(f"\nГенерированный commit message:")
        print("=" * 50)
        print(result.commit_text)
        print("=" * 50)
        print(f"\nМетаданные:")
        print(f"  Confidence: {result.confidence:.2f}")
        print(f"  Files analyzed: {result.files_analyzed}")
        print(f"  Has changes: {result.has_changes}")
        
        if result.has_changes:
            print(f"\nГотов для копирования в git commit!")
        else:
            print(f"\nНет staged изменений для коммита")
            
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
