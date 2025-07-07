# Presepy - Gestione di un presepe elettronico
Presepy è un'applicazione web per la gestione di un presepe elettronico, sviluppata in Python utilizzando il framework Flask. L'applicazione attualmente consente la gestione di dispositivi di illuminazione pilotabili tramite protocollo DMX512.
Le funzionalità principali includono:
- Creazione, modifica e cancellazione di dispositivi
- Creazione, modifica e cancellazione di keyframe
- Creazione, modifica e cancellazione di fasi
- Avvio, pausa e stop della trasmissione dei dati DMX (simulata con una scrittura su file di log)
- Visualizzazione dello stato dei dispositivi e delle fasi
- L'amministratore può gestire gli utenti e i loro ruoli:
    - `User`: può visualizzare lo stato dei dispositivi e delle fasi, ma non può modificarli
    - `Expert`: può anche aggiungere, modificare e cancellare dispositivi, keyframe e fasi


## Struttura del progetto
```
presepy/
├── app/                  # Directory principale dell'applicazione
│   ├── logs/                # Directory per i file di log
│   ├── models/              # Modelli del database
│   ├── services/            # Gestione della logica di business
│   ├── static/              # File statici (CSS, JS, immagini)
│   ├── templates/           # Template HTML per l'interfaccia utente
│   ├── utils/               # Funzioni di utilità
│   ├── __init__.py          # Inizializzazione dell'applicazione Flask
│   ├── db.py                # Gestione del database
|   └──  decorators.py       # Decoratori per la gestione delle autorizzazioni
├── instance/presepy.sqlite  # Database SQLite
├── tests/                # Directory dei test
├── config.py             # Configurazione dell'applicazione
├── run.py                # Punto di ingresso dell'applicazione
├── requirements.txt      # Dipendenze del progetto
├── avvio.sh              # Script per l'avvio dell'applicazione
├── Dockerfile            # File per la creazione dell'immagine Docker
├── docker-compose.yml    # File di configurazione per Docker Compose
├── entrypoint.sh         # Script di entrypoint per Docker
├── README.md             # Documentazione del progetto
├── LICENSE               # Licenza del progetto
├── .gitignore            # File per ignorare file e cartelle non necessari
└── .dockerignore         # File per ignorare file e cartelle non necessari in Docker
```

## Avvio dell'applicazione
Una volta scaricato il repository, è possibile avviare l'applicazione in locale. Assicurarsi di avere installato `Python 3.10` o superiore e di avere `pip` installato.
Su linux è sufficiente eseguire lo script `avvio.sh` che si occuperà di:
- Creare un ambiente virtuale
- Installare le dipendenze
- Creare il database
- Avviare l'applicazione
```bash
chmod +x avvio.sh
./avvio.sh
```

L'interfaccia web è accessibile all'indirizzo [http://localhost:5000/](http://localhost:5000/)

## Esecuzione dei test
### pytest
```bash
pytest
```
### Coverage
```bash
coverage run -m pytest
coverage report -m
coverage html
```

## Docker
### Esecuzione dell'applicazione con docker-compose.yml
```bash
docker compose up --build -d
```
L'interfaccia web è accessibile all'indirizzo [http://localhost:5000/](http://localhost:5000/)