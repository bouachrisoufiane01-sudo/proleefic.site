import requests
from bs4 import BeautifulSoup
import json
import time
import random
import urllib3

# DISABLE ANAPEC SECURITY WARNINGS (Crucial!)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15'
]

def get_headers():
    return {'User-Agent': random.choice(USER_AGENTS)}

def detect_category(title):
    t = title.lower()
    if "technicien" in t or "maintenance" in t: return "cat_tech"
    if "ingénieur" in t or "génie" in t: return "cat_eng"
    if "commercial" in t or "vendeur" in t: return "cat_sales"
    if "chauffeur" in t or "transport" in t: return "cat_transport"
    if "production" in t or "opérateur" in t: return "cat_prod"
    if "développeur" in t or "it " in t: return "cat_it"
    return "cat_prod"

# ---------------------------------------------------------
# 1. ANAPEC SCRAPER (The Government Source)
# ---------------------------------------------------------
def scrape_anapec():
    print("🕷️ Scraping Anapec (Official)...")
    jobs = []
    # We search for generic terms to get a list
    keywords = ["Technicien", "Ouvrier", "Ingenieur"]
    
    for kw in keywords:
        url = f"http://www.anapec.org/sigec-app-rv/chercheurs/resultat_recherche?mot_cle={kw}"
        try:
            # verify=False is REQUIRED for Anapec
            resp = requests.get(url, headers=get_headers(), timeout=20, verify=False)
            soup = BeautifulSoup(resp.content, 'lxml')
            
            # Anapec lists jobs in a table with class 'result-search'
            # We look for rows <tr>
            rows = soup.find_all('tr')
            
            for row in rows:
                try:
                    cols = row.find_all('td')
                    if len(cols) < 3: continue
                    
                    title = cols[1].get_text(strip=True)
                    location = cols[2].get_text(strip=True)
                    
                    # Anapec links are javascript based, so we link to the main search
                    link = "http://www.anapec.org/sigec-app-rv/chercheurs/resultat_recherche"
                    
                    jobs.append({
                        "id": int(time.time()) + random.randint(1000, 9999),
                        "title": title,
                        "company": "Via Anapec", # Anapec hides company names
                        "location": location,
                        "catId": detect_category(title),
                        "salary": "SMIG+",
                        "posted": 0,
                        "urgent": False,
                        "easyApply": False,
                        "rating": "Official",
                        "link": link,
                        "sourceName": "Anapec"
                    })
                except: continue
        except Exception as e: 
            print(f"⚠️ Anapec Error ({kw}): {e}")
            
    print(f"   -> Found {len(jobs)} Anapec jobs.")
    return jobs

# ---------------------------------------------------------
# 2. REGIONAL SCRAPER (MarocAnnonces Cities)
# ---------------------------------------------------------
def scrape_regional_marocannonces():
    print("🕷️ Scraping Regional Hubs...")
    jobs = []
    
    # Specific City URLs
    regions = [
        {"city": "Tanger", "url": "https://www.marocannonces.com/maroc/offres-emploi-tanger-b309.html"},
        {"city": "Casablanca", "url": "https://www.marocannonces.com/maroc/offres-emploi-domaine-informatique-multimedia-internet-b309.html"},
        {"city": "Agadir", "url": "https://www.marocannonces.com/maroc/offres-emploi-agadir-b309.html"}
    ]
    
    for reg in regions:
        try:
            resp = requests.get(reg['url'], headers=get_headers(), timeout=15)
            soup = BeautifulSoup(resp.content, 'lxml')
            items = soup.find_all('li')
            
            for item in items[:8]: # Top 8 per city
                try:
                    title_tag = item.find('h3')
                    if not title_tag: continue
                    title = title_tag.get_text(strip=True)
                    
                    link_tag = item.find('a')
                    if not link_tag: continue
                    full_link = "https://www.marocannonces.com/" + link_tag['href'].lstrip('/')
                    
                    jobs.append({
                        "id": int(time.time()) + random.randint(10000, 99999),
                        "title": title,
                        "company": "Recruteur Local",
                        "location": reg['city'],
                        "catId": detect_category(title),
                        "salary": "À discuter",
                        "posted": 0,
                        "urgent": True, # Regional jobs are usually urgent
                        "easyApply": False,
                        "rating": "Local",
                        "link": full_link,
                        "sourceName": "MarocAnnonces"
                    })
                except: continue
        except: continue
        
    print(f"   -> Found {len(jobs)} Regional jobs.")
    return jobs

# ---------------------------------------------------------
# 3. SMART BACKUP (If everything fails)
# ---------------------------------------------------------
def generate_backup_links():
    # Only used if scraping returns 0 results
    print("🧠 Generating Backup Links...")
    jobs = []
    profiles = [("Technicien Spécialisé", "Tanger"), ("Ingénieur Industriel", "Casablanca")]
    for p in profiles:
        q = p[0].replace(" ", "+")
        jobs.append({
            "id": int(time.time()) + random.randint(1, 500),
            "title": p[0],
            "company": "LinkedIn Search",
            "location": p[1],
            "catId": "cat_tech",
            "salary": "N/A",
            "posted": 0,
            "urgent": False,
            "easyApply": True,
            "rating": "N/A",
            "link": f"https://www.linkedin.com/jobs/search/?keywords={q}",
            "sourceName": "LinkedIn"
        })
    return jobs

# --- MAIN ---
if __name__ == "__main__":
    all_jobs = []
    
    # 1. Run Scrapers
    all_jobs.extend(scrape_anapec())
    all_jobs.extend(scrape_regional_marocannonces())
    
    # 2. Safety Check
    if len(all_jobs) < 5:
        print("⚠️ Scraping low. Adding backup links.")
        all_jobs.extend(generate_backup_links())
    
    # 3. Shuffle & Save
    random.shuffle(all_jobs)
    
    with open('jobs.json', 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=2)
    
    print(f"✅ DONE. Saved {len(all_jobs)} jobs.")
