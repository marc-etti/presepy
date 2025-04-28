from flask import Flask
import os
from app.routes import main_bp
from app.services.audio_management import audio_bp
from app.services.dmx_management import dmx_bp
from app.services.devices_management import light_bp
from app.services.test import test_bp

from app.auth import auth_bp
from app import db

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    app.register_blueprint(main_bp)
    app.register_blueprint(audio_bp)
    app.register_blueprint(dmx_bp)
    app.register_blueprint(light_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(auth_bp)

    # controllo che il file data.json esista e in caso contrario lo creo
    if not os.path.exists(app.config['JSON_FILE']):
        with open(app.config['JSON_FILE'], 'w') as file:
            file.write('{devices_info: []}')

    db.init_app(app)

    # handle the 404 error
    @app.errorhandler(404)
    def page_not_found(e):
        # return render_template('404.html'), 404
        return "404 Not Found"

    return app