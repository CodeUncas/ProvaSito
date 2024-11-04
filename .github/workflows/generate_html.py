import os

# Directory di output dove si trovano i PDF e il file HTML
output_dir = 'output'

# Funzione per generare l'HTML
def generate_html():
    html_content = "<html><body>\n"

    # Scansiona le directory per trovare i file .tex
    for root, dirs, files in os.walk('.'):
        tex_files = [f for f in files if f.endswith('.tex')]
        if tex_files:
            # Ottieni il nome della cartella corrente
            folder_name = os.path.basename(root)
            html_content += f"<h1>{folder_name}</h1>\n"
            html_content += "<ul>\n"
            
            for tex_file in tex_files:
                # Crea il nome del PDF corrispondente
                pdf_file = os.path.splitext(tex_file)[0] + '.pdf'
                pdf_path = os.path.join(output_dir, pdf_file)
                
                # Controlla se il PDF esiste
                if os.path.isfile(pdf_path):
                    # Link senza l'estensione .pdf
                    link_text = os.path.splitext(pdf_file)[0]  # Nome del file senza estensione
                    html_content += f'<li><a href="{pdf_file}">{link_text}</a></li>\n'
                else:
                    html_content += f'<li>{pdf_file} (PDF non trovato)</li>\n'
                    
            html_content += "</ul>\n"

    html_content += "</body></html>\n"
    
    return html_content

# Assicurati che la cartella output esista
os.makedirs(output_dir, exist_ok=True)

# Genera il contenuto HTML
html_output = generate_html()

# Scrivi il file index.html nella cartella output
output_html_file = os.path.join(output_dir, 'index.html')
with open(output_html_file, 'w') as f:
    f.write(html_output)

print("HTML index created successfully in the 'output' directory.")
