# import os
#
# def generate_html_index(template_file="docs/index_template.html", output_file="docs/index.html", pdf_root="docs", ignore_dirs=("images",)):
#     # Carica il template
#     with open(template_file, "r") as template:
#         html_template = template.read()
#
#     # Costruisci il contenuto dinamico per le categorie e i PDF
#     content = ""
#     for category in sorted(os.listdir(pdf_root)):
#         category_path = os.path.join(pdf_root, category)
#
#         # Ignora le cartelle specificate
#         if category in ignore_dirs or not os.path.isdir(category_path):
#             continue
#
#         content += f"<h2>{category}</h2><ul>"
#         for pdf in sorted(os.listdir(category_path)):
#             if pdf.endswith(".pdf"):
#                 pdf_path = os.path.join(category, pdf)
#                 content += f'<li><a href="{pdf_path}">{pdf}</a></li>'
#         content += "</ul>"
#
#     # Sostituisci il segnaposto <<CONTENT>> nel template
#     html_output = html_template.replace("<<CONTENT>>", content)
#
#     # Scrivi il file HTML finale nella cartella docs
#     with open(output_file, "w") as output:
#         output.write(html_output)
#
# if __name__ == "__main__":
#     generate_html_index()
import os
from datetime import datetime

def extract_date_from_filename(filename):
    # Supponiamo che il formato del nome del file sia nomefile-AAAA-MM-GG.pdf
    try:
        date_str = filename.split('-')[-1].replace('.pdf', '')
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

def generate_html_index(template_file="docs/index_template.html", output_file="docs/index.html", pdf_root="docs", ignore_dirs=("images",)):
    # Carica il template
    with open(template_file, "r") as template:
        html_template = template.read()

    # Costruisci il contenuto dinamico per le categorie e i PDF
    content = ""
    for category in sorted(os.listdir(pdf_root)):
        category_path = os.path.join(pdf_root, category)
        
        # Ignora le cartelle specificate
        if category in ignore_dirs or not os.path.isdir(category_path):
            continue

        pdf_files = []
        for pdf in os.listdir(category_path):
            if pdf.endswith(".pdf"):
                date = extract_date_from_filename(pdf)
                if date:
                    pdf_files.append((pdf, date))

        # Ordina i file per data dal più recente al meno recente
        pdf_files.sort(key=lambda x: x[1], reverse=True)

        content += f"<h2>{category}</h2><ul>"
        for pdf, _ in pdf_files:
            pdf_path = os.path.join(category, pdf)
            content += f'<li><a href="{pdf_path}">{pdf}</a></li>'
        content += "</ul>"

    # Sostituisci il segnaposto <<CONTENT>> nel template
    html_output = html_template.replace("<<CONTENT>>", content)

    # Scrivi il file HTML finale nella cartella docs
    with open(output_file, "w") as output:
        output.write(html_output)

if __name__ == "__main__":
    generate_html_index()
