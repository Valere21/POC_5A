import pygame
import requests
import json
import time

# Configuration Adafruit IO
ADAFRUIT_IO_KEY = 'aio_iIXw136O8E8SyHjsQEiHupnTX2kf'
ADAFRUIT_IO_USERNAME = 'valval'
FEED_ID = 'positions'
URL = f"https://io.adafruit.com/api/v2/{ADAFRUIT_IO_USERNAME}/feeds/{FEED_ID}/data"

headers = {
    "X-AIO-Key": ADAFRUIT_IO_KEY,
}

# Initialisation de pygame
pygame.init()

# Configuration de la fenêtre
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pointeur Laser")

# Couleur du point (rouge)
red = (255, 0, 0)

def get_latest_feed_data():
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        feed_data = json.loads(response.content)
        if feed_data:
            value_str = feed_data[0]["value"]
            print(f"Received data: {value_str}")  # Pour le débogage
            if value_str:  # Vérifie que la chaîne n'est pas vide
                try:
                    latest_data = json.loads(value_str)  # Charger la chaîne JSON en dictionnaire
                    return latest_data.get('x'), latest_data.get('y')
                except json.JSONDecodeError:
                    print(f"Invalid JSON: {value_str}")
                    return None, None
            else:
                print("Received empty JSON string.")
                return None, None
    else:
        print(f"Erreur: {response.status_code}")
        return None, None

        
# Initialisation des variables pour le mouvement
current_x, current_y = width // 2, height // 2
velocity_x, velocity_y = 0, 0
jolt_factor = 1  # Facteur d'accélération "jolt"

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Récupérer les données depuis Adafruit IO
    delta_x, delta_y = get_latest_feed_data()
    
    if delta_x is not None and delta_y is not None:
        
        # Ignorer les valeurs en dehors de l'intervalle [-128, 127]
        if -128 <= delta_x <= 127 and -128 <= delta_y <= 127:
            
            # Appliquer la fonction de jolt
            velocity_x += jolt_factor * delta_x
            velocity_y += jolt_factor * delta_y
            
            # Mettre à jour les positions
            current_x += velocity_x
            current_y += velocity_y

            # Restreindre les coordonnées à l'intérieur de la fenêtre
            current_x = max(0, min(width, current_x))
            current_y = max(0, min(height, current_y))

            # Écrire la position du point
            print(f"Position du curseur : x = {current_x}, y = {current_y}")

            # Effacer l'écran
            screen.fill((0, 0, 0))

            # Dessiner le point rouge à la position calculée
            pygame.draw.circle(screen, red, (current_x, current_y), 5)

            # Mettre à jour l'affichage
            pygame.display.flip()

    # Attendre 1 seconde avant la prochaine requête
    time.sleep(1)

# Quitter pygame
pygame.quit()

