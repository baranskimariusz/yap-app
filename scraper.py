import requests
import json
import time
from pathlib import Path

BASE_URL = "https://kanjiapi.dev/v1/"

def fetch_all_kanji():
    try:
        response = requests.get(f"{BASE_URL}kanji/all")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching kanji list: {e}")
        return []

def fetch_kanji_details(character):
    try:
        response = requests.get(f"{BASE_URL}kanji/{character}")
        response.raise_for_status()
        data = response.json()
        
        if data.get('grade') and data.get('meanings'):
            return {
                "character": character,
                "readings": {
                    "on_yomi": data.get('on_readings', []),
                    "kun_yomi": data.get('kun_readings', [])
                },
                "meanings": data.get('meanings', [])
            }
        return None
    except Exception as e:
        print(f"Error fetching {character}: {e}")
        return None

def scrape_kanji():
    kanji_data = []
    existing_characters = set()
    
    if Path("kanji_data.json").exists():
        with open("kanji_data.json", "r", encoding="utf-8") as f:
            kanji_data = json.load(f)
            existing_characters = {k['character'] for k in kanji_data}
    
    all_kanji = fetch_all_kanji()
    
    for i, character in enumerate(all_kanji, 1):
        if character in existing_characters:
            print(f"Omijam {character} (istnieje)")
            continue
            
        details = fetch_kanji_details(character)
        if details:
            kanji_data.append(details)
            print(f"[{i}/{len(all_kanji)}] Przetworzono {character}")
            
            if i % 20 == 0:
                save_progress(kanji_data)
            
            time.sleep(0.5)
    
    save_progress(kanji_data)
    return kanji_data

def save_progress(data):
    try:
        temp_file = "kanji_data_temp.json"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        Path(temp_file).replace("kanji_data.json")
        print(f"Postęp zapisany: {len(data)} kanji")
        
    except Exception as e:
        print(f"Błąd zapisywania postępu: {e}")

if __name__ == "__main__":
    print("Uruchamianie scrapera Kanji API...")
    data = scrape_kanji()
    print(f"Scraping zakończony. Całkowita liczba zapisanych kanji: {len(data)}")