"""
Простой тест импорта для проверки работоспособности
"""

try:
    from mcp_get_text_commit.server import create_server
    print("✓ Server module imported successfully")
    
    from mcp_get_text_commit.models import GetTextCommitParams, GetTextCommitResult
    print("✓ Models imported successfully")
    
    from mcp_get_text_commit.git_analyzer import GitAnalyzer  
    print("✓ GitAnalyzer imported successfully")
    
    from mcp_get_text_commit.commit_type_detector import CommitTypeDetector
    print("✓ CommitTypeDetector imported successfully")
    
    from mcp_get_text_commit.commit_generator import ConventionalCommitGenerator
    print("✓ ConventionalCommitGenerator imported successfully")
    
    from mcp_get_text_commit.commit_text_generator import CommitTextGenerator
    print("✓ CommitTextGenerator imported successfully")
    
    # Попробуем создать сервер
    server = create_server()
    print("✓ MCP Server created successfully!")
    print(f"Server name: {server.name}")
    
    print("\n🎉 ALL IMPORTS SUCCESSFUL! Project is ready to use.")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
