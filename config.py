class Config:
    SECRET_KEY = 'mysecretkey'
    LOG_FILE = 'app/logs/dmx_log.log'
    DEBUG = True
    TEST = True

    # Configurazione del database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///presepy.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False