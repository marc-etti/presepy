import click
from config import Config

from flask import Flask, render_template
from flask.cli import with_appcontext
from flask_login import LoginManager
from app.db import db, init_db

login_manager = LoginManager()

def create_app(myConfig=Config):
    app = Flask(__name__)

    # Importa le configurazioni
    app.config.from_object(myConfig)

    # Importa i blueprint
    from app.services.dmx_management import dmx_bp
    from app.services.devices_management import devices_bp
    from app.services.keyframes_management import keyframes_bp
    from app.services.phases_managements import phases_bp
    from app.services.auth_management import auth_bp
    from app.services.admin_management import admin_bp

    # Registra i blueprint
    app.register_blueprint(dmx_bp)
    app.register_blueprint(devices_bp)
    app.register_blueprint(keyframes_bp)
    app.register_blueprint(phases_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Inizializza SQLAlchemy
    db.init_app(app)
    app.cli.add_command(init_db_command)

    # Inizializza Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Devi essere autenticato per accedere a questa pagina."
    login_manager.login_message_category = "error"


    # Associa il modello User a Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return db.session.get(User, user_id)   

    # Handle per l'errore 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    # Handle per l'errore 403
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    return app

# Comando per inizializzare il database
@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Database inizializzato.")