from django.apps import AppConfig
from django.core.management import call_command

class NeuroreconuiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NeuroReconUI'

    def ready(self):
         from .Schduler import start_monitoring
         start_monitoring()  # Start the monitoring when the app is ready