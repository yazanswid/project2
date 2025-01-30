from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def create_pdf(text, output_folder="PDF_INVOICE", filename="output.pdf"):
    # Zorg dat de map bestaat
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Pad naar het PDF-bestand
    file_path = os.path.join(output_folder, filename)
    
    # Maak een PDF-bestand aan
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    
    # Voeg tekst toe op het midden van de pagina
    text_x = width / 2
    text_y = height / 2
    c.drawCentredString(text_x, text_y, text)
    
    c.save()
    print(f"PDF opgeslagen als: {file_path}")

if __name__ == "__main__":
    user_text = input("Voer de tekst in voor de PDF: ")
    create_pdf(user_text)
