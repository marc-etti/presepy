from config import Config
from app.services.dmx.DMX_logic import dmx

from app.services.dmx.DMX_logic import state_manager


from app.services.dmx.DMX_logic import main_dmx_function
from app.services.dmx.DMX_logic import inizializzazione

from flask import Blueprint, request, jsonify, current_app
import threading

# Variabile globale per il thread 
thread = None

# Creazione del Blueprint
dmx_bp = Blueprint('dmx', __name__)

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
    if state_manager.is_on():
        return jsonify({'message': 'Il sistema è già acceso'})
    else:
        state_manager.turn_on()
        app = current_app._get_current_object()
        thread = threading.Thread(target=main_dmx_function, args=(app,), name = 'DMX_thread')
        thread.start()
        return jsonify({'message': 'Invio valori DMX avviato'})

@dmx_bp.route('/stop_DMX', methods=['POST'])
def stop_DMX():
    """Ferma l'invio dei valori DMX."""
    if state_manager.is_on():
        state_manager.turn_off()
        return jsonify({'message': 'Invio valori DMX fermato'})
    else:
        return jsonify({'message': 'Il sistema è già spento'})

@dmx_bp.route('/pause_DMX', methods=['POST'])
def pause_DMX():
    """Mette in pausa l'invio dei valori DMX."""
    if state_manager.is_on():
        state_manager.pause()
        return jsonify({'message': 'Invio valori DMX in pausa'})
    else:
        return jsonify({'message': 'Il sistema è spento'})

@dmx_bp.route('/resume_DMX', methods=['POST'])
def resume_DMX():
    """Riprende l'invio dei valori DMX dalla pausa."""
    if state_manager.is_on():
        state_manager.resume()
        return jsonify({'message': 'Invio valori DMX ripreso'})
    else:
        return jsonify({'message': 'Il sistema è spento'})

@dmx_bp.route('/stampa_DMX', methods=['POST'])
def stampa_DMX():
    """Stampa i valori dei canali DMX sul file di log."""
    dmx.write_channels_on_log(Config.LOGS_FOLDER + 'dmx_log.log')
    return jsonify({'message': 'Valori DMX stampati sul log'})

@dmx_bp.route('/get_current_status', methods=['GET'])
def get_current_status():
    """Restituisce lo stato corrente."""
    return jsonify({'current_phase': state_manager.get_phase(), 'is_on': state_manager.is_on()})
#TODO: usare la variabile is_on per colorare il bottone di start/stop

#TODO: capire se è meglio fermare il ciclo con una variabile globale o con un evento
