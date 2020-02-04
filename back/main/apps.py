from django.apps import AppConfig


class MainConfig(AppConfig):
    """
    Django app config for main.
    """
    name = 'main'

    def ready(self):

        # connect signals
        import main.signals
