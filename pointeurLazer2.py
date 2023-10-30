import pygame
import requests
import json
import time
import math

# Configuration Adafruit IO
ADAFRUIT_IO_KEY = 'aio_OzEj24OYumLFZAGTLs8QPsEq5QLk'
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


# Initialisation de pygame
pygame.init()

# Récupérer la résolution de l'écran
infoObject = pygame.display.Info()
width, height = infoObject.current_w, infoObject.current_h

# Configuration de la fenêtre
screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
pygame.display.set_caption("Pointeur Laser")


# Couleur du point (rouge)
red = (255, 0, 0)

# Initialisation des variables pour le mouvement
current_x, current_y = width // 2, height // 2
target_x, target_y = current_x, current_y
speed = 0.05  # Vitesse de déplacement du pointeur vers la cible

# Boucle principale
running = True
start_time = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Récupérer les données depuis Adafruit IO
    delta_x, delta_y = get_latest_feed_data()

    elapsed_time = (time.time() - start_time) % 1  # Normalisé entre 0 et 1
    sigmoid = 1 / (1 + math.exp(-10*(elapsed_time - 0.5)))

    if delta_x is not None and delta_y is not None:
        target_x, target_y = delta_x, delta_y

        # Calcul de la différence entre la position actuelle et la cible
        diff_x = target_x - current_x
        diff_y = target_y - current_y

        # Mise à jour des positions en fonction de la vitesse
        current_x += diff_x * speed
        current_y += diff_y * speed
        # Écrire la position du point
        print(f"Position du curseur : x = {current_x}, y = {current_y}")

        # Effacer l'écran
        screen.fill((0, 0, 0, 0))  # Remplir avec une couleur transparente
        
        # Dessiner le point rouge à la position calculée
        pygame.draw.circle(screen, red, (current_x, current_y), 5)

        # Mettre à jour l'affichage
        pygame.display.flip()

    # Attendre avant la prochaine requête
    time.sleep(0.05)  # Réduisez cette valeur pour une animation plus fluide

# Quitter pygame
pygame.quit()

