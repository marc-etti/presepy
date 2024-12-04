#!/bin/bash

# Script per l'avvio dell'applicazione Flask
# Lo script si aspetta di essere eseguito nella cartella del progetto
# e che l'ambiente virtuale sia già stato creato

# Attiva l'ambiente virtuale
source venv/bin/activate

# Esegui l'app Flask
python3 run.py &

# Aspetta un momento per assicurarti che il server sia avviato
sleep 2

# Apri il browser all'indirizzo localhost:5000
google-chrome http://localhost:5000
