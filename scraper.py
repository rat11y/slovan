import requests
from bs4 import BeautifulSoup
import json
import os

def scrape():
    url = "https://www.fotbal.cz/souteze/club/club/697be23f-6185-48b9-ba91-66c82b3d81e9"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    print(f"Připojuji se k: {url}")
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")
    
    data = {"last_update": "Teď", "teams": {}}
    
    # Najdeme tabulky na stránce
    tables = soup.find_all("table")
    for i, table in enumerate(tables):
        rows = table.find_all("tr")
        table_data = []
        for row in rows[1:]: # Přeskočit hlavičku
            cols = row.find_all("td")
            if len(cols) > 1:
                table_data.append([c.text.strip() for c in cols])
        data["teams"][f"tabulka_{i}"] = table_data

    # KLÍČOVÝ BOD: Soubor se MUSÍ vytvořit, i kdyby byl prázdný
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Soubor data.json byl úspěšně vytvořen.")

if __name__ == "__main__":
    scrape()
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("✅ Hotovo! Soubor data.json byl vytvořen a naplněn.")
    else:
        print("❌ Skript skončil bez získání dat.")
