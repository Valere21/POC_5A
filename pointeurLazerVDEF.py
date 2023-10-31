import sys
import tkinter as tk
import json
from Adafruit_IO import MQTTClient

# Configuration Adafruit IO
ADAFRUIT_IO_KEY = 'aio_oLgB78RAMwIcz3v7NcZl6Olssxuf'
ADAFRUIT_IO_USERNAME = 'valval'
FEED_ID = 'positions'

circle_radius = 20

# Initialisation de tkinter
root = tk.Tk()
root.overrideredirect(True)
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
root.attributes('-alpha', 0.01)

circle_win = tk.Toplevel(root)
circle_win.overrideredirect(True)
circle_win.attributes('-alpha', 1, '-transparentcolor', 'white')
circle_win.geometry(f"{2*circle_radius}x{2*circle_radius}")

canvas = tk.Canvas(circle_win, highlightthickness=0, bd=0, bg='white')
canvas.pack(fill=tk.BOTH, expand=tk.YES)
canvas.create_oval(0, 0, 2*circle_radius, 2*circle_radius, fill='red')

# Callback pour le client MQTT
def message(client, feed_id, payload):
    try:
        value = json.loads(payload)
        x, y = value["x"], value["y"]
        if -128 <= x <= 127 and -128 <= y <= 127:
            print(f"Valeurs reçues: x = {x}, y = {y}")
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            center_x = screen_width // 2
            center_y = screen_height // 2
            scaled_x = x * (screen_width // 256)
            scaled_y = y * (screen_height // 256)
            new_x = center_x + scaled_x
            new_y = center_y + scaled_y
            circle_win.geometry(f"{2*circle_radius}x{2*circle_radius}+{int(new_x-circle_radius)}+{int(new_y-circle_radius)}")
    except Exception as e:
        print(f"Erreur: {e}")

# Initialisation du client MQTT
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.on_message = message
client.connect()
client.subscribe(FEED_ID)

# Démarrage de la boucle tkinter
root.after(1000, client.loop_background())
root.mainloop()
