#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    APP_NAME = BASE_DIR.rsplit("/", 1)[-1]
    DEV = os.environ.get("ENV")
    settings = "{}.settings".format(APP_NAME)
    if DEV == "PRO":
        settings = "{}.settings_pro".format(APP_NAME)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)


