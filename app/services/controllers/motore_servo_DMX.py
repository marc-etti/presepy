from app.utils.crib_linea import CribLinea

class MotoreServoDMX:
    def __init__(self):
        self.r_escursione_massima = 0.0                 # numero di gradi dell'escursione del servo
        self.i_dmx_addr = 0                             # indirizzo DMX del servo
        self.i_pos_dmx_prec = 0                         # posizione precedente in infinitesimi del motore
        self.i_pos_attuale = 0                          # 0-255 posizione istantanea del motore
        self.i_pos_dmx_prevista = 0                     # Posizione DMX del servo alla fine della movimentazione
        self.i_stato_motore = 0                         # stato di movimentazione (dipende dall'applicazione)
        self.i_stato_motore_prec = 0
        self.i_pausa_stato_motore = [0] * 601
        self.i_pausa_stato_motore_uscita = [0] * 601
        self.i_stato_fine_mov = [0] * 601
        self.r_stato_quota = [0.0] * 601
        self.i_attesa_ev_prof13 = [0] * 601         # quale fase prof13 è associato l'ev di attesa
        self.b_logic_attesa = [0] * 601             # se c'è una condizione logica da memorizzare
        self.r_gradi_motore = 0.0                   # gradi previsti del motore
        self.r_gradi_quota = 0.0                    # gradi di riferimento secondo movimento
        self.r_delta_pos = 0.0                      # incremento infinitesimale di manovra
        self.i_num_cicli_totali = 0                 # numero di cicli di tick timer per eseguire la movimentazione
        self.i_num_cicli_attuali = 0                # numero di cicli fatti
        self.i_num_cicli_attesa = 0                 # numero di cicli di attesa
        self.i_durata_profilo = 0                   # durata del ciclo [s]
        self.i_cont_motore = 0                      # variabile di servizio x calcolo ritardi automa
        self.i_cont_max_azzurro = 0
        self.i_form_num_contr = 0                   # numero del form di controllo
        self.r_max_gradi_movimento = 0.0            # gradi massimi di estensione del movimento del motore
        self.r_gradi_precedente = 0.0               # posizione precedente del motore
        self.b_modo_esecuzione = 0                  # specifica in che modo è azionato il motore 0 manualmente 1 auto(presepe)
        self.b_prima_volta = 1                      # flag di servizio x istruzioni di movimento (es. prima volta che si esegue...)
        self.b_muovi_rnd = 0.0                      # True: al tot% dei gradi programmati, metti una componente casuale
        self.sg_servo_pos_gradi = ""                # prompt di servizio x form (pos stimata in gradi del servo)
        #   'sgServoPosDMX As String * 10   'prompt di servizio x form (pos stimata in codici DMX)
        #   'sgServoPosDMX(300) As String   'prompt di servizio x form (pos stimata in codici DMX)
        self.sg_servo_pos_gradi_dsp = [""] * 256
        self.r_pos_attuale = [0.0] * 256
        self.r_escursione_max_cicli = 0.0
        self.r_255_div_escursione_massima = 0.0
        self.sg_nome_ini_servo_dmx = ""             # identificativo del motore servo
        self.retta_motore = CribLinea()           # per calcolo delle traiettorie rettilinee
        self.b_is_on_frm_diagno_luci = False        # il motore è gestito come grafica su frmdiagnoluci
    