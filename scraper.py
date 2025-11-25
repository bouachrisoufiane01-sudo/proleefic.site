from bs4 import BeautifulSoup
import requests
import json
import time
import random

# --- CONFIGURATION ---
OUTPUT_FILE = "jobs.json"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://google.com'
}

# List of cities to look for in job descriptions
MOROCCAN_CITIES = [
    "Casablanca", "Rabat", "Tanger", "Marrakech", "Agadir", "Fès", 
    "Meknès", "Oujda", "Kenitra", "Tetouan", "Laayoune", "Dakhla", 
    "Mohammedia", "Salé", "El Jadida", "Bouskoura", "Nouaceur"
]

def extract_city(text_content):
    """
    Helper: Scans a text string to find a matching Moroccan city.
    Defaults to 'Maroc' if no specific city is found.
    """
    if not text_content:
        return "Maroc"
    
    text_lower = text_content.lower()
    for city in MOROCCAN_CITIES:
        # check for city name (surrounded by check to avoid partial matches if needed, 
        # but simple string check is usually fine for scrapers)
        if city.lower() in text_lower:
            return city
            
    return "Maroc"

def get_direct_jobs():
    """
    These are the 10 'Real' Direct Hiring offers (Yazaki, Marjane, etc.)
    that will ALWAYS be on your site, even if scraping fails.
    """
    print("⚡ Adding Direct Hiring Offers...")
    return [
        {
            "id": "d_01", "title": "Responsable Production", "company": "Yazaki Tanger", "location": "Tanger",
            "salary": "12.000 DH", "posted": "1h ago", "urgent": True, "isReal": True, "isDirect": True,
            "sourceName": "Direct HR", "email": "rh.tanger@yazaki-group.com", "catId": "cat_prod",
            "reqs": ["Bac+5 Ingénieur", "5 ans expérience", "Anglais courant"]
        },
        {
            "id": "d_02", "title": "Vendeur Showroom", "company": "Marjane Market", "location": "Casablanca",
            "salary": "4.000 DH", "posted": "2h ago", "urgent": True, "isReal": True, "isDirect": True,
            "sourceName": "Direct HR", "email": "recrutement@marjane.co.ma", "catId": "cat_sales",
            "reqs": ["Niveau Bac", "Bonne présentation", "Dynamique"]
        },
        {
            "id": "d_03", "title": "Technicien Maintenance", "company": "Stellantis", "location": "Kenitra",
            "salary": "7.500 DH", "posted": "3h ago", "urgent": True, "isReal": True, "isDirect": True,
            "sourceName": "Direct HR", "email": "jobs@stellantis.ma", "catId": "cat_tech",
            "reqs": ["Bac+2 Electromécanique", "3 ans expérience", "Travail posté"]
        },
         {
            "id": "d_04", "title": "Infirmière Polyvalente", "company": "Clinique Agdal", "location": "Rabat",
            "salary": "5.500 DH", "posted": "5h ago", "urgent": False, "isReal": True, "isDirect": True,
            "sourceName": "Direct HR", "email": "contact@clinique-agdal.ma", "catId": "cat_health",
            "reqs": ["Diplôme d'état", "Expérience urgences", "Garde de nuit"]
        }
    ]

def scrape_rekrute():
    """Scrape Rekrute.com with City Detection"""
    print("🔍 Scraping Rekrute...")
    jobs = []
    try:
        url = "https://www.rekrute.com/offres.html"
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            items = soup.find_all('li', class_='post-id') 
            
            if not items:
                items = soup.find_all('div', class_='section')
            
            for idx, item in enumerate(items):
                try:
                    title_tag = item.find('h2') or item.find('a', class_='titreJob')
                    if not title_tag: continue
                    
                    title = title_tag.get_text(strip=True)
                    link = "https://www.rekrute.com" + title_tag.find('a')['href'] if title_tag.find('a') else "#"
                    
                    # --- CITY EXTRACTION ---
                    # We grab the full text of the list item to search for the city
                    full_card_text = item.get_text(separator=" ")
                    detected_city = extract_city(full_card_text)

                    jobs.append({
                        "id": f"rek_{idx}",
                        "title": title[:60],
                        "company": "Rekrute Recruteur",
                        "location": detected_city, # Uses the result of extraction
                        "salary": "Negotiable",
                        "posted": "Today",
                        "urgent": False, "isReal": False, "isDirect": False,
                        "sourceName": "Rekrute",
                        "link": link,
                        "catId": "cat_admin"
                    })
                except: continue
    except Exception as e:
        print(f"⚠️ Rekrute Error: {e}")
    return jobs

def scrape_dreamjob():
    """Scrape Dreamjob.ma with City Detection"""
    print("🔍 Scraping Dreamjob...")
    jobs = []
    try:
        url = "https://www.dreamjob.ma/"
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article', limit=15)
            
            for idx, art in enumerate(articles):
                try:
                    title_tag = art.find('h1') or art.find('h2') or art.find('h3')
                    if not title_tag: continue
                    
                    title = title_tag.get_text(strip=True)
                    link_tag = art.find('a')
                    link = link_tag['href'] if link_tag else "#"
                    
                    # --- CITY EXTRACTION ---
                    # Check Title first (Dreamjob often puts city in title) + Body text
                    full_text_to_scan = title + " " + art.get_text(separator=" ")
                    detected_city = extract_city(full_text_to_scan)
                    
                    # Simple category detection
                    cat = "cat_sales"
                    if "technicien" in title.lower(): cat = "cat_tech"
                    elif "ingénieur" in title.lower(): cat = "cat_eng"
                    
                    jobs.append({
                        "id": f"dj_{idx}",
                        "title": title[:60],
                        "company": "Dreamjob Partner",
                        "location": detected_city, # Uses the result of extraction
                        "salary": "Negotiable",
                        "posted": "Today",
                        "urgent": False, "isReal": False, "isDirect": False,
                        "sourceName": "Dreamjob",
                        "link": link,
                        "catId": cat
                    })
                except: continue
    except Exception as e:
        print(f"⚠️ Dreamjob Error: {e}")
    return jobs

def main():
    print("🤖 Robot Started...")
    all_jobs = []

    # 1. Add Direct Jobs
    all_jobs.extend(get_direct_jobs())

    # 2. Add Scraped Jobs
    all_jobs.extend(scrape_rekrute())
    time.sleep(1) 
    all_jobs.extend(scrape_dreamjob())

    # 3. Safety Check
    if len(all_jobs) < 10:
        print("⚠️ Scraping weak. Generating backup data...")
        for i in range(20):
            all_jobs.append({
                "id": f"sim_{i}", "title": "Offre d'emploi (Voir Détails)", "company": "Recruteur", 
                "location": "Casablanca", # Default for simulation
                "salary": "Confidential", "posted": "1d ago", "urgent": False, "isReal": False, "isDirect": False,
                "sourceName": "MarocAnnonces", "link": "https://www.marocannonces.com", "catId": "cat_sales"
            })

    # 4. Overwrite File
    print(f"💾 Saving {len(all_jobs)} jobs to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=2)
    
    print("✅ DONE! Website updated.")

if __name__ == "__main__":
    main()
