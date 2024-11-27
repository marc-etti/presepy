# File della classe DMX

from datetime import datetime

NUMBER_OF_CHANNELS = 512
MAX_CHANNEL_VALUE = 255

class DMX:
    """
    Classe che rappresenta un'interfaccia DMX.
    Permette di inviare valori a 512 canali DMX.
    """

    def __init__(self):
        """
        Costruttore della classe.
        """
        self.channels = [0] * NUMBER_OF_CHANNELS

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
        self.channels[channel - 1] = value

    def set_interval(self, start_channel, end_channel, value):
        """
        Imposta lo stesso valore a più canali DMX.

        :param start_channel: il primo canale da impostare
        :param end_channel: l'ultimo canale da impostare
        :param value: il valore da impostare
        """
        if start_channel < 1 or start_channel > 512:
            raise ValueError("Il canale iniziale deve essere compreso tra 1 e 512")
        if end_channel < 1 or end_channel > 512:
            raise ValueError("Il canale finale deve essere compreso tra 1 e 512")
        if start_channel > end_channel:
            raise ValueError("Il canale iniziale deve essere minore o uguale al canale finale")
        if value < 0 or value > 255:
            raise ValueError("Il valore deve essere compreso tra 0 e 255")
        for i in range(start_channel, end_channel + 1):
            self.channels[i - 1] = value

    def get_channel(self, channel):
        """
        Restituisce il valore di un canale DMX.

        :param channel: il numero del canale da leggere
        :return: il valore del canale
        """
        if channel < 1 or channel > 512:
            raise ValueError("Il canale deve essere compreso tra 1 e 512")
        return self.channels[channel - 1]
    
    def get_channels(self):
        """
        Restituisce i valori di tutti i canali DMX.

        :return: i valori dei canali
        """
        return self.channels
    
    def reset(self):
        """
        Resetta tutti i canali DMX.
        """
        for i in range(512):
            self.channels[i] = 0

    def send(self, host, port):
        """
        Invia i valori dei canali DMX alla porta specificata.
        """
        pass

    def write_channels_on_log(self, log_file):
        """
        Scrive i valori dei canali DMX su file di log.
        """
        with open(log_file, 'a') as f:
            f.write(f'{datetime.now().strftime("%H:%M:%S")}: {self.channels}\n')

    def write_channels_on_console(self):
        """
        Stampa i valori dei canali DMX su console.
        """
        print(self.channels)