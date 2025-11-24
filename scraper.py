import requests
from bs4 import BeautifulSoup
import json
import time

# Target: Rekrute
URL = "https://www.rekrute.com/offres-emploi-maroc.html"

# We look like a real browser to avoid being blocked
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
}

def scrape():
    print(f"🚀 Connecting to {URL}...")
    try:
        session = requests.Session()
        response = session.get(URL, headers=HEADERS, timeout=20)
        
        if response.status_code != 200:
            print(f"❌ Blocked or Error. Status Code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # STRATEGY 1: Look for 'post-item' (Standard)
        cards = soup.find_all(class_="post-item")
        
        # STRATEGY 2: If 1 fails, look for specific list items
        if not cards:
            print("⚠️ Strategy 1 failed. Trying Strategy 2...")
            cards = soup.select('li.post-item')

        print(f"✅ Found {len(cards)} raw job cards.")

        jobs = []
        for card in cards[:30]: # Process top 30
            try:
                # 1. Title (Try H2, then H3, then A)
                title_tag = card.find('h2') or card.find('h3') or card.find('a', class_='titreJob')
                title = title_tag.text.strip() if title_tag else "Offre Recente"

                # 2. Company (Try IMG alt, then text)
                company = "Confidential"
                photo_div = card.find(class_="photo")
                if photo_div and photo_div.find('img'):
                    company = photo_div.find('img').get('alt')
                elif photo_div:
                    company = photo_div.text.strip()

                # 3. Link
                link_tag = card.find('a', class_='titreJob') or card.find('a')
                link = "#"
                if link_tag and 'href' in link_tag.attrs:
                    link = "https://www.rekrute.com" + link_tag['href']

                # 4. Location (Optional - Try to find it)
                location = "Morocco"
                info_tag = card.find(class_="info")
                if info_tag:
                    text = info_tag.text.strip()
                    if "|" in text:
                        location = text.split('|')[-1].strip()

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "link": link,
                    "date": time.strftime("%d/%m/%Y")
                })
                
            except Exception as e:
                continue

        return jobs

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        return []

if __name__ == "__main__":
    data = scrape()
    
    # ALWAYS save the file, even if empty (so the site doesn't crash)
    with open('jobs.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    if len(data) > 0:
        print(f"🎉 Success! Saved {len(data)} jobs.")
    else:
        print("⚠️ Warning: jobs.json is empty. The site structure might have changed.")
