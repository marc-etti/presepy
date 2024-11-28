import json
import os

class jsonFileManager:
    def __init__(self, file_name=None):
        """
        Inizializza il gestore del file JSON.
        :param file_name: Nome del file JSON.
        """
        self.file_name = file_name
        self.data = {}
        if self.file_name and os.path.exists(self.file_name):
            self._load()

    def _load(self):
        """Carica il contenuto del file JSON."""
        with open(self.file_name, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    def _save(self):
        """Salva il contenuto nel file JSON."""
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4)

    def set_file_name(self, file_name):
        """
        Imposta il nome del file JSON e lo carica se esiste.
        :param file_name: Nome del file JSON.
        """
        self.file_name = file_name
        if os.path.exists(file_name):
            self._load()
        else:
            self.data = {}

    def get_value(self, section, key, default=None):
        """
        Ottiene il valore di una chiave all'interno di una sezione.
        :param section: Sezione del file JSON.
        :param key: Chiave da leggere.
        :param default: Valore predefinito se la chiave non esiste.
        :return: Valore della chiave o il valore predefinito.
        """
        return self.data.get(section, {}).get(key, default)

    def set_value(self, section, key, value):
        """
        Imposta il valore di una chiave all'interno di una sezione.
        :param section: Sezione del file JSON.
        :param key: Chiave da impostare.
        :param value: Valore da assegnare alla chiave.
        """
        if section not in self.data:
            self.data[section] = {}
        self.data[section][key] = value
        self._save()

    def get_section(self, section):
        """
        Restituisce l'intera sezione come dizionario.
        :param section: Nome della sezione.
        :return: Dizionario contenente i valori della sezione o un dizionario vuoto.
        """
        return self.data.get(section, {})

    def set_section(self, section, values):
        """
        Imposta una sezione con un dizionario di valori.
        :param section: Nome della sezione.
        :param values: Dizionario dei valori da impostare.
        """
        self.data[section] = values
        self._save()