# Правила разработки

## Вид коммита

Для единообразия и качества истории разработки создавайте текст коммитов по следующему образцу:

### Формат коммита:

```
<type>: <краткое описание на английском>

- <детальное описание изменения 1>
- <детальное описание изменения 2>
- <детальное описание изменения 3>

<контекст/обоснование изменений>
```

### Пример правильного коммита:

```
feat: separate AmoCRM and Tilda data into dedicated tables

- Create new TildaLead model with full lifecycle management
- Add migration to create tilda_leads table with proper indexing
- Remove Tilda fields from amocrm_contacts table via migration
- Implement status machine for Tilda lead processing (pending/processing/synced/failed)

This refactoring separates concerns between AmoCRM contacts and Tilda leads, enabling independent tracking of lead sources and improving data integrity for the upcoming Tilda API polling service.
```

### Типы коммитов (type):

- **feat**: новая функциональность
- **fix**: исправление багов
- **docs**: изменения в документации
- **style**: форматирование, отсутствие изменений в коде
- **refactor**: рефакторинг кода без изменения функциональности
- **test**: добавление или изменение тестов
- **chore**: обновление сборки, вспомогательных инструментов

### Принципы хорошего коммита:

1. **Краткое описание** (до 50 символов) - что было сделано
2. **Детальное описание** - список конкретных изменений с маркерами
3. **Контекст** - почему это было сделано, какую проблему решает
4. **Атомарность** - один коммит = одна логическая единица изменений
5. **Читаемость** - коммит должен быть понятен через месяц/год
6. **Только текст коммита** - при запросе коммита давать только готовый текст без дополнительных пояснений

### Плохие примеры:

❌ `fix bugs`  
❌ `update code`  
❌ `работает`  
❌ `фикс`

### Хорошие примеры:

✅ `feat: add PyDriller integration for repository analysis`  
✅ `fix: resolve CSS layout issues in dashboard charts`  
✅ `docs: update README with installation instructions`  
✅ `refactor: extract git analysis logic into separate module`

