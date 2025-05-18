#!/bin/bash

# Script per l'avvio dell'applicazione Flask

# Controlla se l'ambiente virtuale esiste
if [ ! -d "venv" ]; then
    echo "Ambiente virtuale non trovato."
    echo "Creando un nuovo ambiente virtuale..."
    python3 -m venv venv
    echo "Ambiente virtuale creato."
    echo "Attivando l'ambiente virtuale..."
    source venv/bin/activate
    echo "Installando le dipendenze..."
    pip install -r requirements.txt
    echo "Dipendenze installate."
else
    echo "Ambiente virtuale trovato."
    echo "Attivando l'ambiente virtuale..."
    source venv/bin/activate
    echo "Ambiente virtuale attivato."
fi

# Controlla se il database in ./instance/presepy.sqlite esiste
if [ ! -f "./instance/presepy.sqlite" ]; then
    echo "Database non trovato."
    echo "Creando il database..."
    flask init-db
    echo "Database creato."
else
    echo "Database trovato."
fi

# Esegui l'app Flask
python3 run.py
