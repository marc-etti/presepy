class Config:
    DMX_PORT = 'change_me'
    AUDIO_PATH = 'audio'
    SECRET_KEY = 'mysecretkey'
    LOGS_FOLDER = 'app/logs/'
    LOG_FILE = 'app/logs/dmx_log.log'
    AUDIO_FOLDER = 'app/static/audio/'
    JSON_FILE = 'data/data.json'
    DEBUG = True
    TEST = True

    DATA_SQL = 'data/data.sql'
    SCHEMA_SQL = 'data/schema.sql'
    DATABASE = 'data/presepy.sqlite'