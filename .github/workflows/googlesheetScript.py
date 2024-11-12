import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request



# Funzione per costruire il servizio Google Sheets
def build_sheets_service(key):
    service = build('sheets', 'v4', developerKey=key)
    return service

# Funzione per aggiornare il numero di ore
def update_hours(service, spreadsheet_id, nome, ruolo, ore):
    try:
        # Intervallo da leggere dal foglio
        range_ = "Foglio1!B3:I10"  # Modifica l'intervallo se necessario

        # Ottieni i dati dal foglio
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_).execute()
        values = result.get('values', [])

        # Stampa i dati letti dal foglio per il debug
        print("Dati letti dal foglio:")
        for row in values:
            print(row)

        
        # Trova la riga corrispondente al nome
        for i, row in enumerate(values):
            # La prima colonna (index 0) ora contiene i nomi
            if row and row[0].strip().lower() == nome.strip().lower():  # Normalizza il nome
                print(f"Nome trovato: {row[0]}")  # Debug per verificare se il nome è stato trovato
                # Trova la colonna corrispondente al ruolo
                for j, cell in enumerate(row[1:], start=1):  # Le colonne da B a H (ruolo1 a ruolo7)
                    print(cell.strip())
                    if cell.strip().lower() == ruolo.strip().lower():  # Normalizza il ruolo
                        print(f"Ruolo trovato: {cell}")  # Debug per verificare se il ruolo è stato trovato
                        # Aggiorna il valore nella cella (i, j)
                        update_range = f"Foglio1!{chr(65 + j)}{i + 2}"  # Calcola la cella da aggiornare (aggiungiamo 2 per saltare l'intestazione)
                        body = {
                            'values': [[ore]]
                        }
                        sheet.values().update(spreadsheetId=spreadsheet_id, range=update_range, body=body, valueInputOption="RAW").execute()
                        print(f"Ora aggiornate con successo per {nome} nel ruolo di {ruolo}: {ore} ore.")
                        return
        print(f"Nome o ruolo non trovati nel foglio.")
        
    except Exception as e:
        print(f"Errore nell'aggiornamento del foglio: {e}")
        
    except Exception as e:
        print(f"Errore nell'aggiornamento del foglio: {e}")

