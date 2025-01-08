from config import Config

from flask import Blueprint, request, jsonify

import json

# Creazione del Blueprint
light_bp = Blueprint('light', __name__)

@light_bp.route('/get_lights', methods=['GET'])
def get_lights():
    """Restituisce la lista delle luci."""
    try:
        with open(Config.JSON_FILE, 'r') as file:
            data = json.load(file)

        devices = data.get("devices_info", [])

        lights = [device for device in devices if device['type'] == 'light']
        
        return jsonify({'lights': lights})
    except FileNotFoundError:
        return jsonify({'message': 'File non trovato'})
    except json.JSONDecodeError:
        return jsonify({'message': 'Errore nella decodifica del file JSON'})
    except Exception as e:
        return jsonify({'message': str(e)})
    

    

    