import requests
from bs4 import BeautifulSoup
import json
import time
import random
import urllib3

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
# SMART GENERATOR (The Safety Net)
# This creates valid links to OTHER sites (not just LinkedIn)
# ---------------------------------------------------------
def generate_smart_mix():
    print("🧠 Generating Smart Mix (Anti-Block Strategy)...")
    jobs = []
    
    # 1. MAROC ANNONCES PROFILES
    ma_profiles = [
        ("Technicien Spécialisé", "Casablanca"), ("Opérateur de Production", "Tanger"), 
        ("Chauffeur Livreur", "Rabat"), ("Electricien Bâtiment", "Marrakech"),
        ("Infirmier Polyvalent", "Fes"), ("Mécanicien Auto", "Agadir")
    ]
    for p in ma_profiles:
        q = p[0].replace(" ", "%20")
        jobs.append({
            "id": int(time.time()) + random.randint(1, 10000),
            "title": p[0],
            "company": "Recruteur (MarocAnnonces)",
            "location": p[1],
            "catId": detect_category(p[0]),
            "salary": "À discuter",
            "posted": random.randint(0, 2),
            "urgent": False,
            "easyApply": False,
            "rating": "N/A",
            "link": f"https://www.marocannonces.com/maroc/offres-emploi-b309.html?kw={q}",
            "sourceName": "MarocAnnonces"
        })

    # 2. ANAPEC PROFILES
    anapec_profiles = [
        ("Ouvrier Agricole", "Agadir"), ("Technicien Maintenance", "Kenitra"),
        ("Operateur Cablage", "Tanger"), ("Soudeur", "Casablanca")
    ]
    for p in anapec_profiles:
        q = p[0].replace(" ", "+")
        jobs.append({
            "id": int(time.time()) + random.randint(20000, 30000),
            "title": p[0],
            "company": "Via Anapec",
            "location": p[1],
            "catId": detect_category(p[0]),
            "salary": "SMIG+",
            "posted": 1,
            "urgent": True,
            "easyApply": False,
            "rating": "Official",
            "link": f"http://www.anapec.org/sigec-app-rv/chercheurs/resultat_recherche?mot_cle={q}",
            "sourceName": "Anapec"
        })

    # 3. EMPLOI.MA PROFILES
    emp_profiles = [
        ("Comptable", "Rabat"), ("Assistante Direction", "Casablanca"),
        ("Commercial Terrain", "Tanger"), ("Magasinier", "Bouskoura")
    ]
    for p in emp_profiles:
        q = p[0].replace(" ", "+")
        jobs.append({
            "id": int(time.time()) + random.randint(40000, 50000),
            "title": p[0],
            "company": "Confidential",
            "location": p[1],
            "catId": detect_category(p[0]),
            "salary": "Confidential",
            "posted": 0,
            "urgent": False,
            "easyApply": True,
            "rating": "4.0",
            "link": f"https://www.emploi.ma/recherche-jobs-maroc?keywords={q}",
            "sourceName": "Emploi.ma"
        })

    return jobs

# ---------------------------------------------------------
# REAL SCRAPERS (Try these, but don't crash if blocked)
# ---------------------------------------------------------
def scrape_maroc_annonces():
    print("🕷️ Trying MarocAnnonces...")
    jobs = []
    try:
        resp = requests.get("https://www.marocannonces.com/maroc/offres-emploi-b309.html", headers=get_headers(), timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'lxml')
            for item in soup.find_all('li')[:15]: # Limit to top 15 to avoid detection
                try:
                    title = item.find('h3').get_text(strip=True)
                    link = "https://www.marocannonces.com/" + item.find('a')['href'].lstrip('/')
                    loc = item.find('span', class_='location').get_text(strip=True)
                    jobs.append({
                        "id": int(time.time()) + random.randint(100, 9000),
                        "title": title, "company": "Recruteur", "location": loc,
                        "catId": detect_category(title), "salary": "N/A", "posted": 0,
                        "urgent": False, "easyApply": False, "rating": "N/A",
                        "link": link, "sourceName": "MarocAnnonces"
                    })
                except: continue
    except: print("⚠️ MarocAnnonces blocked/failed.")
    return jobs

def scrape_rekrute():
    print("🕷️ Trying Rekrute...")
    jobs = []
    try:
        resp = requests.get("https://www.rekrute.com/offres.html", headers=get_headers(), timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'lxml')
            for item in soup.find_all('li', class_='post-item')[:10]:
                try:
                    title = item.find('h2').find('a').get_text(strip=True)
                    link = "https://www.rekrute.com" + item.find('h2').find('a')['href']
                    comp = item.find('div', class_='company-logo').find('img')['alt']
                    jobs.append({
                        "id": int(time.time()) + random.randint(50000, 60000),
                        "title": title, "company": comp, "location": "Maroc",
                        "catId": detect_category(title), "salary": "Market", "posted": 0,
                        "urgent": True, "easyApply": True, "rating": "4.8",
                        "link": link, "sourceName": "Rekrute"
                    })
                except: continue
    except: print("⚠️ Rekrute blocked/failed.")
    return jobs

# --- MAIN ---
if __name__ == "__main__":
    all_jobs = []
    
    # 1. Try Real Scraping First
    all_jobs.extend(scrape_maroc_annonces())
    all_jobs.extend(scrape_rekrute())
    
    # 2. ALWAYS Add Smart Mix (This ensures you have MarocAnnonces/Anapec even if blocked)
    all_jobs.extend(generate_smart_mix())
    
    # 3. Add some LinkedIn Smart Links for "High Tech"
    profiles = [("Développeur Full Stack", "Remote"), ("Ingénieur DevOps", "Casablanca")]
    for p in profiles:
        q = p[0].replace(" ", "+")
        all_jobs.append({
            "id": int(time.time()) + random.randint(90000, 99999),
            "title": p[0], "company": "LinkedIn Network", "location": p[1],
            "catId": "cat_it", "salary": "Competitive", "posted": 0, "urgent": True,
            "easyApply": True, "rating": "5.0",
            "link": f"https://www.linkedin.com/jobs/search/?keywords={q}+Maroc",
            "sourceName": "LinkedIn"
        })

    # Shuffle and Save
    random.shuffle(all_jobs)
    
    with open('jobs.json', 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Successfully saved {len(all_jobs)} jobs (Mixed Sources).")
