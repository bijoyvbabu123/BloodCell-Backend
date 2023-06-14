from django.apps import AppConfig


class BloodrequesthandlingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bloodrequesthandling'

    # for using signals
    def ready(self):
        import bloodrequesthandling.signals
        import telegrambot.signals
    