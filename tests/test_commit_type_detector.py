"""
Unit Tests для CommitTypeDetector

Тесты логики определения типов коммитов.
"""

import pytest
from mcp_get_text_commit.commit_type_detector import CommitTypeDetector


def test_detect_feat_commit():
    """Тест определения feature коммита"""
    detector = CommitTypeDetector()
    staged_files = ["src/user_service.py"] 
    staged_diff = """
+def create_user(self, user_data):
+    '''Создает нового пользователя'''
+    return self.repository.save(user_data)
"""
    
    commit_type, confidence = detector.detect_commit_type(staged_files, staged_diff)
    assert commit_type == "feat"
    assert confidence > 0.3


def test_detect_fix_commit():
    """Тест определения fix коммита"""
    detector = CommitTypeDetector()
    staged_files = ["src/payment.py"]
    staged_diff = """
-if user.balance == None:
+if user.balance is None:
     # Fix null check for balance
"""
    
    commit_type, confidence = detector.detect_commit_type(staged_files, staged_diff)
    assert commit_type == "fix"
    assert confidence > 0.5


def test_detect_docs_only():
    """Тест определения docs коммита для документации"""
    detector = CommitTypeDetector()
    staged_files = ["README.md", "docs/installation.md"]
    staged_diff = """
+## Installation
+
+Run the following command:
+```bash
+pip install package
+```
"""
    
    commit_type, confidence = detector.detect_commit_type(staged_files, staged_diff)
    assert commit_type == "docs"
    assert confidence == 0.95


def test_detect_chore_commit():
    """Тест определения chore коммита"""
    detector = CommitTypeDetector()
    staged_files = ["pyproject.toml", "requirements.txt"]
    staged_diff = """
+pytest>=8.4.0
+black>=25.1.0
"""
    
    commit_type, confidence = detector.detect_commit_type(staged_files, staged_diff)
    assert commit_type == "chore"
    assert confidence > 0.4


def test_detect_refactor_commit():
    """Тест определения refactor коммита"""
    detector = CommitTypeDetector()
    staged_files = ["src/old_module.py", "src/new_module.py"]
    staged_diff = """
# rename old function to new one
-def old_function_name():
+def optimized_function_name():
     pass
"""
    
    commit_type, confidence = detector.detect_commit_type(staged_files, staged_diff)
    assert commit_type == "refactor"
    assert confidence > 0.3


def test_empty_files():
    """Тест обработки пустого списка файлов"""
    detector = CommitTypeDetector()
    staged_files = []
    staged_diff = ""
    
    commit_type, confidence = detector.detect_commit_type(staged_files, staged_diff)
    # Должен вернуть что-то по умолчанию
    assert commit_type in detector.COMMIT_TYPES.keys()
    assert 0.0 <= confidence <= 1.0


def test_mixed_files():
    """Тест обработки смешанных типов файлов"""
    detector = CommitTypeDetector()
    staged_files = ["src/controller.py", "README.md", "tests/test_api.py"]
    staged_diff = """
+class UserController:
+    def get_user(self):
+        pass

+# Updated documentation
+## API Changes
"""
    
    commit_type, confidence = detector.detect_commit_type(staged_files, staged_diff)
    # Должен определить наиболее подходящий тип
    assert commit_type in detector.COMMIT_TYPES.keys()
    assert confidence > 0.0