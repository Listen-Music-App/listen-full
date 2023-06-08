#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
from django.core.management.commands.runserver import Command as runserver
import os
import sys


def main():
    """Run administrative tasks."""
    runserver.default_addr = os.environ.get('HOST', '127.0.0.1')
    runserver.default_port = os.environ.get('PORT', '5000')

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
