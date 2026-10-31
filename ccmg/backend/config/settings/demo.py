"""Configuración para revisiones y demostraciones: usa una base de datos aparte.

Uso:
    python manage.py sembrar_demo --settings=config.settings.demo
    python manage.py runserver --settings=config.settings.demo
"""
from .development import *  # noqa: F401,F403

DATABASES["default"]["NAME"] = os.getenv("DB_NAME_DEMO", "CCMG_GIRON_demo")  # noqa: F405
