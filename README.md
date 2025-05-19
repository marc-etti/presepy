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

# Inizializzazione database
Per inizializzare il database, è necessario eseguire il comando di inizializzazione del database.

```bash
flask init-db
```

## Accesso all'interfaccia web

L'interfaccia web è accessibile all'indirizzo [http://localhost:5000/](http://localhost:5000/).

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