import requests
import json
import tkinter as tk

# Configuration Adafruit IO
ADAFRUIT_IO_KEY = 'aio_YOYa32DiptVNpCXzOmUxyae0gSbM'
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

circle_radius = 20

def update_circle_position():
    x, y = get_latest_feed_data()
    if x and y and -128 <= x <= 127 and -128 <= y <= 127:
        print(f"Valeurs lues: x = {x}, y = {y}")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = screen_width // 2
        center_y = screen_height // 2
        scaled_x = x * (screen_width // 256)
        scaled_y = y * (screen_height // 256)
        new_x = center_x + scaled_x
        new_y = center_y + scaled_y
        circle_win.geometry(f"{2*circle_radius}x{2*circle_radius}+{int(new_x-circle_radius)}+{int(new_y-circle_radius)}")
    root.after(500, update_circle_position)

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

update_circle_position()

root.mainloop()
