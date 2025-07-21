Конечно, вы правы. Вот полный и готовый к использованию файл `README.md`. Вы можете просто скопировать и вставить весь этот текст в ваш файл, полностью заменив его старое содержимое.

---

# MCP Get Text Commit - Git Commit Intelligence

**One-Click Git Commit Intelligence через Model Context Protocol**

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Tests Passing](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#-разработка-и-тестирование)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Автоматический анализ git-изменений и генерация готовых сообщений для коммитов в соответствии со стандартом Conventional Commits.

## ⚙️ Установка и Настройка

Проект теперь является полноценным Python-пакетом. Для разработки рекомендуется следующий порядок установки:

1.  **Клонируйте репозиторий:**

    ```bash
    git clone <repo-url>
    cd mcp-get-text-commit
    ```

2.  **Создайте и активируйте виртуальное окружение:**

    ```bash
    # Создаем venv
    python -m venv venv

    # Активация в PowerShell (Windows)
    .\venv\Scripts\Activate.ps1

    # Активация в Bash (Linux/macOS)
    # source venv/bin/activate
    ```

3.  **Установите пакет в режиме разработки:**
    Эта команда установит пакет и все зависимости, необходимые для разработки и тестирования (`pytest`, `black` и т.д.).

    ```bash
    pip install -e .[dev]
    ```

4.  **Проверьте установку:**
    Запустите тесты, чтобы убедиться, что все работает корректно.
    ```bash
    pytest
    ```

## 🚀 Использование

Вы можете использовать инструмент тремя способами: через CLI, как библиотеку или интегрировав с Claude Desktop.

### 1. Интерфейс командной строки (CLI)

Самый простой способ получить сообщение для коммита — использовать скрипт `scripts/cli.py`.

```bash
# Сгенерировать сообщение для текущей директории
python scripts/cli.py

# Сгенерировать сообщение для другого репозитория
python scripts/cli.py /path/to/another/repo
```

### 2. Как библиотеку в вашем коде

Вы можете импортировать `CommitTextGenerator` в любой другой Python-проект.

````python
import asyncio
from mcp_get_text_commit.commit_text_generator import CommitTextGenerator

async def main():
    result = await CommitTextGenerator.generate(
        working_directory="/path/to/repo",
        style="conventional"
    )
    print(f"Commit: {result.commit_text}")
    print(f"Confidence: {result.confidence}")

if __name__ == "__main__":
    asyncio.run(main())```
Больше примеров смотрите в директории `examples/`.

### 3. Интеграция с Claude Desktop

Обновите ваш `claude_desktop_config.json`, указав путь к новому dev-серверу:

```json
{
  "mcpServers": {
    "git-commit-intelligence": {
      "command": "python",
      "args": ["scripts/dev_server.py"],
      "cwd": "C:\\path\\to\\your\\mcp-get-text-commit"
    }
  }
}
````

## 🏗️ Структура проекта

Структура репозитория была реорганизована для соответствия лучшим практикам Python-проектов.

```
mcp-get-text-commit/
├── src/
│   └── mcp_get_text_commit/  # Основной исходный код
├── tests/                    # Все тесты
│   ├── unit/                 # Модульные тесты (изолированные компоненты)
│   └── integration/          # Интеграционные тесты (взаимодействие компонентов)
├── examples/                 # Примеры использования библиотеки
├── scripts/                  # Исполняемые скрипты (CLI, dev-сервер)
├── docs/                     # Документация
├── pyproject.toml            # Конфигурация проекта и зависимостей
└── README.md
```

## 🛠️ Разработка и Тестирование

1.  **Установка:** Следуйте инструкциям в разделе [Установка и Настройка](#️-установка-и-настройка).
2.  **Запуск тестов:**
    ```bash
    pytest
    ```
3.  **Форматирование кода:**
    ```bash
    black .
    isort .
    ```
4.  **Проверка типов:**
    ````bash
    mypy src/
    ```5.  **Запуск dev-сервера:**
    ```bash
    python scripts/dev_server.py
    ````

## 📋 Примеры commit messages

### Feature коммит

```
feat: implement user authentication

- implement login() method
- add password validation
- create JWT token generation
```

### Fix коммит

```
fix: resolve null pointer exception in payment processing
```

### Docs коммит

```
docs: update API documentation

- add authentication endpoints
- update installation guide
```

## 🎯 Performance

- **Cold Start**: < 500ms
- **Warm Execution**: < 200ms
- **Large Repositories** (< 1000 файлов): < 3s
- **Memory Usage**: < 50MB

## 📝 Технические детали

### Алгоритм определения типа коммита

1. **Pattern Matching** - Анализ git diff на предмет ключевых паттернов
2. **File Analysis** - Типы файлов и их расширения
3. **Keyword Detection** - Ключевые слова в изменениях
4. **Priority Scoring** - Weighted scoring для определения лучшего типа

### Graceful Error Handling

- Fallback к `chore: misc changes` при ошибках
- Логирование через MCP Context API
- Проверка git репозитория перед анализом

## 🐛 Troubleshooting

### Частые проблемы

**"Not a git repository"**

- Убедитесь что работаете в git репозитории
- Проверьте правильность пути в `working_directory`

**"Нет staged изменений"**

- Выполните `git add .` перед генерацией commit message
- Проверьте статус: `git status`

**Низкая уверенность (confidence < 0.5)**

- Добавьте более специфичные изменения
- Проверьте качество git diff

## 📄 License

MIT License - см. LICENSE файл для деталей.

## 🤝 Contributing

1. Fork репозиторий
2. Создайте feature branch
3. Добавьте тесты для новой функциональности
4. Запустите `pytest`
5. Создайте Pull Request

---

**Made with ❤️ using Python MCP SDK**
