import requests
import sys
import json

def send_to_adafruit_io(x, y):
    # Votre clé et nom d'utilisateur Adafruit IO
    ADAFRUIT_IO_KEY = 'aio_wJFt18d2Azl9yYkdMNs8CRcTJIm0'
    ADAFRUIT_IO_USERNAME = 'valval'
    FEED_ID = 'positions'
    
    # URL du feed
    url = f"https://io.adafruit.com/api/v2/{ADAFRUIT_IO_USERNAME}/feeds/{FEED_ID}/data"
    
    # Entêtes HTTP
    headers = {
        'X-AIO-Key': ADAFRUIT_IO_KEY,
    }

    # Données à envoyer sous forme de dictionnaire JSON
    payload = {
        'value': json.dumps({"x": int(x), "y": int(y)})
    }
    
    # Envoyer la requête POST avec les données JSON
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print(f"Les données ont été envoyées avec succès: x:{x}, y:{y}")
    else:
        print(f"Erreur: {response.status_code}")
        print(response.text)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py <x_value> <y_value>")
        sys.exit(1)
        
    x_value = sys.argv[1]
    y_value = sys.argv[2]
    
    send_to_adafruit_io(x_value, y_value)

