from django.apps import AppConfig

from relays import __version__


class RelaysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relays'
    label = 'relays'
    verbose_name = f'AA Relays v{__version__}'

    def ready(self):
        import relays.signals  # noqa:F401
