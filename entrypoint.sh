#!/bin/bash

# Script per l'avvio dell'applicazione Flask in Docker

# Controlla se il database in ./instance/presepy.sqlite esiste
if [ ! -f "/usr/src/presepy/instance/presepy.sqlite" ]; then
    echo "Database non trovato."
    echo "Creando il database..."
    flask init-db
    echo "Database creato."
else
    echo "Database trovato."
fi

# Esegui l'app Flask
python3 run.py