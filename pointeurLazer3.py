import requests
import json
import time
import tkinter as tk
import pyautogui

# Configuration Adafruit IO
ADAFRUIT_IO_KEY = 'aio_EvvJ15E0NlrMhlFP04L83cZAOpxG'
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
        print(f"Dernière valeur lue : x = {value['x']}, y = {value['y']}")  # Debug de la dernière valeur lue
        return value["x"], value["y"]
    else:
        print(f"Erreur: {response.status_code}")
        return None, None

def move_circle(delta_x, delta_y):
    # Conversion des valeurs delta_x et delta_y pour correspondre à la taille de l'écran
    target_x = screen_center_x + (circle_radius * delta_x / 128)
    target_y = screen_center_y + (circle_radius * delta_y / 128)
    canvas.coords(circle, target_x - circle_radius, target_y - circle_radius, target_x + circle_radius, target_y + circle_radius)

def update_circle_position():
    # Récupérer les données depuis Adafruit IO
    delta_x, delta_y = get_latest_feed_data()

    if delta_x is not None and delta_y is not None:
        move_circle(delta_x, delta_y)
    
    root.after(1000, update_circle_position)  # Rafraîchissement toutes les secondes

# GUI avec tkinter
root = tk.Tk()
root.overrideredirect(True)
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
root.attributes('-alpha', 0.4)
root.configure(bg='')

canvas = tk.Canvas(root, bg='white', highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=tk.YES)

screen_center_x = root.winfo_screenwidth() // 2
screen_center_y = root.winfo_screenheight() // 2
circle_radius = min(screen_center_x, screen_center_y) // 10
circle = canvas.create_oval(screen_center_x - circle_radius, screen_center_y - circle_radius,
                            screen_center_x + circle_radius, screen_center_y + circle_radius, fill='red')

canvas.bind_all('<Key>', lambda event: root.destroy() if event.keysym == 'Escape' else None)

update_circle_position()  # Initialisation de la mise à jour de la position du cercle
root.mainloop()
