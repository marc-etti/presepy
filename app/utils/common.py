from config import Config
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
    try:
        with open(path_to_log_file, 'a') as log_file:
            log_file.write(f"{datetime.now()} - {message}\n")
            log_file.close()
    except FileNotFoundError:
        print(f"File {path_to_log_file} non trovato.")
    except Exception as e:
        print(f"Errore nella scrittura sul file di log: {str(e)}")


def write_device_info_on_json(myDevice, file_path=Config.JSON_FILE):
    """
    Scrive o aggiorna i dati di un dispositivo nel file JSON.
    
    :param myDevice: Oggetto dispositivo che deve fornire un dizionario con i suoi dati tramite un metodo `to_dict()`.
    :param file_path: Percorso del file JSON in cui scrivere i dati. Default: Config.JSON_FILE
    """
    # Assicuriamoci che il dispositivo abbia un metodo `to_dict`
    if not hasattr(myDevice, 'to_dict') or not callable(myDevice.to_dict):
        raise ValueError(f"Il dispositivo {myDevice} deve avere un metodo 'to_dict' che restituisca un dizionario dei suoi dati.")
    
    # Otteniamo i dati del dispositivo
    myDevice_data = myDevice.to_dict()
    if 'name' not in myDevice_data:
        raise ValueError(f"Errore durante la lettura di {myDevice}. Il dizionario restituito da 'to_dict' deve contenere una chiave 'name'.")
    
    # Controlla se il file esiste, altrimenti creane uno vuoto
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump({}, file)
        print(f"Il file {file_path} non esiste. Creazione di un nuovo file JSON.")

    # Leggi i dati esistenti dal file
    with open(file_path, 'r') as file:
        try:
            existing_data = json.load(file)
        except json.JSONDecodeError:
            raise ValueError(f"Errore durante la lettura di {myDevice.name}. Il file JSON non è valido.")
        
    # Trova l'indice del dispositivo se già esiste
    devices = existing_data.get("devices_info", [])
    if not isinstance(devices, list):
        raise ValueError(f"Errore durante la lettura di {myDevice.name}. Il file JSON non contiene una lista di dispositivi.")
    
    for device in devices:
        if device.get("name") == myDevice_data["name"]:
            # Aggiorna i dati esistenti
            device.update(myDevice_data)
            break
    else:
        # Aggiungi un nuovo dispositivo se non esiste
        devices.append(myDevice_data)

    # Salva i dati aggiornati sul file
    existing_data["devices_info"] = devices
    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)
        print(f"Dati di {myDevice.name} scritti sul file JSON.")


def init_device_from_json(myDevice, file_path=Config.JSON_FILE):
    """
    Inizializza un'istanza del dispositivo dai dati presenti nel file JSON.
    
    :param myDevice: Oggetto dispositivo che deve fornire un metodo `from_dict(dict)` per inizializzarsi.
    :param file_path: Percorso del file JSON da cui leggere i dati. Default: Config.JSON_FILE
    """
    # Assicuriamoci che il dispositivo abbia un metodo `from_dict`
    if not hasattr(myDevice, 'from_dict') or not callable(myDevice.from_dict):
        raise ValueError(f"Il dispositivo {myDevice} deve avere un metodo 'from_dict' per inizializzarsi da un dizionario.")
    
    # Controlla se il file esiste
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Il file {file_path} non esiste.")
    
    # Leggi i dati dal file
    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            raise ValueError(f"Il file JSON {file_path} non è valido.")
    
    devices = data.get("devices_info", [])
    if devices == []:
        # Se non ci sono dispositivi, non fare nulla
        return
    elif not isinstance(devices, list):
        raise ValueError(f"Il file JSON {file_path} non contiene una lista di dispositivi.")
    
    for device in devices:
        if device.get("name") == myDevice.name:
            myDevice.from_dict(device)
            print(f"Dispositivo {myDevice.name} inizializzato con i dati presenti nel file JSON.")
            return
    
    # Se il dispositivo non è stato trovato verrà inizializzato con i valori di default
    print(f"Il dispositivo {str(myDevice)} non è stato trovato nel file JSON.")
    
    #raise ValueError(f"Il dispositivo {str(myDevice)} non è stato trovato nel file JSON.")