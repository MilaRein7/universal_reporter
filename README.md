# Universal DevSecOps Reporter

Учебный проект: универсальный репортёр, который автоматически собирает результаты разных проверок  
(SAST, Lint, DAST, Coverage), объединяет их в единый HTML-отчёт и отправляет краткое резюме в Telegram.

Проект демонстрирует основы DevSecOps-практик:
- статический анализ безопасности (SAST);
- линтеры (Lint);
- динамический анализ (DAST);
- анализ покрытия тестов (Coverage);
- автоматическая агрегация результатов;
- уведомления через Telegram;
- интеграция в CI/CD.

---

## Структура проекта

```
universal_reporter/
│   README.md
│   requirements.txt
│   get_chat_id.py
│   devsecops_report.html
│
├── reports/
│     bandit_report.json
│     flake8_report.txt
│     zap_report.json
│     coverage_summary.json
│
├── universal_reporter/
│     __init__.py
│     main.py
│     models.py
│     html_reporter.py
│     telegram_notifier.py
│
│     ├── templates/
│     │       report_template.html
│
│     └── parsers/
│             __init__.py
│             base.py
│             bandit_parser.py
│             flake8_parser.py
│             zap_parser.py
│             coverage_parser.py
│
└── sample_code/
        bad_code.py
        style_issues.py
```

---

## Возможности

### SAST  
Анализ Python-кода с помощью **Bandit**.

### Lint  
Проверка качества кода через **Flake8**.

### DAST  
Упрощённый анализ веб-уязвимостей через отчёт **OWASP ZAP**.

### Coverage  
Обработка JSON-отчётов покрытия тестами.

### HTML-отчёт  
Генерация HTML-файла со сводкой и таблицами.

### Telegram-уведомления  
Отправка краткого отчёта в Telegram-бота.

### Универсальная архитектура  
Поддержка новых инструментов через добавление новых парсеров.

---

## Установка

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### requirements.txt

```
jinja2
requests
bandit
flake8
```

---

## Настройка Telegram

1. Создать бота через **@BotFather**  
2. Получить `BOT_TOKEN`  
3. Вставить токен в `main.py`:

```python
TELEGRAM_BOT_TOKEN = "ВАШ_ТОКЕН"
```

4. Написать боту любое сообщение  
5. Запустить команду для получения `chat_id`:

```bash
python get_chat_id.py
```

6. Вставить chat_id в `main.py`:

```python
TELEGRAM_CHAT_ID = "123456789"
```

---

## Генерация отчётов

### SAST (Bandit)

```bash
python -m bandit -r sample_code -f json -o reports/bandit_report.json
```

### Lint (Flake8)

```bash
python -m flake8 sample_code --output-file reports/flake8_report.txt
```

### DAST (OWASP ZAP — упрощённо)

Создать файл:

`reports/zap_report.json`:

```json
{
  "alerts": [
    {
      "name": "SQL Injection",
      "risk": "High",
      "url": "http://example.com/login",
      "description": "Potential SQL injection",
      "solution": "Use parameterized queries"
    }
  ]
}
```

### Coverage

Файл:

`reports/coverage_summary.json`:

```json
{
  "line_coverage": 73.5
}
```

---

## Запуск репортера

```bash
python -m universal_reporter.main
```

После запуска:
1. Собираются все отчёты из папки `reports/`
2. Определяется подходящий парсер для каждого файла
3. Формируется HTML-файл `devsecops_report.html`
4. Отправляется уведомление в Telegram
