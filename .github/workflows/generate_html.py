import os
from datetime import datetime

# Funzione per generare l'HTML
def generate_html():
    html_content = ""

    # Scansiona le directory per trovare i file .tex
    for root, dirs, files in os.walk('.'):
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
