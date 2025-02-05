import json
import os

from config import Config

def get_lights():
    """Restituisce la lista delle luci."""
    try:
        with open(Config.JSON_FILE, 'r') as file:
            data = json.load(file)

        devices = data.get("devices_info", [])

        lights = [device for device in devices if device['type'] == 'light']
        
        return lights
    
    except FileNotFoundError:
        raise FileNotFoundError('File non trovato')
    except json.JSONDecodeError:
        raise json.JSONDecodeError('Errore nella decodifica del file JSON')
    except Exception as e:
        raise Exception(str(e))