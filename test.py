import requests
import sys

def send_to_adafruit_io(x, y):
    # Votre clé et nom d'utilisateur Adafruit IO
    ADAFRUIT_IO_KEY = 'aio_iIXw136O8E8SyHjsQEiHupnTX2kf'
    ADAFRUIT_IO_USERNAME = 'valval'
    FEED_ID = 'pointeurlazer'
    
    # URL du feed
    url = f"https://io.adafruit.com/api/v2/{ADAFRUIT_IO_USERNAME}/feeds/{FEED_ID}/data"
    
    # Entêtes HTTP
    headers = {
        'X-AIO-Key': ADAFRUIT_IO_KEY,
    }

    # Données à envoyer
    payload = {
        'value': f"x:{x},y:{y}"
    }
    
    # Envoyer la requête POST
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

