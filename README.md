# MCP Get Text Commit - Git Commit Intelligence

**One-Click Git Commit Intelligence через Model Context Protocol**

Автоматический анализ git изменений и генерация готовых commit messages в соответствии с Conventional Commits стандартом.

## 🚀 Быстрый старт

### Установка

```bash
# Клонируйте репозиторий
git clone <repo-url>
cd mcp-get-text-commit

# Установите зависимости
uv sync

# Тест работоспособности
uv run python test_manual.py
```

### Интеграция с Claude Desktop

Добавьте в ваш `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "git-commit-intelligence": {
      "command": "uv",
      "args": ["run", "python", "dev_runner.py"],
      "cwd": "C:\\Projects\\MCP\\0720_mcp-devtools\\mcp-get-text-commit"
    }
  }
}
```

## 🛠️ Использование

### Через Claude Desktop

1. Откройте Claude Desktop
2. Выполните staged изменения: `git add .`
3. Спросите Claude: *"Сгенерируй commit message для моих изменений"*
4. Claude автоматически использует `get_text_commit` tool

### Прямое использование

```python
from mcp_get_text_commit import CommitTextGenerator

# Генерация commit message
result = await CommitTextGenerator.generate(
    working_directory="/path/to/repo",
    style="conventional"
)

print(f"Commit: {result.commit_text}")
print(f"Confidence: {result.confidence}")
```

## 🏗️ Архитектура

### Основные компоненты

- **FastMCP Server** (`server.py`) - Главный MCP сервер
- **Git Analyzer** (`git_analyzer.py`) - Асинхронный анализ git данных
- **Commit Type Detector** (`commit_type_detector.py`) - Pattern matching для типов
- **Commit Generator** (`commit_generator.py`) - Генерация Conventional Commits
- **Models** (`models.py`) - Pydantic модели для типобезопасности

### Поддерживаемые типы коммитов

- `feat` - Новая функциональность
- `fix` - Исправления багов
- `docs` - Изменения документации
- `refactor` - Рефакторинг кода
- `style` - Форматирование, стили
- `chore` - Обновления зависимостей, конфигураций

## 🧪 Тестирование

```bash
# Запуск unit тестов
uv run pytest tests/ -v

# Ручное тестирование
uv run python test_manual.py

# Тестирование с MCP Inspector
uv run mcp dev src/mcp_get_text_commit/server.py
```

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

## 🔧 Development

### Структура проекта

```
mcp-get-text-commit/
├── src/mcp_get_text_commit/
│   ├── server.py              # FastMCP сервер
│   ├── git_analyzer.py        # Git анализ
│   ├── commit_type_detector.py # Определение типов
│   ├── commit_generator.py    # Генерация сообщений
│   ├── commit_text_generator.py # Основной координатор
│   └── models.py              # Pydantic модели
├── tests/                     # Unit тесты
├── pyproject.toml            # Конфигурация проекта
└── dev_runner.py             # Development entry point
```

### Development workflow

```bash
# Запуск в dev режиме с live reload
uv run mcp dev src/mcp_get_text_commit/server.py

# Форматирование кода
uv run black src/ tests/
uv run isort src/ tests/

# Проверка типов
uv run mypy src/
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
4. Запустите `uv run pytest tests/`
5. Создайте Pull Request

---

**Made with ❤️ using Python MCP SDK**
