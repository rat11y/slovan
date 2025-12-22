import requests
from bs4 import BeautifulSoup
import json

def scrape():
    url = "https://www.fotbal.cz/souteze/club/club/697be23f-6185-48b9-ba91-66c82b3d81e9"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    print("Stahuji data...")
    
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, "html.parser")
        
        # Vytvoříme základní strukturu
        data = {"klub": "SK Slovan Kunratice", "tabulky": []}
        
        # Najdeme všechny tabulky na stránce
        for table in soup.find_all("table"):
            rows = []
            for tr in table.find_all("tr"):
                cells = [td.text.strip() for td in tr.find_all(["td", "th"])]
                rows.append(cells)
            data["tabulky"].append(rows)
            
    except Exception as e:
        print(f"Chyba při stahování: {e}")
        data = {"error": str(e)}

    # DŮLEŽITÉ: Tento řádek MUSÍ proběhnout vždy
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Soubor data.json uložen!")

if __name__ == "__main__":
    scrape()
