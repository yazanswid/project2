from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def create_pdf(output_folder="PDF_INVOICE", filename="factuur_template.pdf"):
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    
    file_path = os.path.join(output_folder, filename)
    
   
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Factuur")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "Bedrijfsnaam: ")
    c.drawString(50, height - 120, "Adres: ")
    c.drawString(50, height - 140, "KVK-nummer: ")
    c.drawString(50, height - 160, "BTW-nummer: ")
    c.drawString(50, height - 180, "IBAN: ")
    
    c.drawString(50, height - 220, "Factuurnummer: ")
    c.drawString(50, height - 240, "Factuurdatum: ")
    c.drawString(50, height - 260, "Vervaldatum: ")
    
    c.drawString(50, height - 300, "Klantgegevens:")
    c.drawString(50, height - 320, "Bedrijfsnaam: ")
    c.drawString(50, height - 340, "Adres: ")
    c.drawString(50, height - 360, "KVK-nummer: ")
    c.drawString(50, height - 380, "BTW-nummer: ")
    
    c.drawString(50, height - 420, "Omschrijving van de geleverde diensten/producten:")
    c.line(50, height - 430, width - 50, height - 430)
    c.drawString(50, height - 450, "| Aantal | Omschrijving | Prijs per stuk | Totaal |")
    c.line(50, height - 460, width - 50, height - 460)
    
    c.drawString(50, height - 520, "Subtotaal:")
    c.drawString(50, height - 540, "BTW (21%):")
    c.drawString(50, height - 560, "Totaalbedrag:")
    
    c.drawString(10, height - 600, "Gelieve het totaalbedrag over te maken naar bovenstaand IBAN onder vermelding van het factuurnummer.")
    
    c.save()
    print(f"PDF opgeslagen als: {file_path}")

if __name__ == "__main__":
    create_pdf()
