import os, json
from config import Config
from threading import Event

class StateManager:
    """Classe per la gestione dello stato del sistema."""
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Metodo per creare un'istanza singola della classe."""
        if not cls._instance:
            cls._instance = super(StateManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """Costruttore della classe."""
        if not hasattr(self, 'current_phase'):
            self.pause_event = None
            self.isOn = False
            self.current_phase = 'inizializzazione'
            self.istante = 0

    def is_on(self) -> bool:
        """Restituisce True se il sistema è acceso, False altrimenti."""
        return self.isOn
    
    def turn_on(self):
        """Accende il sistema."""
        if self.isOn:
            print("Il sistema è già acceso.")
        else:
            self.isOn = True
            if not self.pause_event.is_set():
                self.pause_event.set()

    def turn_off(self):
        """Spegne il sistema.
           se il sistema è acceso e in pausa, lo spegne e toglie la pausa."""
        if self.isOn:
            if not self.pause_event.is_set():
                self.pause_event.set()
            self.isOn = False
        else:
            print("Il sistema è già spento.")

    def set_phase(self, phase):
        """Imposta la fase del giorno corrente."""
        self.current_phase = phase

    def get_phase(self):
        """Restituisce la fase del giorno corrente."""
        return self.current_phase
    
    def set_istante(self, istante):
        """Salva l'istante corrente."""
        self.istante = istante

    def get_istante(self):
        """Restituisce l'istante salvato."""
        return self.istante
    
    def set_paused_event(self, event: Event):
        """Imposta l'evento di pausa.
           param event: Evento di pausa."""
        self.pause_event = event
        self.pause_event.set()
    
    def pause(self):
        """Mette in pausa il sistema.
           Se il flag è True lo imposta a False, altrimenti dice che il sistema è già in pausa."""
        if self.pause_event.is_set():
            self.pause_event.clear()
        else:
            print("Il sistema è già in pausa.")

    def resume(self):
        """Riprende il sistema dalla pausa.
           Se il flag è False lo imposta a True, altrimenti dice che il sistema non è in pausa."""
        if not self.pause_event.is_set():
            self.pause_event.set()
        else:
            print("Il sistema non è in pausa.")