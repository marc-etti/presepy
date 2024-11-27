from app.services.dmx.DMX import DMX
from app.services.controllers.led_controller import LedController

import pygame
from flask import Blueprint, request, jsonify
import os
import threading
import time

# Creazione del Blueprint
dmx_bp = Blueprint('dmx', __name__)

LOGS_FOLDER = 'app/logs'

# Inizializzazione dell'interfaccia DMX
dmx = DMX()

# Creazione di un controller per i LED
led_controller = LedController(dmx, 1)

# Variabile per controllare il thread
running = False
thread = None

def log_dmx_data():
    global running
    if not os.path.exists(LOGS_FOLDER):
        os.makedirs(LOGS_FOLDER)
    log_file = os.path.join(LOGS_FOLDER, 'dmx_log.log')
    while running:
        dmx.write_channels_on_log(log_file)
        time.sleep(1)  # Scrive sul log ogni secondo

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
    global running, thread
    if not running:
        running = True
        #   thread = threading.Thread(target=log_dmx_data)
        thread = threading.Thread(target=main_dmx_function)
        thread.start()
    return jsonify({'message': 'Invio valori DMX avviato'})

@dmx_bp.route('/stop_DMX', methods=['POST'])
def stop_DMX():
    """Ferma l'invio dei valori DMX."""
    global running, thread
    if running:
        running = False
        thread.join()
    return jsonify({'message': 'Invio valori DMX fermato'})

def inizializzazione_test():
    """Inizializza l'interfaccia DMX."""
    dmx.set_channel(1, 255)
    dmx.set_channel(2, 255)
    dmx.set_channel(3, 255)
    dmx.set_channel(4, 255)
    dmx.set_channel(5, 255)
    dmx.set_channel(6, 255)
    dmx.set_interval(7, 20, 20)

def main_dmx_function():
    """Funzione di loop che si occupa di aggiornare i valori del DMX
    e inviarli alla porta USB specificata."""
    while running:
        led_controller.increase_color('red', 1, dmx)
        led_controller.increase_color('green', 1, dmx)
        led_controller.increase_color('blue', 1, dmx)
        dmx.write_channels_on_log('app/logs/dmx_log.log')
        time.sleep(0.5)