from django.apps import AppConfig


class MmablogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mmablog'
    
    def ready(self):
        import mmablog.signals