from config import Config

from flask import Blueprint, request, jsonify

import json

from app.services.devices_utils.lights_utils import get_lights

# Creazione del Blueprint
light_bp = Blueprint('light', __name__)

@light_bp.route('/get_lights_info', methods=['GET'])
def get_lights_info():
    lights = get_lights()
    return jsonify(lights)
    

    

    