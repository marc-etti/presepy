import os
import click

from flask import Flask, render_template
from flask.cli import with_appcontext
from flask_login import LoginManager
from app.db import db, init_db, seed_development_db

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    from app.routes import main_bp
    from app.services.audio_management import audio_bp
    from app.services.dmx_management import dmx_bp
    from app.services.devices_management import devices_bp
    from app.services.keyframes_management import keyframes_bp
    from app.auth import auth_bp

    # Registra i blueprint
    app.register_blueprint(main_bp)
    app.register_blueprint(audio_bp)
    app.register_blueprint(dmx_bp)
    app.register_blueprint(devices_bp)
    app.register_blueprint(keyframes_bp)
    app.register_blueprint(auth_bp)

    # Inizializza SQLAlchemy
    db.init_app(app)
    app.cli.add_command(init_db_command)

    # Inizializza Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Associa il modello User a Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    # handle the 404 error
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    # init_db()
    seed_development_db()
    click.echo("Initialized the database.")