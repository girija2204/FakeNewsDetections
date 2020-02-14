#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# import keras.backend.tensorflow_backend as tb


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsPortal.settings")
    # tb._SYMBOLIC_SCOPE.value = True
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
