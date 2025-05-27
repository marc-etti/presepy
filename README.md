# Presepy - Gestione di un presepe elettronico
Presepy è un'applicazione web per la gestione di un presepe elettronico, sviluppata in Python utilizzando il framework Flask. L'applicazione attualmente consente la gestione di dispositivi di illuminazione pilotabili tramite protocollo DMX512.
Le funzionalità principali includono:
- Creazione, modifica e cancellazione di dispositivi
- Creazione, modifica e cancellazione di keyframe
- Avvio, pausa e stop della trasmissione dei dati DMX (simulata con una scrittura su file di log)

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

## Inizializzazione database
Per inizializzare il database, è necessario eseguire il comando di inizializzazione del database.
```bash
flask init-db
```

## Accesso all'interfaccia web
L'interfaccia web è accessibile all'indirizzo [http://localhost:5000/](http://localhost:5000/).

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

## Avvio dell'applicazione con Docker

### Build dell'immagine
```bash
docker build -t andreamarchetti/presepy:1.0 .
```
### Push dell'immagine
```bash
docker push andreamarchetti/presepy:1.0
```
### Pull dell'immagine
```bash
docker pull andreamarchetti/presepy:1.0
```
### Esecuzione dell'immagine
```bash
docker run -p 5000:5000 andreamarchetti/presepy:1.0
```