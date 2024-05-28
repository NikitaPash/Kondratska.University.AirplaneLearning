from django.apps import AppConfig


class ResourceLibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resource_library'

    def ready(self):
        pass
