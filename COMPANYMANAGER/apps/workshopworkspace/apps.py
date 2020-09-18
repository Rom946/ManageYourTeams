from django.apps import AppConfig


class WorkshopworkspaceConfig(AppConfig):
    name = 'apps.workshopworkspace'
    
    def ready(self):   #import our signals 
        import apps.teamleaderworkspace.signals
        import apps.workshopworkspace.signals