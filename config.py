class Config:
    DMX_PORT = 'change_me'
    SECRET_KEY = 'mysecretkey'
    LOGS_FOLDER = 'app/logs/'
    LOG_FILE = 'app/logs/dmx_log.log'
    DEBUG = True
    TEST = True

    # Configurazione del database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///presepy.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False