from app.utils.common import calcola_m_retta

class CribLinea:
    def __init__(self):
        self.bmSteep = False  # Modella se la linea è inclinata o a picco
        self.imDeltaX = 0
        self.imDeltaY = 0
        self.imDeltaX2 = 0
        self.imDeltaY2 = 0
        self.imDelta = 0
        self.imStepY = 0
        self.imCoord = 0
        self.imInitialX = 0
        self.imInitialY = 0
        self.imFinalY = 0
        self.rm_m = 0.0
        self.rm_q = 0.0
        self.imDummy = 0

    # inizializzazione della linea DMX
    # invocare il metodo prima dell'effettivo tracciamento dei valori
    # OKKIO! da usare SOLO se le ordinate da calcolare sono valori DMX
    # iLimit: limite di protezione a seconda della bisogna

    def set_crib_linea(self, iInitialX, iInitialY, iFinalX, iFinalY, iLimit):
        self.imInitialY = self.is_dmx(iInitialY, iLimit)
        self.imFinalY = self.is_dmx(iFinalY, iLimit)
        self.imDeltaX = abs(iFinalX - iInitialX)
        self.imDeltaY = abs(self.imFinalY - self.imInitialY)

        if self.imDeltaY > self.imDeltaX:  # Linea più inclinata di 45°
            self.rm_m = self.calcola_m_retta(iInitialX, self.imInitialY, iFinalX, self.imFinalY)
            self.rm_q = self.imInitialY - self.rm_m * iInitialX
            self.imInitialX = iInitialX
            self.bmSteep = True
        else:
            self.bmSteep = False
            self.imDeltaX2 = 2 * self.imDeltaX
            self.imDeltaY2 = 2 * self.imDeltaY
            self.imStepY = 1 if (self.imFinalY - self.imInitialY) > 0 else -1
            self.imDelta = self.imDeltaY2 - self.imDeltaX

        self.imCoord = 0

    # Restituisce il valore in ordinata della linea virtuale
    # serve x le transizioni a decadimento/accrescimento lineare    

    def cal_crib_linea(self):
        if self.imCoord == 373:
            self.imDummy = 373

        if 0 <= self.imCoord < self.imDeltaX - 1:
            if self.bmSteep:
                self.imInitialY = self.rm_m * (self.imInitialX + self.imCoord) + self.rm_q
            else:
                while self.imDelta >= 0:
                    self.imInitialY += self.imStepY
                    self.imDelta -= self.imDeltaX2
                self.imDelta += self.imDeltaY2

            self.imCoord += 1
        else:
            self.imInitialY = self.imFinalY

        return self.imInitialY

    # verifica che le coordinate siano comprese tra 0 e 255
    # funzione anti inculata
    # iVal valore da controllare
    # Private Function IsDmx(ByRef iVal As Long) As Long
    
    @staticmethod
    def is_dmx(iVal, iMaxVal):
        if iVal < 0:
            return 0
        elif iVal > iMaxVal:
            return iMaxVal
        return iVal

