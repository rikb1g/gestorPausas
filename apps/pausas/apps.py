from django.apps import AppConfig


class PausasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pausas'

    def ready(self) -> None:
        import apps.pausas.signals
