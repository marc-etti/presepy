from flask import Blueprint, request, jsonify
import os
from datetime import datetime

# Creazione del Blueprint
test_bp = Blueprint('test', __name__)

# Cartella contenente i file di log in ../logs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FOLDER = os.path.join(BASE_DIR, '..', 'logs')

@test_bp.route('/write_log', methods=['POST'])
def write_log():
    """Scrivi un messaggio di log su file."""
    data = request.json
    message = data.get('message')
    if not message:
        return jsonify({'error': 'Messaggio mancante'}), 400

    # Crea la cartella se non esiste
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)

    # Crea il nome del file con la data corrente
    now = datetime.now()
    log_file = os.path.join(LOG_FOLDER, f'{now.strftime("%Y-%m-%d")}.log')

    # Scrivi il messaggio di log
    with open(log_file, 'a') as f:
        f.write(f'[{now.strftime("%H:%M:%S")}] {message}\n')

    return jsonify({'message': 'Messaggio di log scritto'}), 201