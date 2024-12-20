import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

def build_sheets_service():
    # Percorso del file delle credenziali
    credentials_path = os.path.join(os.getenv('GITHUB_WORKSPACE'), '.github', 'workflows', 'jcredentials.json')

    # Carica le credenziali direttamente dal file
    credentials = service_account.Credentials.from_service_account_file(
        filename=credentials_path
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
                
                # Calcola l'intervallo per leggere la cella corrispondente
                # La colonna per il ruolo è `role_column` e la riga è `i + 3` (perché l'intervallo inizia dalla riga 3)
                read_range = f"Foglio1!{chr(65 + role_column + 1)}{i + 3}"  # +1 per l'indice della colonna, +3 per l'offset delle righe

                # Ottieni il valore corrente nella cella (ore già inserite)
                current_value_result = sheet.values().get(spreadsheetId=spreadsheet_id, range=read_range).execute()
                current_value = current_value_result.get('values', [[]])[0][0] if current_value_result.get('values') else '0'

                # Converte il valore attuale in un numero (se è vuoto o non valido, usa 0)
                try:
                    current_hours = float(current_value)
                except ValueError:
                    current_hours = 0.0  # Se il valore corrente non è un numero, consideralo come 0

                # Somma le ore attuali con le nuove ore
                new_hours = current_hours + ore

                # Prepara il corpo per l'aggiornamento
                body = {
                    'values': [[new_hours]]
                }

                # Calcola l'intervallo per aggiornare la cella corrispondente
                update_range = f"Foglio1!{chr(65 + role_column + 1)}{i + 3}"

                # Esegui l'aggiornamento con la somma delle ore
                sheet.values().update(spreadsheetId=spreadsheet_id, range=update_range, body=body, valueInputOption="RAW").execute()
                print(f"Ora aggiornate con successo per {nome} nel ruolo di {ruolo}: {new_hours} ore.")
                return
        
        print(f"Nome '{nome}' non trovato nel foglio.")

    except Exception as e:
        print(f"Errore nell'aggiornamento del foglio: {e}")

