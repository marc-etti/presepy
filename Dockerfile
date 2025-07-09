# Usa un'immagine Python ufficiale
FROM python:3.13-alpine

# Imposta la directory di lavoro
WORKDIR /usr/src/presepy

# Copia i file necessari
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# volume per il database
VOLUME /usr/src/presepy/instance/

# Copia il resto del codice sorgente
COPY . .

# Espone la porta 5000
EXPOSE 5000

# Comando per avviare l'applicazione
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["sh", "/entrypoint.sh"]