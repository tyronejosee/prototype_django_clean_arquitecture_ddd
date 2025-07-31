#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "src"))


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        message = "Can't import Django. Check PYTHONPATH or venv."
        raise ImportError(message) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
