from datetime import datetime
import os
import json

def calcola_m_retta(x1, y1, x2, y2):
    if x1 != x2:
        return (y2 - y1) / (x2 - x1)
    else:
        return 1

def write_on_log(message, path_to_log_file):
    """Scrive un messaggio sul file di log."""
    with open(path_to_log_file, 'a') as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")
        log_file.close()

