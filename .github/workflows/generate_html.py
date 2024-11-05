
import os
import shutil
from datetime import datetime

# Directory di output dove si trovano i PDF e il file HTML
output_dir = 'output'
sitoweb_dir = 'sitoweb'  # Percorso della cartella 'sitoweb' nella root del repository
# Funzione per generare l'HTML
def generate_html():
    html_content = ""

    # Scansiona le directory per trovare i file .tex, ma ignorando la root
    for root, dirs, files in os.walk('.'):
        # Ignora la directory root
        if root == '.':
            continue
        
        dirs.sort()

        tex_files = [f for f in files if f.endswith('.tex')]
        subdirs_with_tex = []  # Per tenere traccia delle sottodirectory che contengono file .tex

        # Verifica se ci sono file .tex in questa directory
        if tex_files:
            subdirs_with_tex.append(root)

        # Controlla le sottodirectory per file .tex
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            for subroot, _, subfiles in os.walk(subdir_path):
                if any(f.endswith('.tex') for f in subfiles):
                    subdirs_with_tex.append(root)
                    break  # Una volta trovato un file .tex, non è necessario continuare

        # Se la directory (o una sua sottodirectory) contiene file .tex
        if subdirs_with_tex:
            # Calcola il livello di annidamento
            level = root.count(os.sep) - 1
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

            # Se ci sono file .tex, li elenchiamo
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

# Funzione per copiare i file da sitoweb a output
def copy_sitoweb_files():
    for item in os.listdir(sitoweb_dir):
        src = os.path.join(sitoweb_dir, item)
        dst = os.path.join(output_dir, item)

        # Sovrascrive i file esistenti senza errori
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)  # Sovrascrive la directory
        else:
            shutil.copy2(src, dst)  # Sovrascrive il file


# Funzione per inserire contenuto nell'index.html di sitoweb
def insert_content_into_html(content):
    sitoweb_index_path = os.path.join(output_dir, 'index.html')  # File index.html in output

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

    # Scrive nuovamente il file HTML
    with open(sitoweb_index_path, 'w') as f:
        f.writelines(html_lines)

# Assicurati che la cartella output esista
os.makedirs(output_dir, exist_ok=True)

# Copia i file da sitoweb nella cartella output
copy_sitoweb_files()

# Genera il contenuto HTML
html_output = generate_html()

# Inserisci il contenuto nel file index.html di sitoweb
insert_content_into_html(html_output)

print("HTML index created successfully in the 'output' directory.")
