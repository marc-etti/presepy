# File della classe DMX

from datetime import datetime
import threading

NUMBER_OF_CHANNELS = 512
MAX_CHANNEL_VALUE = 255

class DMXData:
    """
    Classe che gestisce i dati DMX.
    Il protocollo DMX prevede la trasmissione di 512 canali
    (513 canali in totale ma il canale 0 viene tenuto a 0)
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """
        Metodo per creare un'istanza singola della classe.
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:  # Doppio controllo per la sicurezza con thread multipli.
                    cls._instance = super(DMXData, cls).__new__(cls, *args, **kwargs)
        return cls._instance 

    def __init__(self):
        """
        Costruttore della classe.
        """
        if not hasattr(self, 'channels'):  # Per evitare di sovrascrivere l'istanza esistente.
            self.channels = [0] * (NUMBER_OF_CHANNELS + 1)

        
    def set_channel(self, channel, value):
        """
        Imposta il valore di un canale DMX.

        :param channel: il numero del canale da impostare
        :param value: il valore da impostare
        """
        if channel < 1 or channel > 512:
            raise ValueError("Il canale deve essere compreso tra 1 e 512")
        if value < 0 or value > 255:
            raise ValueError("Il valore deve essere compreso tra 0 e 255")
        self.channels[channel] = value
    
    def reset(self):
        """
        Resetta tutti i canali DMX.
        """
        for i in range(1, NUMBER_OF_CHANNELS + 1):
            self.channels[i] = 0

    def open(self):
        """
        Apre la connessione DMX.
        """
        #TODO: implementare l'apertura della connessione DMX'
        raise NotImplementedError("Metodo non implementato")

    def send(self, host, port):
        """
        Invia i valori dei canali DMX alla porta specificata.
        """
        #TODO: implementare la connessione DMX
        raise NotImplementedError("Metodo non implementato")

    def close(self):
        """
        Chiude la connessione DMX.
        """
        #TODO: implementare la chiusura della connessione DMX
        raise NotImplementedError("Metodo non implementato")


    def write_channels_on_log(self, log_file):
        """
        Scrive i valori dei canali DMX su file di log.
        """
        if not log_file:
            raise ValueError("Il file di log non è stato specificato")
        
        with open(log_file, 'a') as f:
            f.write(f'{datetime.now().strftime("%H:%M:%S")}: {self.channels}\n')

    def write_channels_on_console(self):
        """
        Stampa i valori dei canali DMX su console.
        """
        print(self.channels)

    def clear_log_file(self, log_file):
        """
        Pulisce il file di log.
        """
        if not log_file:
            raise ValueError("Il file di log non è stato specificato")
        
        with open(log_file, 'w') as f:
            f.write('')