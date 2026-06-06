# AGENTS.md

## Project Overview

Django 5.1.15 project for a Telegram bot. Python 3.13, SQLite, webhook-based Telegram integration, Razorpay payments.

## Commands

```bash
# Run development server
python telegram_bot_project/manage.py runserver

# Run all tests
python telegram_bot_project/manage.py test

# Run a single test class or method
python telegram_bot_project/manage.py test telegram_bot_app.tests.TestClassName
python telegram_bot_project/manage.py test telegram_bot_app.tests.TestClassName.test_method

# Run a single test app / file
python telegram_bot_project/manage.py test telegram_bot_app

# Make migrations
python telegram_bot_project/manage.py makemigrations

# Apply migrations
python telegram_bot_project/manage.py migrate

# Django shell
python telegram_bot_project/manage.py shell

# Lint with ruff (installed globally)
ruff check telegram_bot_project/

# Format with ruff
ruff format telegram_bot_project/

# Type check (install mypy first)
mypy telegram_bot_project/

# Set Telegram webhook
python telegram_bot_project/manage.py set_telegram_webhook --url https://your-domain.com/telegram/webhook/

# Delete Telegram webhook
python telegram_bot_project/manage.py set_telegram_webhook --delete
```


## Commands

```bash
# Run development server
python telegram_bot_project/manage.py runserver

# Run all tests
python telegram_bot_project/manage.py test

# Run a single test class or method
python telegram_bot_project/manage.py test telegram_bot_app.tests.TestClassName
python telegram_bot_project/manage.py test telegram_bot_app.tests.TestClassName.test_method

# Run a single test app / file
python telegram_bot_project/manage.py test telegram_bot_app

# Make migrations
python telegram_bot_project/manage.py makemigrations

# Apply migrations
python telegram_bot_project/manage.py migrate

# Django shell
python telegram_bot_project/manage.py shell

# Lint with ruff (installed globally)
ruff check telegram_bot_project/

# Format with ruff
ruff format telegram_bot_project/

# Type check (install mypy first)
mypy telegram_bot_project/

# Set Telegram webhook
python telegram_bot_project/manage.py set_telegram_webhook --url https://your-domain.com/telegram/webhook/

# Delete Telegram webhook
python telegram_bot_project/manage.py set_telegram_webhook --delete

# Celery worker (when configured)
celery -A telegram_bot_project worker -l info

# Redis (assumed running on localhost:6379)
```

## Tech Stack & Available Packages

- **Framework:** Django 5.1.15, django-cors-headers, django-filter
- **Telegram:** python-telegram-bot 22.7
- **Async:** Channels 4.2.0, Daphne 4.1.2, Uvicorn 0.32.1
- **Task Queue:** Celery 5.5.3 (optional — install separately if needed)
- **REST API:** DRF 3.15.2, djangorestframework-simplejwt 5.4.0
- **Auth:** django-allauth 65.4.1
- **AI/ML:** langchain, openai, transformers, torch, chromadb
- **Other:** stripe, twilio, boto3, firebase-admin, cloudinary, elasticsearch

## Project Structure

```
telegram_bot_project/      # Django project root (contains manage.py)
├── telegram_bot_project/  # Django project package (settings, urls, wsgi, asgi)
├── telegram_bot_app/      # Main Django application
└── AGENTS.md
```

## Code Style

### Imports

- Standard library first, then Django/third-party, then local
- One import per line for stdlib, groups separated by blank line
- Use explicit relative imports (`from .models import X`) within the app
- Absolute imports for cross-app imports (`from telegram_bot_project.settings import ...`)

```python
import json
import logging
from pathlib import Path

from django.conf import settings
from django.db import models
from rest_framework import serializers

from .models import TelegramUser
```

### Formatting

- Ruff for linting and formatting (4-space indent, 88 char lines)
- Follow PEP 8 conventions
- Single blank line between top-level definitions, two before classes

### Type Annotations

- Use Python type hints everywhere (functions, methods, class attributes)
- Use `from __future__ import annotations` at top of file for PEP 604 syntax
- Prefer `|` over `Optional[]` and `Union[]` (e.g., `str | None` instead of `Optional[str]`)

```python
from __future__ import annotations

def get_user(telegram_id: int) -> User | None: ...
```

### Naming Conventions

- **Classes:** PascalCase (`TelegramBotClient`, `UserSerializer`)
- **Functions/methods:** snake_case (`send_message`, `get_user`)
- **Constants:** UPPER_SNAKE_CASE (`MAX_RETRIES`, `DEFAULT_TIMEOUT`)
- **Private:** prefix with underscore (`_internal_helper`, `_cache`)
- **Module-level dunder:** `__all__` lists all public API names
- **Django models:** singular PascalCase (`class TelegramUser(models.Model):`)
- **DRF serializers:** `<Model>Serializer`
- **DRF views:** `<Model>ViewSet` or `<Action>APIView`
- **Management commands:** snake_case directory/module names

### Error Handling

- Use specific exception types, never bare `except:`
- Log exceptions with `logger.exception()` (includes traceback)
- For Telegram bot handlers, catch `telegram.error.TelegramError`
- Use early returns to avoid deep nesting
- Raise Django HTTP exceptions (`Http404`, `PermissionDenied`) in views
- Use DRF's `ValidationError` for API validation

```python
import logging

logger = logging.getLogger(__name__)

def process_update(update: Update) -> None:
    if update.message is None:
        return
    try:
        ...
    except TelegramError:
        logger.exception("Failed to process update")
```

### Django Conventions

- **Models:** define `__str__`, `Meta` class with `ordering`, `verbose_name`
- **Views:** prefer class-based views, use DRF ViewSets for APIs
- **Signals:** define in `signals.py`, register in `apps.py` `ready()` method
- **Admin:** use `@admin.register(Model)` decorator
- **URLs:** app-specific `urls.py` included from project `urls.py`
- **Settings:** keep environment-specific settings out of repo (use env vars / `.env`)

### Async & Celery

- Use `asgiref.sync.sync_to_async` to call sync Django ORM from async contexts
- Celery tasks go in `tasks.py` within each app
- Tasks should be idempotent where possible
- Use Celery retry with `max_retries` and `countdown` for transient failures

### Logging

- Use module-level logger: `logger = logging.getLogger(__name__)`
- Structured logging via `logging` module (no print statements)
- Log levels: DEBUG for dev details, INFO for normal ops, WARNING for issues, ERROR for failures

### Testing

- Tests live in `tests.py` or `tests/` package per app
- Use Django's `TestCase` for DB-backed tests
- Use `@override_settings` for test-specific config
- Use `Client` or `APIClient` (DRF) for request tests
- Use `pytest`-style function tests with `pytest-django` if added
- Name test methods: `test_<action>_<expected_result>`
- Use `factory_boy` factories for model instances if added

### Configuration Files To Create

When adding new tooling, use these standard filenames:
- Dependencies: `pyproject.toml` (preferred) or `requirements.txt`
- Linting: `pyproject.toml` (ruff section) or `ruff.toml`
- pre-commit: `.pre-commit-config.yaml`
- Docker: `Dockerfile` + `docker-compose.yml`
- Environment: `.env` (never committed)
