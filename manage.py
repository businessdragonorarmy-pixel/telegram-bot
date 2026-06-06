#!/usr/bin/env python
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegram_bot_project.settings")

    sys.path.insert(0, str(Path(__file__).resolve().parent / "telegram_bot_project"))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
