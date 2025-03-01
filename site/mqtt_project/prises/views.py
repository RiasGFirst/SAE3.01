import os
import time

from django.shortcuts import render, redirect
from .mqtt_client import prise_states, MQTTClient

mqtt_client = MQTTClient()


def home(request):
    # Rendre la page avec les états actuels des prises
    mqtt_client.publish("PRISE1_STATE")
    mqtt_client.publish("PRISE2_STATE")
    return render(request, 'home.html')


def login(request):
    # Vérification des identifiants de connexion
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == os.getenv("DASH_USERNAME") and password == os.getenv("DASH_PASSWORD"):
            # Création d'un cookie nommé 'login' avec la valeur 'true'
            response = redirect('dash')
            response.set_cookie('login', 'true')
            return response
        else:
            # Redirection vers la page de connexion
            return redirect('home')
    else:
        return redirect('home')


def logout(request):
    # Suppression du cookie 'login'
    response = redirect('home')
    response.delete_cookie('login')
    return response


def index(request):
    # Check if we have a cookie named 'login' with the value 'true'
    if request.COOKIES.get('login') == 'true':
        time.sleep(0.5)
        return render(request, 'secure.html', {'prise_states': prise_states})
    else:
        # Rediriger l'utilisateur vers la page de connexion
        return redirect('home')


def toggle_prise(request, prise):
    # Envoi de la commande MQTT pour basculer l'état de la prise
    mqtt_client.publish(f"{prise}_TOGGLE")
    time.sleep(0.5)
    return redirect('dash')

def control_all1(request):
    # Sinon, on allume toutes les prises
    mqtt_client.publish("PRISE1_ON")
    mqtt_client.publish("PRISE2_ON")
    time.sleep(1)
    return redirect('dash')

def control_all0(request):
    # Sinon, on éteint toutes les prises
    mqtt_client.publish("PRISE1_OFF")
    mqtt_client.publish("PRISE2_OFF")
    time.sleep(1)
    return redirect('dash')