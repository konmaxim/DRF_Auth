from django.apps import AppConfig
from django.db.models.signals import post_migrate

class DRFAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DRFAuth'

    def ready(self):
        from .populate_db import populate_db
        from django.contrib.auth import get_user_model

        def run_population(sender, **kwargs):
            User = get_user_model()
            if not User.objects.exists():
                populate_db()

        post_migrate.connect(run_population, sender=self)