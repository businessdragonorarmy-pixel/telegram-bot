import sys
from pathlib import Path

from serverless_wsgi import handle

# Add project root so telegram_bot_project package is importable
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from telegram_bot_project.wsgi import application


def handler(request, context):
    return handle(application, request, context)
