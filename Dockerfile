# Usa un'immagine Python ufficiale
FROM python:3.10-slim

# Imposta la directory di lavoro
WORKDIR /usr/src/app

# Copia i file necessari
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# volume per il database
VOLUME /usr/src/app/instance/

# Copia il resto del codice sorgente
COPY . .

# Espone la porta 5000
EXPOSE 5000

# Comando per avviare l'applicazione
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]