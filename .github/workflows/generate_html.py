import os
import requests

# Ottieni il nome della repository dalla directory corrente
repo = os.path.basename(os.getcwd())  # Nome della directory corrente
owner = 'username'  # Sostituisci con il tuo username su GitHub
url = f'https://api.github.com/repos/{owner}/{repo}/contents'

# Funzione per ottenere i file e le directory
def fetch_contents(path=''):
    response = requests.get(f'{url}/{path}')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching contents: {response.status_code}")
        return []

# Funzione per generare l'HTML
def generate_html(contents):
    html_content = "<html><body>\n"
    for item in contents:
        if item['type'] == 'dir':
            html_content += f"<h1>{item['name']}</h1>\n"
            sub_contents = fetch_contents(item['path'])
            html_content += "<ul>\n"
            for sub_item in sub_contents:
                if sub_item['type'] == 'file' and sub_item['name'].endswith('.pdf'):
                    html_content += f'<li><a href="{sub_item["download_url"]}">{sub_item["name"]}</a></li>\n'
            html_content += "</ul>\n"
    html_content += "</body></html>\n"
    return html_content

# Ottieni i contenuti dalla root del repository
contents = fetch_contents()
html_output = generate_html(contents)

# Scrivi il file HTML
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)  # Crea la directory output se non esiste
with open(os.path.join(output_dir, 'index.html'), 'w') as f:
    f.write(html_output)

print("HTML index created successfully.")
