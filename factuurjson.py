import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def load_order(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def calculate_invoice(order_data):
    invoice = {
        "invoice_id": f"INV-{order_data['order_id']}",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "customer": order_data["customer"],
        "items": [],
        "subtotal": 0.0,
        "tax": 0.0,
        "total": 0.0
    }
    
    tax_rate = 0.21  # 21% btw
    subtotal = sum(item["price"] * item["quantity"] for item in order_data["items"])
    tax = round(subtotal * tax_rate, 2)
    total = round(subtotal + tax, 2)
    
    invoice["items"] = order_data["items"]
    invoice["subtotal"] = round(subtotal, 2)
    invoice["tax"] = tax
    invoice["total"] = total
    
    return invoice

def save_invoice(invoice_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(invoice_data, file, indent=4, ensure_ascii=False)

def generate_pdf(invoice_data, pdf_file):
    c = canvas.Canvas(pdf_file, pagesize=A4)
    c.drawString(100, 800, f"Factuur ID: {invoice_data['invoice_id']}")
    c.drawString(100, 780, f"Datum: {invoice_data['date']}")
    c.drawString(100, 760, f"Klant: {invoice_data['customer']}")
    
    y_position = 720
    c.drawString(100, y_position, "Items:")
    y_position -= 20
    for item in invoice_data["items"]:
        c.drawString(100, y_position, f"{item['name']} - Aantal: {item['quantity']} - Prijs: €{item['price']}")
        y_position -= 20
    
    c.drawString(100, y_position - 20, f"Subtotaal: €{invoice_data['subtotal']}")
    c.drawString(100, y_position - 40, f"BTW (21%): €{invoice_data['tax']}")
    c.drawString(100, y_position - 60, f"Totaal: €{invoice_data['total']}")
    
    c.save()

def main():
    order_file = "order.json"  # Pas dit aan naar de juiste bestandsnaam
    invoice_file = "invoice.json"
    pdf_file = "invoice.pdf"
    
    order_data = load_order(order_file)
    invoice_data = calculate_invoice(order_data)
    save_invoice(invoice_data, invoice_file)
    generate_pdf(invoice_data, pdf_file)
    
    print(f"Factuur opgeslagen in {invoice_file} en PDF gegenereerd: {pdf_file}")

if __name__ == "__main__":
    main()
