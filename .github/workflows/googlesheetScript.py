import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def build_sheets_service():
    # Recupera il percorso del file JSON contenente le credenziali
    #credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    
    #if not credentials_path:
       # raise ValueError("La variabile d'ambiente 'GOOGLE_APPLICATION_CREDENTIALS' non è definita.")
    with open('/tmp/google-credentials.json', 'r') as file:
        data = json.load(file)

    # Stampa il JSON in una sola riga
    print(json.dumps(data))
    # Carica le credenziali direttamente dal file
    credentials = Credentials.from_service_account_file(
        '/tmp/google-credentials.json', 
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    # Costruisci il servizio per Google Sheets
    service = build('sheets', 'v4', credentials=credentials)
    return service
def update_hours(service, spreadsheet_id, nome, ruolo, ore):
    try:
        # Intervallo da leggere dal foglio (completo)
        range_ = "Foglio1!B3:I10"  # Modifica l'intervallo se necessario

        # Ottieni i dati dal foglio
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_).execute()
        values = result.get('values', [])

        # Stampa i dati letti dal foglio per il debug
        print("Dati letti dal foglio:")
        for row in values:
            print(row)

        # La prima riga (index 0) contiene le intestazioni dei ruoli
        headers = values[0]  # Prima riga è l'intestazione dei ruoli

        # Trova la colonna corrispondente al ruolo
        role_column = None
        for j, header in enumerate(headers):
            print(header)
            if header.strip().lower() == ruolo.strip().lower():
                role_column = j  # Memorizza l'indice della colonna corrispondente al ruolo
                break
        
        if role_column is None:
            print(f"Ruolo '{ruolo}' non trovato.")
            return

        # Trova la riga corrispondente al nome
        for i, row in enumerate(values[1:], start=1):  # Inizia dalla seconda riga (index 1)
            if row and row[0].strip().lower() == nome.strip().lower():  # Normalizza il nome
                print(f"Nome trovato: {row[0]}")  # Debug per verificare se il nome è stato trovato
                
                # Calcola l'intervallo per aggiornare la cella corrispondente
                # La colonna per il ruolo è `role_column` e la riga è `i + 3` (perché l'intervallo inizia dalla riga 3)
                update_range = f"Foglio1!{chr(65 + role_column + 1)}{i + 3}"  # +1 perché il range inizia da B, non A, e +3 per offset della riga

                body = {
                    'values': [[ore]]
                }

                # Esegui l'aggiornamento nella cella corretta
                sheet.values().update(spreadsheetId=spreadsheet_id, range=update_range, body=body, valueInputOption="RAW").execute()
                print(f"Ora aggiornate con successo per {nome} nel ruolo di {ruolo}: {ore} ore.")
                return
        
        print(f"Nome '{nome}' non trovato nel foglio.")

    except Exception as e:
        print(f"Errore nell'aggiornamento del foglio: {e}")

