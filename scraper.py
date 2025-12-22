import requests
from bs4 import BeautifulSoup
import json
import time

# Konfigurace - Hlavní URL klubu Kunratice
CLUB_URL = "https://www.fotbal.cz/souteze/club/club/697be23f-6185-48b9-ba91-66c82b3d81e9"
BASE_URL = "https://www.fotbal.cz"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_team_data():
    print("🚀 Startuji stahování dat z fotbal.cz...")
    try:
        response = requests.get(CLUB_URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data = {}
        
        # Najdeme tabulku se seznamem týmů v sekci "Seznam týmů v aktuálních soutěžích"
        teams_table = soup.find('table')
        if not teams_table:
            print("❌ Chyba: Nepodařilo se najít hlavní tabulku týmů.")
            return data

        rows = teams_table.find_all('tr')[1:] # Přeskočíme hlavičku
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 2: continue
            
            team_name = cols[0].text.strip()
            # Odkaz na detailní tabulku soutěže
            link_tag = cols[1].find('a')
            if not link_tag: continue
            
            link = link_tag['href']
            full_link = BASE_URL + link
            
            print(f"🔄 Zpracovávám: {team_name}...")
            
            # Stáhneme stránku s tabulkou konkrétní ligy
            team_response = requests.get(full_link, headers=headers)
            team_soup = BeautifulSoup(team_response.content, 'html.parser')
            
            team_info = {
                "competition": cols[1].text.strip(),
                "table": []
            }
            
            # Hledáme tabulku s pořadím
            league_table = team_soup.find('table')
            if league_table:
                league_rows = league_table.find_all('tr')[1:]
                for l_row in league_rows:
                    l_cols = l_row.find_all('td')
                    if len(l_cols) >= 5:
                        team_info["table"].append({
                            "pos": l_cols[0].text.strip().replace('.', ''),
                            "team": l_cols[1].text.strip(),
                            "matches": l_cols[2].text.strip(),
                            "points": l_cols[-1].text.strip()
                        })
            
            data[team_name] = team_info
            time.sleep(1) # Prevence proti zablokování (Rate limiting)

        return data

    except Exception as e:
        print(f"⚠️ Došlo k chybě: {e}")
        return {}

if __name__ == "__main__":
    results = get_team_data()
    if results:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("✅ Hotovo! Soubor data.json byl vytvořen a naplněn.")
    else:
        print("❌ Skript skončil bez získání dat.")
