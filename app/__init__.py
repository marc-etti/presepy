import os
import click

from flask import Flask, render_template
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    from app.routes import main_bp
    from app.services.audio_management import audio_bp
    from app.services.dmx_management import dmx_bp
    from app.services.devices_management import light_bp
    from app.services.test import test_bp
    from app.auth import auth_bp

    # Registra i blueprint
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

def init_db():
    # Ottieni l'app corrente
    from app.models.user import User
    from flask import current_app

    with current_app.app_context():
        db.drop_all()
        db.create_all()

        # Crea le fixture
        fixtures = {
            'admin': {
                'username': 'admin',
                'password': 'admin',
                'is_admin': True,
                'is_active': True
            },
            'user': {
                'username': 'user',
                'password': 'user',
                'is_admin': False,
                'is_active': True
            }
        }
        # Aggiungi gli utenti al database
        try:
            for user_data in fixtures.values():
                # Crea un nuovo utente
                user = User(username=user_data['username'], password=user_data['password'])
                # Aggiungi l'utente alla sessione
                db.session.add(user)
            # Commit the changes to the database
            db.session.commit()
            print("Users added successfully.")
        except Exception as e:
            # Rollback in caso di errore
            db.session.rollback()
            print(f"Error occurred while adding users: {e}")
        # Chiudi la sessione
        finally:    
            db.session.close()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")