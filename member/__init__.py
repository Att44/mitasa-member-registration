from django.apps import AppConfig

class memberConfig(AppConfig):
    name = 'member'

    def ready(self):
        import member.signals