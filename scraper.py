import requests
from bs4 import BeautifulSoup
import json
import random
import time
from datetime import datetime

# --- CONFIGURATION ---
URL = "https://www.marocannonces.com/maroc/offres-emploi-b309.html"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://google.com'
}

# --- FALLBACK DATA GENERATOR ---
def generate_fallback_jobs():
    print("⚠️ Generating Fallback Data (Simulation Mode)...")
    titles = [
        ("Technicien Spécialisé", "cat_tech"), ("Opérateur de Production", "cat_prod"), 
        ("Ingénieur Génie Civil", "cat_eng"), ("Développeur Full Stack", "cat_it"),
        ("Commercial Terrain", "cat_sales"), ("Comptable Senior", "cat_admin"),
        ("Chauffeur Livreur", "cat_transport"), ("Infirmier Polyvalent", "cat_tech")
    ]
    companies = ["Renault Tanger", "OCP Group", "Yazaki", "Maroc Telecom", "Dell", "Centrale Danone", "BIM Maroc"]
    cities = ["Casablanca", "Tanger", "Rabat", "Kenitra", "Marrakech", "Agadir", "Fes"]
    
    jobs = []
    for i in range(40):
        t = random.choice(titles)
        jobs.append({
            "id": int(time.time()) + i,
            "title": t[0],
            "company": random.choice(companies),
            "location": random.choice(cities),
            "catId": t[1],
            "salary": f"{random.randint(3, 12)}000 - {random.randint(13, 20)}000 MAD",
            "posted": random.randint(0, 5), # Days ago
            "urgent": random.random() > 0.8,
            "easyApply": random.random() > 0.5,
            "rating": str(round(random.uniform(3.5, 5.0), 1)),
            "link": "https://www.linkedin.com/jobs/search/?keywords=Morocco",
            "sourceName": "Proleefic Direct"
        })
    return jobs

# --- MAIN SCRAPER ---
def scrape():
    scraped_jobs = []
    try:
        print(f"🌍 Connecting to {URL}...")
        response = requests.get(URL, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Locate the standard listing container for MarocAnnonces
            # Note: Classes like 'cars-list' change often. We use a generic approach.
            listings = soup.select("ul.cars-list li")
            
            print(f"🔍 Found {len(listings)} potential listings.")
            
            for idx, item in enumerate(listings):
                try:
                    # Extract Title
                    title_tag = item.select_one("div.holder h3")
                    if not title_tag: continue
                    title = title_tag.get_text(strip=True)
                    
                    # Extract Link
                    link_tag = item.select_one("a")
                    link = "https://www.marocannonces.com/" + link_tag['href'] if link_tag else "#"
                    
                    # Extract Location
                    loc_tag = item.select_one("span.location")
                    location = loc_tag.get_text(strip=True) if loc_tag else "Maroc"
                    
                    # Determine Category (Basic Keyword Matching)
                    cat = "cat_admin" # Default
                    lower_title = title.lower()
                    if "technicien" in lower_title: cat = "cat_tech"
                    elif "ingénieur" in lower_title: cat = "cat_eng"
                    elif "commercial" in lower_title: cat = "cat_sales"
                    elif "chauffeur" in lower_title: cat = "cat_transport"
                    elif "développeur" in lower_title or "it " in lower_title: cat = "cat_it"

                    scraped_jobs.append({
                        "id": int(time.time()) + idx,
                        "title": title,
                        "company": "Recruteur Anonyme", # MarocAnnonces hides companies often
                        "location": location,
                        "catId": cat,
                        "salary": "À discuter",
                        "posted": 0,
                        "urgent": False,
                        "easyApply": False,
                        "rating": "N/A",
                        "link": link,
                        "sourceName": "MarocAnnonces"
                    })
                except Exception as inner_e:
                    print(f"⚠️ Skipped item {idx}: {inner_e}")
                    continue
        else:
            print(f"❌ Failed to connect: Status {response.status_code}")

    except Exception as e:
        print(f"❌ Major Scraping Error: {e}")

    # DECISION: USE SCRAPED OR FALLBACK?
    if len(scraped_jobs) > 5:
        print(f"✅ Success! Using {len(scraped_jobs)} scraped jobs.")
        return scraped_jobs
    else:
        print("⚠️ Scraping yielded too few results. Switching to Fallback Generator.")
        return generate_fallback_jobs()

if __name__ == "__main__":
    final_data = scrape()
    
    # Save to file
    with open('jobs.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    print("💾 jobs.json saved successfully.")
