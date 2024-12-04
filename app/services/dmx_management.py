from config import Config
from app.services.dmx.DMX_logic import dmx

from app.services.dmx.DMX_logic import state_manager

from app.services.dmx.DMX_logic import running_event
from app.services.dmx.DMX_logic import main_dmx_function
from app.services.dmx.DMX_logic import inizializzazione

from flask import Blueprint, request, jsonify
import threading

# Creazione del Blueprint
dmx_bp = Blueprint('dmx', __name__)

# Variabile globale per il thread 
thread = None

@dmx_bp.route('/initialize_DMX', methods=['POST'])
def initialize_DMX():
    """Inizializza l'interfaccia DMX."""
    inizializzazione()
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
        state_manager.turn_on()
        running_event.set()
        thread = threading.Thread(target=main_dmx_function)
        thread.start()
    return jsonify({'message': 'Invio valori DMX avviato'})

@dmx_bp.route('/stop_DMX', methods=['POST'])
def stop_DMX():
    """Ferma l'invio dei valori DMX."""
    if running_event.is_set():
        state_manager.turn_off()
        running_event.clear()
    return jsonify({'message': 'Invio valori DMX fermato'})

@dmx_bp.route('/stampa_DMX', methods=['POST'])
def stampa_DMX():
    """Stampa i valori dei canali DMX sul file di log."""
    dmx.write_channels_on_log(Config.LOGS_FOLDER + 'dmx_log.log')
    return jsonify({'message': 'Valori DMX stampati sul log'})

@dmx_bp.route('/get_current_phase', methods=['GET'])
def get_current_phase():
    """Restituisce la fase corrente."""
    return jsonify({'current_phase': state_manager.get_phase(), 'is_on': state_manager.is_on()})
