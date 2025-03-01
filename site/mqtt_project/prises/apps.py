from django.apps import AppConfig
from .mqtt_client import MQTTClient


class PrisesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prises'

    def ready(self):
        client = MQTTClient()
        client.loop_start()
