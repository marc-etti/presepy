def calcola_m_retta(x1, y1, x2, y2):
    if x1 != x2:
        return (y2 - y1) / (x2 - x1)
    else:
        return 1
