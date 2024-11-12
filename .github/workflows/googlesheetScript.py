import os
from googleapiclient.discovery 
import build
from google.auth.transport.requests 
import Request



# Funzione per costruire il servizio Google Sheets
def build_sheets_service(key):
    service = build('sheets', 'v4', developerKey=key)
    return service

# Funzione per aggiornare il numero di ore
def update_hours(service, spreadsheet_id, nome, ruolo, ore):
    try:
        # Ottieni i dati dal foglio
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range="Foglio1!A1:Z1000").execute()
        values = result.get('values', [])

        # Trova la riga corrispondente al nome
        for i, row in enumerate(values):
            if row and row[0] == nome:  # La prima colonna contiene i nomi
                # Trova la colonna corrispondente al ruolo
                for j, cell in enumerate(row[1:], start=1):  # Inizia dalla seconda colonna
                    if cell == ruolo:  # Supponiamo che il ruolo sia un valore nelle colonne successive
                        # Aggiorna il valore nella cella (i, j)
                        update_range = f"Foglio1!{chr(65 + j)}{i + 1}"  # Calcola la cella di destinazione
                        body = {
                            'values': [[ore]]
                        }
                        sheet.values().update(spreadsheetId=spreadsheet_id, range=update_range, body=body, valueInputOption="RAW").execute()
                        print(f"Ora aggiornate con successo per {nome} nel ruolo di {ruolo}: {ore} ore.")
                        return
        print(f"Nome o ruolo non trovati nel foglio.")
        
    except Exception as e:
        print(f"Errore nell'aggiornamento del foglio: {e}")

