from django.apps import AppConfig
from importlib import import_module

class ReportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reports'
    
    def ready(self):
        import_module('reports.signals')
