from __future__ import absolute_import, unicode_literals

# Questo farà sì che app.py venga caricato quando Django avvia.
from .celery import app as celery_app

__all__ = ('celery_app',)