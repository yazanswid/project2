import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def read_json(file_path):
    try:
        with open(file_path) as f:
            return json.load(f)
    except Exception as e:
        return None

def calculate_total(producten):
    total_excl_btw = sum(p['aantal'] * p['prijs_per_stuk_excl_btw'] for p in producten)
    total_btw = sum(p['aantal'] * p['prijs_per_stuk_excl_btw'] * (p['btw_percentage'] / 100) for p in producten)
    total_incl_btw = total_excl_btw + total_btw
    return total_incl_btw

def create_invoice_pdf(invoice_data, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    
    order = invoice_data['order']
    klant = order['klant']
    
    # Basisinformatie
    c.drawString(100, 750, f"Factuurnummer: {order['ordernummer']}")
    c.drawString(100, 735, f"Orderdatum: {order['orderdatum']}")
    c.drawString(100, 720, f"Betalingstermijn: {order['betaaltermijn']}")
    c.drawString(100, 705, f"Klant: {klant['naam']}")
    c.drawString(100, 690, f"Adres: {klant['adres']}, {klant['postcode']} {klant['stad']}")
    c.drawString(100, 675, f"KVK-nummer: {klant['KVK-nummer']}")

    # Producten
    y_position = 650
    for product in order['producten']:
        c.drawString(100, y_position, f"{product['productnaam']} - {product['aantal']} @ €{product['prijs_per_stuk_excl_btw']:.2f} (Excl. BTW)")
        y_position -= 15
    
    # Totaal inclusief BTW
    total_incl_btw = calculate_total(order['producten'])
    c.drawString(100, y_position - 30, f"Totaal (Incl. BTW): €{total_incl_btw:.2f}")
    c.save()

def process_orders(orders_path, output_path, error_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    if not os.path.exists(error_path):
        os.makedirs(error_path)

    for filename in os.listdir(orders_path):
        if filename.endswith('.json'):
            file_path = os.path.join(orders_path, filename)
            order_data = read_json(file_path)

            if order_data is None:
                error_file_path = os.path.join(error_path, filename)
                os.rename(file_path, error_file_path)
                continue

            pdf_path = os.path.join(output_path, filename.replace('.json', '.pdf'))
            create_invoice_pdf(order_data, pdf_path)
            print(f"Invoice PDF created for {filename}")

# Paden (pas deze aan naar je eigen locaties)
orders_path = '\Users\yazan\Documents\GitHub\project2\JSON_ORDER '
output_path = '\Users\yazan\Documents\GitHub\project2\PDF_INVOICE'
error_path = '\Users\yazan\Documents\GitHub\project2\JSON_ORDER_ERROR'

# Verwerk de orders
process_orders(orders_path, output_path, error_path)
