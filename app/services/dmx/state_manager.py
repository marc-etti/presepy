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
            self.isOn = False
            self.current_phase = 'inizializzazione'

    def is_on(self):
        """Restituisce True se il sistema è acceso, False altrimenti."""
        return self.isOn
    
    def turn_on(self):
        """Accende il sistema."""
        if not self.isOn:
            self.isOn = True
        else:
            print("Il sistema è già acceso.")

    def turn_off(self):
        """Spegne il sistema."""
        if self.isOn:
            self.isOn = False
        else:
            print("Il sistema è già spento.")

    def set_phase(self, phase):
        """Imposta la fase del giorno corrente."""
        self.current_phase = phase

    def get_phase(self):
        """Restituisce la fase del giorno corrente."""
        return self.current_phase
    
    #TODO: Implementare il meteo quando sarà possibile