from django.apps import AppConfig


class PersonalblogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'personalblog'


    def ready(self):
        import personalblog.signals
