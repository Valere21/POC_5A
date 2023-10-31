import tkinter as tk

def on_canvas_click(event):
    """Déplace le cercle à la position du clic."""
    x, y = event.x, event.y
    canvas.coords(circle, x-50, y-50, x+50, y+50)

def on_key(event):
    """Ferme la fenêtre si 'Echap' est pressé."""
    if event.keysym == 'Escape':
        root.destroy()

root = tk.Tk()
root.overrideredirect(True)  # Supprime la bordure de la fenêtre
root.geometry('+300+300')  # Position initiale de la fenêtre
root.attributes('-alpha', 0.4)  # Rend la fenêtre transparente
root.configure(bg='')  # Enlève la couleur d'arrière-plan

canvas = tk.Canvas(root, bg='white', highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=tk.YES)

# Dessine un cercle rouge
circle = canvas.create_oval(25, 25, 125, 125, fill='red')
canvas.bind('<Button-1>', on_canvas_click)
canvas.bind_all('<Key>', on_key)

root.mainloop()