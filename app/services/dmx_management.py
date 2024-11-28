from app.services.dmx.DMX_instance import dmx

from app.services.dmx.DMX_logic import running_event
from app.services.dmx.DMX_logic import main_dmx_function
from app.services.dmx.DMX_logic import inizializzazione_test

import pygame
from flask import Blueprint, request, jsonify
import os
import threading
import time

# Creazione del Blueprint
dmx_bp = Blueprint('dmx', __name__)

LOGS_FOLDER = 'app/logs'

thread = None

@dmx_bp.route('/initialize_DMX', methods=['POST'])
def initialize_DMX():
    """Inizializza l'interfaccia DMX."""
    #dmx.reset()
    inizializzazione_test()
    return jsonify({'message': 'Interfaccia DMX inizializzata'})

@dmx_bp.route('/reset_DMX', methods=['POST'])
def reset_DMX():
    """Resetta i valori dei canali DMX."""
    dmx.reset()
    return jsonify({'message': 'Valori DMX resettati'})

@dmx_bp.route('/start_DMX', methods=['POST'])
def start_DMX():
    """Avvia la funzione di invio dei valori DMX."""
    if not running_event.is_set():
        running_event.set()
        thread = threading.Thread(target=main_dmx_function)
        thread.start()
    return jsonify({'message': 'Invio valori DMX avviato'})

@dmx_bp.route('/stop_DMX', methods=['POST'])
def stop_DMX():
    """Ferma l'invio dei valori DMX."""
    if running_event.is_set():
        running_event.clear()
    return jsonify({'message': 'Invio valori DMX fermato'})


def log_dmx_data():
    global running
    if not os.path.exists(LOGS_FOLDER):
        os.makedirs(LOGS_FOLDER)
    log_file = os.path.join(LOGS_FOLDER, 'dmx_log.log')
    while running:
        dmx.write_channels_on_log(log_file)
        time.sleep(1)  # Scrive sul log ogni secondo

