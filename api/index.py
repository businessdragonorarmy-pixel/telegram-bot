from __future__ import annotations

import sys
from pathlib import Path

from serverless_wsgi import handle

# Add outer telegram_bot_project dir so inner package is importable
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "telegram_bot_project"))

from telegram_bot_project.wsgi import application


def handler(request, context):
    return handle(application, request, context)
