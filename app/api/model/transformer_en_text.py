import fitz  # PyMuPDF pour les PDF
import docx  # python-docx pour les fichiers Word
from bs4 import BeautifulSoup  # BeautifulSoup pour les fichiers HTML
import os

def extraire_texte_pdf(pdf_path):
    """Extrait le texte d'un fichier PDF"""
    texte_complet = ""
    doc = fitz.open(pdf_path)  # Ouvre le fichier PDF
    for page in doc:
        texte_complet += page.get_text("text") + "/n"  # Récupère le texte de chaque page
    return texte_complet

def extraire_texte_word(docx_path):
    """Extrait le texte d'un fichier Word (.docx)"""
    doc = docx.Document(docx_path)
    texte_complet = ""
    for para in doc.paragraphs:
        texte_complet += para.text + "/n"
    return texte_complet

def extraire_texte_html(html_path):
    """Extrait le texte d'un fichier HTML"""
    with open(html_path, "r", encoding="utf-8") as file:
        contenu_html = file.read()
    soup = BeautifulSoup(contenu_html, "html.parser")
    texte_complet = soup.get_text()
    return texte_complet

def sauvegarder_texte(texte, output_path):
    """Sauvegarde le texte dans un fichier .txt"""
    with open(output_path, "w", encoding="utf-8") as fichier:
        fichier.write(texte)

def convertir_fichier_en_texte(input_path, output_path):
    """Détecte le format du fichier et extrait le texte"""
    _, extension = os.path.splitext(input_path)
    texte = ""
    
    if extension.lower() == ".pdf":
        texte = extraire_texte_pdf(input_path)
    elif extension.lower() == ".docx":
        texte = extraire_texte_word(input_path)
    elif extension.lower() == ".html":
        texte = extraire_texte_html(input_path)
    else:
        raise ValueError("Format de fichier non pris en charge : " + extension)
    
    sauvegarder_texte(texte, output_path)
    print(f"Le texte du fichier {input_path} a été sauvegardé dans {output_path}")

# Exemple d'utilisation
fichier_input = "C:/Users/lapto/Desktop/supnum_CS-s3/S3C-2025-DEFI2/backend/defi-2-server/app/api/model/données_entrainement/Dico 9 arabe_g q.pdf"  # Remplace par ton fichier d'entrée (PDF, Word ou HTML)
fichier_output = "C:/Users/lapto/Desktop/supnum_CS-s3/S3C-2025-DEFI2/backend/defi-2-server/app/api/model/données_entrainement/donnée_entrainement_format_text.txt"  # Le fichier texte de sortie
convertir_fichier_en_texte(fichier_input, fichier_output)
