from app import create_app
from config import Config
import click

app = create_app(Config)

@click.command()
@click.option('--test', is_flag=True, help='Esegui i test')
def run(test):
    """Esegui l'applicazione Flask."""
    if test:
        # Esegui i test
        pass
    else:
        # Esegui l'applicazione
        app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)

if __name__ == '__main__':
    run()