import requests
from bs4 import BeautifulSoup
import json
import time

# --- CONFIGURATION FOR REKRUTE ---
URL = "https://www.rekrute.com/offres-emploi-maroc.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape():
    print("🚀 Starting Scraper...")
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Rekrute uses 'post-item' or 'li' for job cards
        cards = soup.find_all(class_="post-item")
        
        jobs = []
        for card in cards[:30]: # Get top 30 jobs
            try:
                # 1. Title
                title_tag = card.find('h2')
                title = title_tag.text.strip() if title_tag else "Offre d'emploi"

                # 2. Company
                # Try to get it from the logo ALT text first (cleaner)
                company = "Confidential"
                logo_div = card.find(class_="photo")
                if logo_div and logo_div.find('img'):
                    company = logo_div.find('img').get('alt')
                elif logo_div:
                    company = logo_div.text.strip()

                # 3. Link
                link_tag = card.find('a', class_='titreJob')
                if not link_tag: link_tag = card.find('a')
                
                link = "#"
                if link_tag and 'href' in link_tag.attrs:
                    link = "https://www.rekrute.com" + link_tag['href']

                # 4. Date (Today's date)
                date = time.strftime("%d/%m/%Y")

                jobs.append({
                    "title": title,
                    "company": company,
                    "link": link,
                    "date": date
                })
                
            except Exception as e:
                continue

        return jobs

    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == "__main__":
    data = scrape()
    # Save to JSON
    with open('jobs.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved {len(data)} jobs to jobs.json")
