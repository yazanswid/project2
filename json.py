import json
from datetime import datetime, timedelta

def load_order(file_path):
    """Laadt de ordergegevens uit een JSON-bestand."""
    with open(file_path, 'r') as file:
        return json.load(file)

def calculate_invoice(order_data):
    """Zet ordergegevens om in factuurgegevens met de nodige berekeningen."""
    order = order_data["order"]
    klant = order["klant"]
    producten = order["producten"]
    
    factuurnummer = f"F-{order['ordernummer']}"
    factuurdatum = datetime.strptime(order["orderdatum"], "%d-%m-%Y")
    vervaldatum = factuurdatum + timedelta(days=int(order["betaaltermijn"].split('-')[0]))
    
    factuur_producten = []
    totaal_excl_btw = 0
    totaal_btw = 0
    
    for product in producten:
        subtotaal_excl = product["aantal"] * product["prijs_per_stuk_excl_btw"]
        btw_bedrag = round(subtotaal_excl * (product["btw_percentage"] / 100), 2)
        subtotaal_incl = subtotaal_excl + btw_bedrag
        
        totaal_excl_btw += subtotaal_excl
        totaal_btw += btw_bedrag
        
        factuur_producten.append({
            "productnaam": product["productnaam"],
            "aantal": product["aantal"],
            "prijs_per_stuk_excl_btw": product["prijs_per_stuk_excl_btw"],
            "btw_percentage": product["btw_percentage"],
            "subtotaal_excl_btw": round(subtotaal_excl, 2),
            "btw_bedrag": round(btw_bedrag, 2),
            "subtotaal_incl_btw": round(subtotaal_incl, 2)
        })
    
    totaal_incl_btw = totaal_excl_btw + totaal_btw
    
    factuur = {
        "factuur": {
            "factuurnummer": factuurnummer,
            "factuurdatum": factuurdatum.strftime("%d-%m-%Y"),
            "vervaldatum": vervaldatum.strftime("%d-%m-%Y"),
            "klant": klant,
            "producten": factuur_producten,
            "totaal_excl_btw": round(totaal_excl_btw, 2),
            "totaal_btw": round(totaal_btw, 2),
            "totaal_incl_btw": round(totaal_incl_btw, 2)
        }
    }
    
    return factuur

def save_invoice(invoice_data, output_path):
    """Slaat de gegenereerde factuurgegevens op in een JSON-bestand."""
    with open(output_path, 'w') as file:
        json.dump(invoice_data, file, indent=4)

def main():
    order_file = "order.json"  
    invoice_file = "factuur.json"

    try:
        order_data = load_order(order_file)
        print("Orderdata succesvol geladen:", order_data)

        invoice_data = calculate_invoice(order_data)
        print("Factuurdata succesvol gegenereerd:", invoice_data)

        save_invoice(invoice_data, invoice_file)
        print(f"Factuur opgeslagen als {invoice_file}")
    
    except Exception as e:
        print(f"Fout opgetreden: {e}")
