import os
import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Funzione per costruire il servizio Google Sheets con OAuth 2.0
def build_sheets_service(credentials_file):
    creds = None
    # Il file token.pickle memorizza l'accesso e il refresh token dell'utente.
    # Se esiste, carica i credenziali salvate
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Se non ci sono (o sono scadute) credenziali, chiedi all'utente di autenticarsi
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            # Usa il file credentials.json scaricato dal Google Cloud Console
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, ['https://www.googleapis.com/auth/spreadsheets']
            )
            creds = flow.run_local_server(port=0)
        # Salva le credenziali per il prossimo utilizzo
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Crea il servizio Sheets con le credenziali OAuth
    service = build('sheets', 'v4', credentials=creds)
    return service

# Funzione per aggiornare il numero di ore
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
                # Aggiorna il valore nella cella corrispondente a nome e ruolo
                update_range = f"Foglio1!{chr(65 + role_column)}{i + 1}"  # Calcola la cella da aggiornare
                body = {
                    'values': [[ore]]
                }
                sheet.values().update(spreadsheetId=spreadsheet_id, range=update_range, body=body, valueInputOption="RAW").execute()
                print(f"Ora aggiornate con successo per {nome} nel ruolo di {ruolo}: {ore} ore.")
                return
        
        print(f"Nome '{nome}' non trovato nel foglio.")

    except Exception as e:
        print(f"Errore nell'aggiornamento del foglio: {e}")
