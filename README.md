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
│   ├── __init__.py          # Inizializzazione del pacchetto Flask
│   ├── routes.py            # Definizione delle rotte Flask
│   ├── templates/           # File HTML per il frontend
│   │   ├── base.html        # Layout base per tutte le pagine
│   │   ├── index.html       # Homepage con interfaccia principale
│   │   ├── dmx.html         # Pagina di gestione DMX
│   │   └── musica.html      # Pagina di gestione musica
│   ├── static/              # File statici (CSS, JS, immagini)
│   │   ├── css/
│   │   │   └── styles.css   # Foglio di stile per l'interfaccia
│   │   ├── js/
│   │   │   └── app.js       # Script JavaScript personalizzati
│   │   └── images/          # Immagini usate nell'interfaccia
|   |       └── favicon.ico  # Icona del sito
|   ├── services/            # Servizi per la gestione del presepe
│   │   ├── controllers/     # Controller per la gestione delle luci
│   │   │   ├── controller_faro.py      # Controller per la gestione del faro
│   │   │   └── controller_led.py       # Controller per la gestione dei led
│   │   ├── dmx/             # Cartella per la gestione DMX
│   │   │   ├── DMX_data.py  # Modello per la gestione DMX
│   │   │   └── DMX_logic.py # Logica per la gestione DMX
│   │   ├── audio_management.py         # Gestione della riproduzione audio
│   │   └── dmx_management.py           # Gestione della comunicazione DMX
│   └── utils/               # Moduli di utilità
│       ├── common.py        # Funzioni comuni per il progetto
│       └── crib_linea.py    # Crib linea 
├── data/                    # Cartella di file in cui salvare lo stato
│   └── data.json            # info dispositivi e stato salvato
├── config.py                # Configurazione del progetto
├── requirements.txt         # Elenco delle dipendenze del progetto
├── run.py                   # File principale per avviare l'app
├── avvio.sh                 # Script per avviare l'applicazione
└── README.md                # Documentazione del progetto

``` 
