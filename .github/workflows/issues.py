import requests
import json
import os


issue_number = os.getenv('ISSUE_NUMBER')
token = os.getenv('PYTHON_TOKEN')
urlGithubIssue =  'https://api.github.com/repos/CodeUncas/ProvaSito/issues/{issue_number}'

# https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28"

}

response = requests.get(urlGithubIssue,headers=headers)

JsonResponse = response.json();

TitoloIssue = JsonResponse['title']
DescrizioneIssue = JsonResponse['body']
AssigneeIssue = JsonResponse['assignees'][0]['login']
LabelIssue = JsonResponse['labels'][0]['name']

print(TitoloIssue + "\n" + DescrizioneIssue + "\n" + AssigneeIssue + "\n" + "LabelIssue");
