# Presepy - Gestione di un presepe elettronico

## Creazione ambiente virtuale

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Avvio dell'applicazione

```bash
python run.py
```

## Terminazione applicazione

```bash
CTRL+C
deactivate
```

## Accesso all'interfaccia web

L'interfaccia web è accessibile all'indirizzo [http://localhost:5000/](http://localhost:5000/).


## Configurazione

Il file `config.py` contiene le seguenti variabili di configurazione:

- `DEBUG`: abilita la modalità di debug di Flask
- `SECRET_KEY`: chiave segreta per la sessione di Flask
- `DMX_PORT`: porta seriale per la comunicazione DMX512
- `AUDIO_DIR`: percorso della cartella contenente i file audio
- `LOGS_FILE`: percorso del file di log

## Dipendenze

- Flask
- Flask-WTF
- pygame

## Funzionalità

- Interfaccia web per la gestione di un presepe elettronico
- Controllo delle luci tramite protocollo DMX512
- Riproduzione di suoni e musiche
- Pianificazione di eventi tramite file JSON
- Configurazione tramite interfaccia web


## Struttura

```plaintext
presepy/
├── app/
│   ├── __init__.py          # Inizializzazione del pacchetto Flask -
│   ├── routes.py            # Definizione delle rotte Flask        -
│   ├── templates/           # File HTML per il frontend            -
│   │   ├── base.html        # Layout base per tutte le pagine      -
│   │   ├── index.html       # Homepage con interfaccia principale  -
│   │   └── settings.html    # Pagina di configurazione             -
│   ├── static/              # File statici (CSS, JS, immagini)     -
│   │   ├── css/                                                    -
│   │   │   └── styles.css   # Foglio di stile per l'interfaccia    -
│   │   ├── js/                                                     -
│   │   │   └── app.js       # Script JavaScript personalizzati     -
│   │   └── images/          # Immagini usate nell'interfaccia      -
│   └── utils/               # Moduli di utilità                    -
│       ├── dmx_controller.py  # Gestione del protocollo DMX512     -
│       ├── scheduler.py       # Logica di pianificazione eventi    -
│       └── audio_player.py    # Gestione di suoni e musiche        -
├── config.py                # Configurazione del progetto          -
├── requirements.txt         # Elenco delle dipendenze del progetto -
├── run.py                   # File principale per avviare l'app    -
└── README.md                # Documentazione del progetto          -

``` 
