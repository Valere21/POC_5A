import pygame
import requests
import json
import time

# Configuration Adafruit IO
ADAFRUIT_IO_KEY = 'aio_iIXw136O8E8SyHjsQEiHupnTX2kf'
ADAFRUIT_IO_USERNAME = 'valval'
FEED_ID = 'pointeurlazer'
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
            latest_data = feed_data[0]["value"]
            x, y = map(int, latest_data.replace("x:", "").replace("y:", "").split(","))
            return x, y
    else:
        print(f"Erreur: {response.status_code}")
        return None, None

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Récupérer les données depuis Adafruit IO
    x, y = get_latest_feed_data()

    if x is not None and y is not None:
        # Convertir les valeurs en coordonnées d'écran
        screen_x = int((x / 4096) * width)
        screen_y = int((y / 4096) * height)

        # Écrire la position du point
        print(f"Position du curseur : x = {screen_x}, y = {screen_y}")

        # Effacer l'écran
        screen.fill((0, 0, 0))

        # Dessiner le point rouge à la position calculée
        pygame.draw.circle(screen, red, (screen_x, screen_y), 5)

        # Mettre à jour l'affichage
        pygame.display.flip()

    # Attendre 1 seconde avant la prochaine requête
    time.sleep(1)

# Quitter pygame
pygame.quit()

