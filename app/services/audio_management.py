from config import Config

import pygame
from flask import Blueprint, request, jsonify
import os
import threading
import time

# Creazione del Blueprint
audio_bp = Blueprint('audio', __name__)

# variabili globali
current_track = None
is_playing = False

# Inizializzazione di pygame mixer
pygame.mixer.init()

# Funzione per ottenere la lista di file audio
def get_audio_files():
    return [f for f in os.listdir(Config.AUDIO_FOLDER) if f.endswith(('.mp3', '.wav', '.ogg'))]

# Thread di controllo della riproduzione
def background_player():
    """Thread che controlla lo stato della riproduzione."""
    global is_playing
    while True:
        if is_playing and not pygame.mixer.music.get_busy():
            is_playing = False
        time.sleep(1)

# Avvia il thread in background
threading.Thread(target=background_player, daemon=True).start()

@audio_bp.route('/play', methods=['POST'])
def play():
    """Avvia la riproduzione di una traccia audio."""
    global current_track, is_playing
    data = request.json
    track_name = data.get('track')
    if not track_name or track_name not in get_audio_files():
        return jsonify({'error': 'Traccia non trovata'}), 404

    track_path = os.path.join(Config.AUDIO_FOLDER, track_name)
    pygame.mixer.music.load(track_path)
    pygame.mixer.music.play()
    current_track = track_name
    is_playing = True
    return jsonify({'message': f'Riproduzione avviata: {track_name}'})

@audio_bp.route('/pause', methods=['POST'])
def pause():
    """Mette in pausa la riproduzione."""
    pygame.mixer.music.pause()
    return jsonify({'message': 'Riproduzione in pausa'})

@audio_bp.route('/resume', methods=['POST'])
def resume():
    """Riprende la riproduzione."""
    pygame.mixer.music.unpause()
    return jsonify({'message': 'Riproduzione ripresa'})

@audio_bp.route('/stop', methods=['POST'])
def stop():
    """Interrompe la riproduzione."""
    global is_playing
    pygame.mixer.music.stop()
    is_playing = False
    return jsonify({'message': 'Riproduzione interrotta'})

@audio_bp.route('/status', methods=['GET'])
def status():
    """Restituisce lo stato corrente della riproduzione."""
    if pygame.mixer.music.get_busy():
        return jsonify({'status': 'playing', 'track': current_track})
    return jsonify({'status': 'stopped', 'track': None})

@audio_bp.route('/tracks', methods=['GET'])
def tracks():
    """Restituisce la lista delle tracce audio disponibili."""
    return jsonify({'tracks': get_audio_files()})