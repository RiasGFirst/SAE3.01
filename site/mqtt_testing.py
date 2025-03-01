import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os


load_dotenv()
"""
Connect to the brocker and listen for messages on test topic.
When a message is recieved, check if it is:
    - ID_ON # je m'allume
    - ID_OFF # je m'éteint
    - ID_TOGGLE # je change mon état
    - ID_STATE # j'envoie mon état
    
ID is PRISE1 or PRISE1

And then publish the new state on the same topic.
    ID_ISON # je suis allumé
    ID_ISOFF # je suis éteint
"""

# Define the callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("test")

def on_message(client, userdata, msg):
    global PRISE1, PRISE2
    print(msg.topic+" "+str(msg.payload))
    match msg.payload:

        case b'PRISE1_ON':
            client.publish(msg.topic, "PRISE1_ISON")
        case b'PRISE1_OFF':
            client.publish(msg.topic, "PRISE1_ISOFF")
        case b'PRISE1_TOGGLE':
            if PRISE1:
                client.publish(msg.topic, "PRISE1_ISOFF")
            else:
                client.publish(msg.topic, "PRISE1_ISON")
        case b'PRISE1_STATE':
            if PRISE1:
                client.publish(msg.topic, "PRISE1_ISON")
            else:
                client.publish(msg.topic, "PRISE1_ISOFF")
        case b'PRISE2_ON':
            client.publish(msg.topic, "PRISE2_ISON")
        case b'PRISE2_OFF':
            client.publish(msg.topic, "PRISE2_ISOFF")
        case b'PRISE2_TOGGLE':
            if PRISE2:
                client.publish(msg.topic, "PRISE2_ISOFF")
            else:
                client.publish(msg.topic, "PRISE2_ISON")
        case b'PRISE2_STATE':
            if PRISE2:
                client.publish(msg.topic, "PRISE2_ISON")
            else:
                client.publish(msg.topic, "PRISE2_ISOFF")
        case b'PRISE1_ISON':
            PRISE1 = True
        case b'PRISE1_ISOFF':
            PRISE1 = False
        case b'PRISE2_ISON':
            PRISE2 = True
        case b'PRISE2_ISOFF':
            PRISE2 = False
        case _:
            pass

# Create the client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the brocker
broker_address = os.getenv("HOST")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
topic = os.getenv("TOPIC")
client.username_pw_set(username, password)
client.connect(broker_address, 1883, 60)

PRISE1 = False
PRISE2 = False

# Start the loop
client.loop_forever()