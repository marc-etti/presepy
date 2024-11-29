from flask import Flask
import os
from app.routes import main_bp
from app.services.audio_management import audio_bp
from app.services.dmx_management import dmx_bp
from app.services.test import test_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    app.register_blueprint(main_bp)
    app.register_blueprint(audio_bp)
    app.register_blueprint(dmx_bp)
    app.register_blueprint(test_bp)

    # controllo che la cartella per i log esista
    if not os.path.exists(app.config['LOGS_FOLDER']):
        os.makedirs(app.config['LOGS_FOLDER'])

    return app