import os
import json
import shutil

# Stap 1: Mappen aanmaken
base_path = os.getcwd()  # Huidige werkmap
json_order_path = os.path.join(base_path, 'JSON_ORDER')
json_processed_path = os.path.join(base_path, 'JSON_PROCESSED')
json_invoice_path = os.path.join(base_path, 'JSON_INVOICE')

# Mappen aanmaken als ze niet bestaan
os.makedirs(json_order_path, exist_ok=True)
os.makedirs(json_processed_path, exist_ok=True)
os.makedirs(json_invoice_path, exist_ok=True)

# Stap 2: Haal de bestanden op in JSON_ORDER
def get_files_from_order():
    files = []
    for filename in os.listdir(json_order_path):
        file_path = os.path.join(json_order_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.json'):
            files.append(file_path)
    return files

# Stap 3: Verwerk ieder bestand en genereer een factuur
def generate_invoice(order_data):
    # Voorbeeld van hoe een factuur JSON eruit zou kunnen zien
    invoice = {
        "invoice_number": order_data["order_id"],  # Gebruik een uniek order_id
        "customer_name": order_data["customer_name"],
        "items": order_data["items"],
        "total_amount": sum(item["price"] * item["quantity"] for item in order_data["items"]),
        "status": "Paid"  # Stel hier een status in, afhankelijk van je logica
    }
    return invoice

# Stap 4: Verwerk bestanden
def process_orders():
    order_files = get_files_from_order()
    for order_file in order_files:
        # Bestanden lezen
        with open(order_file, 'r') as f:
            order_data = json.load(f)
        
        # Genereer een factuur
        invoice = generate_invoice(order_data)

        # Sla de factuur op in JSON_INVOICE
        invoice_filename = f"invoice_{order_data['order_id']}.json"
        invoice_file_path = os.path.join(json_invoice_path, invoice_filename)
        with open(invoice_file_path, 'w') as f:
            json.dump(invoice, f, indent=4)

        # Verplaats het verwerkte bestand naar JSON_PROCESSED
        processed_file_path = os.path.join(json_processed_path, os.path.basename(order_file))
        shutil.move(order_file, processed_file_path)

# Stap 5: Uitvoeren van de functie
process_orders()
