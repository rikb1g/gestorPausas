from __future__ import absolute_import, unicode_literals

# Importar o módulo Celery
from .celery import app as celery_app

# Tornar o Celery disponível para outras partes do Django
__all__ = ('celery_app',)
