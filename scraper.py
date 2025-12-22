import requests
from bs4 import BeautifulSoup
import json

def scrape():
    # URL klubu Kunratice
    url = "https://www.fotbal.cz/souteze/club/club/697be23f-6185-48b9-ba91-66c82b3d81e9"
    
    # Špičkové maskování za moderní prohlížeč
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "cs,en-GB;q=0.9,en;q=0.8",
        "Referer": "https://www.google.com/",
        "DNT": "1"
    }
    
    print("🕵️ Pokouším se oklamat ochranu fotbal.cz...")
    
    try:
        # Použijeme Session, která si pamatuje "cookies" (vypadá to víc lidsky)
        session = requests.Session()
        session.headers.update(headers)
        
        # Nejdřív jdeme na hlavní stranu, abychom dostali cookies
        session.get("https://www.fotbal.cz", timeout=10)
        
        # Teď teprve jdeme pro data
        res = session.get(url, timeout=15)
        res.raise_for_status()
        
        soup = BeautifulSoup(res.content, "html.parser")
        data = {"status": "success", "tables": []}
        
        # Najdeme všechny tabulky (výsledky, rozpisy)
        found_tables = soup.find_all("table")
        for table in found_tables:
            rows = []
            for tr in table.find_all("tr"):
                cells = [td.text.strip() for td in tr.find_all(["td", "th"])]
                if cells: rows.append(cells)
            if rows: data["tables"].append(rows)
            
        print(f"🎉 Úspěch! Staženo {len(data['tables'])} tabulek.")
            
    except Exception as e:
        print(f"❌ Pořád nás blokují: {e}")
        data = {"status": "error", "message": str(e)}

    # TENTO ŘÁDEK JE NEJDŮLEŽITĚJŠÍ: Musíme vytvořit soubor, i kdyby byl prázdný
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("💾 Soubor data.json byl uložen na disk.")

if __name__ == "__main__":
    scrape()
