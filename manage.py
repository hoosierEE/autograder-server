#!/usr/bin/env python3
import os
import sys


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autograder.settings.development")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autograder.settings.production")

    os.environ.setdefault("DJANGO_TEST_PROCESSES", '1')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
