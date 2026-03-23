from django.apps import AppConfig

class GreenshanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'greenshan'

    def ready(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='greenshan',
                email='23332@krcollege.net',
                password='1234@qwer'
            )