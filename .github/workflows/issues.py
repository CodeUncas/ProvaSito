import requests
import json
import os
from googlesheetScript import *


issue_number = os.getenv('ISSUE_NUMBER')
token = os.getenv('PYTHON_TOKEN')
urlGithubIssue =  f'https://api.github.com/repos/CodeUncas/ProvaSito/issues/{issue_number}'

# SECONDO PROCESSO
SPREADSHEET_ID = 'https://docs.google.com/spreadsheets/d/1xmtRTVE1byAcSEzIK11N_ePO2ruVTPVJaMGrDqfBcaQ/edit?gid=0#gid=0'  # Inserisci l'ID del tuo foglio di calcolo
SHEETS_KEY = os.getenv('SHEETS_TOKEN')  # Inserisci la tua API Key
############

# https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28"

}
def getIssueDetails(urlParam,headerParam):
    response = requests.get(urlParam,headers=headerParam)

    JsonResponse = response.json();
    
    dictWithInfo = {
        'TitoloIssue' : JsonResponse['title'],
        'DescrizioneIssue' : JsonResponse['body'],
        'AssigneeIssue' : JsonResponse['assignees'][0]['login'],
        'LabelIssue' : JsonResponse['labels'][0]['name']
    }
    return dictWithInfo

def main():
    finalDictionary = getIssueDetails(urlGithubIssue,headers)
    service = build_sheets_service(SHEETS_KEY)
    
    # Esegui l'aggiornamento
    update_hours(service, SPREADSHEET_ID, finalDictionary['AssigneeIssue'], finalDictionary['DescrizioneIssue'], 2 )

if __name__ == '__main__':
    main()