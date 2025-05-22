import os

class Config:
    SECRET_KEY = 'mysecretkey'
    DEBUG = True
    TEST = True

    if not os.path.exists('app/logs'):
        # Creazione della cartella logs se non esiste
        os.makedirs('app/logs')
        # Creazione del file di log vuoto
        with open('app/logs/DMX.log', 'w') as f:
            pass
    LOG_FILE = 'app/logs/DMX.log'
        

    if os.path.exists('/.dockerenv'):
        # Configurazione per Docker
        HOST = '0.0.0.0'
    else:
        # Configurazione per l'esecuzione locale
        HOST = 'localhost'
    PORT = 5000

    # Configurazione del database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///presepy.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    SECRET_KEY = 'mysecretkey'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = False
    LOG_FILE = 'app/logs/DMX_test.log'  # Log file for testing