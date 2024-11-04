import os

output_dir = 'output'
index_file = os.path.join(output_dir, 'index.html')

# Crea un dizionario per tenere traccia delle cartelle e dei loro PDF
folder_dict = {}

# Scansiona la cartella output per i file PDF
for root, dirs, files in os.walk(output_dir):
    pdf_files = [f for f in files if f.endswith('.pdf')]
    if pdf_files:
        folder_name = os.path.relpath(root, output_dir)
        folder_dict[folder_name] = pdf_files

# Genera l'HTML
with open(index_file, 'w') as f:
    f.write("<html><body>\n")
    for folder, pdfs in folder_dict.items():
        # Aggiungi il titolo della cartella
        f.write(f"<h1>{folder}</h1>\n")
        f.write("<ul>\n")
        for pdf in pdfs:
            f.write(f'<li><a href="{pdf}">{pdf}</a></li>\n')
        f.write("</ul>\n")
    f.write("</body></html>\n")
