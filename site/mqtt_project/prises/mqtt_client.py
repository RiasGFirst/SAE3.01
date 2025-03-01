import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

# États des prises stockés en mémoire
prise_states = {
    'PRISE1': False,  # False = éteinte, True = allumée
    'PRISE2': False
}

class MQTTClient:
    def __init__(self):
        load_dotenv()
        self.client = mqtt.Client()

        # Configuration des callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Connexion au serveur MQTT
        self.client.username_pw_set(os.getenv("USERNAME"), os.getenv("PASSWORD"))
        self.client.connect(os.getenv("HOST"), 1883, 60)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connecté au serveur MQTT avec le code {rc}")
        # S'abonner au topic "test"
        self.client.subscribe("test")

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        print(f"Message reçu: {msg.topic} -> {message}")

        # Filtrer et mettre à jour l'état des prises
        if message == "PRISE1_ISON":
            prise_states['PRISE1'] = True
        elif message == "PRISE1_ISOFF":
            prise_states['PRISE1'] = False
        elif message == "PRISE2_ISON":
            prise_states['PRISE2'] = True
        elif message == "PRISE2_ISOFF":
            prise_states['PRISE2'] = False

    def publish(self, message):
        self.client.publish(os.getenv("TOPIC"), message)

    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self):
        self.client.loop_stop()
