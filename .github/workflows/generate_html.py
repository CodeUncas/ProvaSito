import os
import shutil
from datetime import datetime

# Directory di output dove si trovano i PDF e il file HTML
output_dir = 'output'
sitoweb_dir = 'sitoweb'

# Funzione per generare l'HTML
def generate_html():
    html_content = ""

    # Scansiona le directory per trovare i file .tex
    for root, dirs, files in os.walk('.'):
        tex_files = [f for f in files if f.endswith('.tex')]
        
        if tex_files:
            # Calcola il livello di annidamento
            level = root.count(os.sep)
            folder_name = os.path.basename(root)

            # Aggiungi intestazione appropriata in base al livello
            if level == 0:
                html_content += f"<h1>{folder_name}</h1>\n"
            elif level == 1:
                html_content += f"<h2>{folder_name}</h2>\n"
            elif level == 2:
                html_content += f"<h3>{folder_name}</h3>\n"
            else:
                html_content += f"<h4>{folder_name}</h4>\n"
                
            html_content += "<ul>\n"

            pdf_links_with_dates = []
            pdf_links_without_dates = []

            for tex_file in tex_files:
                # Crea il nome del PDF corrispondente
                pdf_file = os.path.splitext(tex_file)[0] + '.pdf'
                pdf_path = os.path.join(output_dir, pdf_file)
                
                # Controlla se il PDF esiste
                if os.path.isfile(pdf_path):
                    # Estrai la data dal nome del file
                    date_str = os.path.splitext(tex_file)[0][-10:]
                    try:
                        date = datetime.strptime(date_str, '%Y-%m-%d')
                        pdf_links_with_dates.append((pdf_file, date))
                    except ValueError:
                        pdf_links_without_dates.append(pdf_file)

            # Ordina i link per data, dal più recente al più vecchio
            pdf_links_with_dates.sort(key=lambda x: x[1], reverse=True)

            # Aggiungi i file con data
            for pdf_file, _ in pdf_links_with_dates:
                link_text = os.path.splitext(pdf_file)[0]
                html_content += f'<li><a href="{pdf_file}">{link_text}</a></li>\n'

            # Aggiungi i file senza data
            for pdf_file in pdf_links_without_dates:
                link_text = os.path.splitext(pdf_file)[0]
                html_content += f'<li><a href="{pdf_file}">{link_text}</a></li>\n'

            html_content += "</ul>\n"

    return html_content

# Funzione per copiare la cartella sitoweb
def copy_sitoweb():
    shutil.copytree(sitoweb_dir, os.path.join(output_dir, sitoweb_dir), dirs_exist_ok=True)

# Funzione per inserire contenuto nell'index.html di sitoweb
def insert_content_into_html(content):
    sitoweb_index_path = os.path.join(output_dir, sitoweb_dir, 'index.html')

    with open(sitoweb_index_path, 'r') as f:
        html_lines = f.readlines()

    # Trova il tag <main> e inserisci il contenuto
    for i, line in enumerate(html_lines):
        if '<main>' in line:
            # Trova la riga di chiusura del tag <main>
            close_main_index = i
            while '</main>' not in html_lines[close_main_index]:
                close_main_index += 1
            
            # Inserisci il contenuto prima della chiusura del tag <main>
            html_lines.insert(close_main_index, content + "\n")
            break

    with open(sitoweb_index_path, 'w') as f:
        f.writelines(html_lines)

# Assicurati che la cartella output esista
os.makedirs(output_dir, exist_ok=True)

# Copia la cartella sitoweb nella cartella output
copy_sitoweb()

# Genera il contenuto HTML
html_output = generate_html()

# Inserisci il contenuto nel file index.html di sitoweb
insert_content_into_html(html_output)

print("HTML index created successfully in the 'output' directory.")
