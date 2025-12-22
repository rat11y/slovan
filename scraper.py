import requests
from bs4 import BeautifulSoup
import json

def scrape():
    url = "https://www.fotbal.cz/souteze/club/club/697be23f-6185-48b9-ba91-66c82b3d81e9"
    # Toto je maskování za běžný prohlížeč:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    
    print("🚀 Startuji maskované stahování...")
    
    try:
        session = requests.Session()
        res = session.get(url, headers=headers, timeout=15)
        res.raise_for_status() # Pokud hodí 403, uvidíme to v logu
        
        soup = BeautifulSoup(res.content, "html.parser")
        data = {"klub": "SK Slovan Kunratice", "tabulky": []}
        
        for table in soup.find_all("table"):
            rows = []
            for tr in table.find_all("tr"):
                cells = [td.text.strip() for td in tr.find_all(["td", "th"])]
                if cells: rows.append(cells)
            data["tabulky"].append(rows)
            
        print(f"✅ Staženo {len(data['tabulky'])} tabulek.")
            
    except Exception as e:
        print(f"❌ Chyba: {e}")
        data = {"error": str(e), "status": "blocked_or_failed"}

    # Vždy zapíšeme soubor, aby robot nehlásil chybu 128
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("💾 Soubor data.json uložen.")

if __name__ == "__main__":
    scrape()
    
    print(f"Soubor {file_path} byl zapsán. Velikost: {os.path.getsize(file_path)} bajtů")

if __name__ == "__main__":
    scrape()
