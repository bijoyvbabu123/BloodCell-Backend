from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

        # for using signals
    def ready(self):
        import users.signals
        import telegrambot.signals
