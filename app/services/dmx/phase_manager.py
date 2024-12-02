class PhaseManager:
    """Classe per la gestione delle fasi del giorno."""
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PhaseManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'current_phase'):
            self.current_phase = 'inizializzazione'

    def set_phase(self, phase):
        self.current_phase = phase

    def get_phase(self):
        return self.current_phase
    
    #TODO: Implementare il meteo quando sarà possibile