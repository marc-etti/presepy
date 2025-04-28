from app import create_app
from config import Config
import os

app = create_app()

if __name__ == '__main__':
    if not os.path.exists(Config.DATABASE):
        print(f"Database non trovato in {Config.DATABASE}. Eseguire 'flask init-db' per inizializzarlo.")
        exit(1)
    app.run(debug=True, host='localhost', port=5000)