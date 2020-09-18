from django.apps import AppConfig


class TeamleaderworkspaceConfig(AppConfig):
    name = 'apps.teamleaderworkspace'
    
    def ready(self):   #import our signals 
        import apps.teamleaderworkspace.signals
