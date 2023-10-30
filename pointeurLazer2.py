import requests
import json
import time
import math
import pyautogui

# Configuration Adafruit IO
ADAFRUIT_IO_KEY = 'aio_wJFt18d2Azl9yYkdMNs8CRcTJIm0'
ADAFRUIT_IO_USERNAME = 'valval'
FEED_ID = 'positions'
API_URL = f"https://io.adafruit.com/api/v2/{ADAFRUIT_IO_USERNAME}/feeds/{FEED_ID}/data/last"

HEADERS = {
    'X-AIO-Key': ADAFRUIT_IO_KEY,
}

def get_latest_feed_data():
    response = requests.get(API_URL, headers=HEADERS)
    if response.status_code == 200:
        data = json.loads(response.text)
        value = json.loads(data['value'])
        return value["x"], value["y"]
    else:
        print(f"Erreur: {response.status_code}")
        return None, None

# Fonction pour mapper une valeur d'une plage à une autre
def remap(old_value, old_min, old_max, new_min, new_max):
    return (old_value - old_min) * (new_max - new_min) / (old_max - old_min) + new_min

# Obtenir la taille de l'écran
screen_width, screen_height = pyautogui.size()

# Boucle principale
running = True
speed = 1 # Contrôlez la vitesse du mouvement du curseur

while running:
    # Récupérer les données depuis Adafruit IO
    delta_x, delta_y = get_latest_feed_data()

    if delta_x is not None and delta_y is not None:
        # Convertir les valeurs delta_x et delta_y pour correspondre à la taille de l'écran
        target_x = remap(delta_x, -128, 127, 0, screen_width)
        target_y = remap(delta_y, -128, 127, 0, screen_height)

        # Obtenir la position actuelle du curseur
        current_x, current_y = pyautogui.position()

        # Calculer les étapes de déplacement pour le curseur
        step_x = (target_x - current_x) / speed
        step_y = (target_y - current_y) / speed

        # Bouger le curseur progressivement vers la position cible
        for _ in range(speed):
            current_x += step_x
            current_y += step_y
            pyautogui.moveTo(current_x, current_y)
            time.sleep(0.01)  # Temps de pause pour voir le mouvement

        # Écrire la position du curseur
        print(f"Position du curseur : x = {current_x}, y = {current_y}")

    # Attendre avant la prochaine requête
    time.sleep(0.05)

