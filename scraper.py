import requests
from bs4 import BeautifulSoup
import json
import os

def scrape():
    # Cesta k souboru
    file_path = 'data.json'
    
    # Základní data, kdyby vše selhalo
    output_data = {"status": "error", "message": "Nepodařilo se stáhnout data"}
    
    try:
        url = "https://www.fotbal.cz/souteze/club/club/697be23f-6185-48b9-ba91-66c82b3d81e9"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html.parser")
            output_data = {"status": "ok", "tables": []}
            
            for table in soup.find_all("table"):
                rows = []
                for tr in table.find_all("tr"):
                    cells = [td.text.strip() for td in tr.find_all(["td", "th"])]
                    rows.append(cells)
                output_data["tables"].append(rows)
                
    except Exception as e:
        print(f"Chyba: {e}")
        output_data["message"] = str(e)

    # ZÁPIS SOUBORU - Tohle je nejdůležitější část
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    
    print(f"Soubor {file_path} byl zapsán. Velikost: {os.path.getsize(file_path)} bajtů")

if __name__ == "__main__":
    scrape()
