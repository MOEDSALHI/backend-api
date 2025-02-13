from django.apps import AppConfig


class BarConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bar"

    def ready(self):
        # Import signals to ensure they are registered
        import bar.signals
