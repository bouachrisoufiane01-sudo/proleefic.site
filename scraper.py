import requests
from bs4 import BeautifulSoup
import json
import time
import random
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Headers to look like a real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

def detect_category(title):
    t = title.lower()
    if "technicien" in t or "maintenance" in t: return "cat_tech"
    if "ingénieur" in t or "génie" in t: return "cat_eng"
    if "commercial" in t or "vendeur" in t: return "cat_sales"
    if "chauffeur" in t or "transport" in t or "coursier" in t: return "cat_transport"
    if "production" in t or "opérateur" in t or "usine" in t: return "cat_prod"
    if "développeur" in t or "it " in t: return "cat_it"
    return "cat_prod"

# ==========================================
# 🤖 ROBOT 1: THE HUNTER (Real Scraping)
# Scrapes MarocAnnonces & Anapec
# ==========================================
def run_hunter_robot():
    print("🤖 ROBOT 1 (Hunter): Starting...")
    real_jobs = []
    
    # A. MAROC ANNONCES (Best for Individuals/Technicians)
    url_ma = "https://www.marocannonces.com/maroc/offres-emploi-b309.html"
    try:
        resp = requests.get(url_ma, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'lxml')
            items = soup.select('ul.cars-list li')
            for item in items:
                try:
                    title = item.find('h3').get_text(strip=True)
                    link = "https://www.marocannonces.com/" + item.find('a')['href'].lstrip('/')
                    loc = item.find('span', class_='location').get_text(strip=True)
                    
                    real_jobs.append({
                        "id": int(time.time()) + random.randint(1, 9999),
                        "title": title,
                        "company": "Recruteur (MarocAnnonces)",
                        "location": loc.strip(),
                        "catId": detect_category(title),
                        "salary": "À discuter",
                        "posted": 0, # Fresh
                        "urgent": False,
                        "easyApply": False,
                        "rating": "N/A",
                        "link": link,
                        "sourceName": "MarocAnnonces"
                    })
                except: continue
    except Exception as e:
        print(f"⚠️ Hunter (MA) Error: {e}")

    # B. ANAPEC (Best for Government/Regulated)
    # We search for a generic term like "Technicien" to grab latest
    url_anapec = "http://www.anapec.org/sigec-app-rv/chercheurs/resultat_recherche?mot_cle=Technicien"
    try:
        resp = requests.get(url_anapec, headers=HEADERS, timeout=20, verify=False)
        soup = BeautifulSoup(resp.content, 'lxml')
        rows = soup.find_all('tr')
        for row in rows:
            try:
                cols = row.find_all('td')
                if len(cols) < 3: continue
                title = cols[1].get_text(strip=True)
                loc = cols[2].get_text(strip=True)
                
                real_jobs.append({
                    "id": int(time.time()) + random.randint(10000, 19999),
                    "title": title,
                    "company": "Via Anapec",
                    "location": loc.strip(),
                    "catId": detect_category(title),
                    "salary": "SMIG+",
                    "posted": 1,
                    "urgent": False,
                    "easyApply": False,
                    "rating": "Official",
                    "link": "http://www.anapec.org/sigec-app-rv/chercheurs/resultat_recherche",
                    "sourceName": "Anapec"
                })
            except: continue
    except: pass

    print(f"✅ ROBOT 1 Finished: Found {len(real_jobs)} real jobs.")
    return real_jobs

# ==========================================
# 🏭 ROBOT 2: THE FACTORY (Generator)
# Creates Smart Links for LinkedIn & Individuals
# ==========================================
def run_factory_robot():
    print("🏭 ROBOT 2 (Factory): Starting...")
    gen_jobs = []
    
    # 1. INDUSTRIAL GIANTS (Smart Search Links)
    factories = [
        ("Opérateur Câblage", "Yazaki", "Tanger"),
        ("Technicien Qualité", "Renault", "Tanger"),
        ("Ingénieur Process", "Stellantis", "Kenitra"),
        ("Magasinier", "Lear Corporation", "Meknes"),
        ("Agent de Production", "Aptiv", "Tanger"),
        ("Electricien Industriel", "OCP", "Jorf Lasfar")
    ]
    
    for f in factories:
        q = f"{f[0]} {f[1]}".replace(" ", "+")
        gen_jobs.append({
            "id": int(time.time()) + random.randint(20000, 29999),
            "title": f[0],
            "company": f[1],
            "location": f[2],
            "catId": detect_category(f[0]),
            "salary": "4000 - 8000 MAD",
            "posted": 0,
            "urgent": True,
            "easyApply": True,
            "rating": "4.5",
            "link": f"https://www.linkedin.com/jobs/search/?keywords={q}",
            "sourceName": "LinkedIn"
        })
        
    # 2. INDIVIDUALS (Particuliers) - High Demand
    # We link these to specific search queries on MarocAnnonces/Avito styles
    individuals = [
        ("Chauffeur Personnel", "Rabat", "cat_transport"),
        ("Femme de Ménage", "Casablanca", "cat_prod"),
        ("Jardinier", "Marrakech", "cat_prod"),
        ("Garde malade", "Fes", "cat_tech"),
        ("Coursier Moto", "Casablanca", "cat_transport"),
        ("Cuisinier / Chef", "Agadir", "cat_prod")
    ]
    
    for ind in individuals:
        q = ind[0].replace(" ", "+")
        gen_jobs.append({
            "id": int(time.time()) + random.randint(30000, 39999),
            "title": ind[0],
            "company": "Particulier",
            "location": ind[1],
            "catId": ind[2],
            "salary": "À discuter",
            "posted": 0,
            "urgent": True,
            "easyApply": False,
            "rating": "N/A",
            "link": f"https://www.marocannonces.com/maroc/offres-emploi-b309.html?kw={q}",
            "sourceName": "MarocAnnonces"
        })

    print(f"✅ ROBOT 2 Finished: Generated {len(gen_jobs)} smart jobs.")
    return gen_jobs

# ==========================================
# 🧠 MAIN BRAIN (Merger)
# ==========================================
if __name__ == "__main__":
    final_db = []
    
    # 1. Run Both Robots
    final_db.extend(run_hunter_robot())
    final_db.extend(run_factory_robot())
    
    # 2. Shuffle for variety
    random.shuffle(final_db)
    
    # 3. Save
    if len(final_db) > 0:
        with open('jobs.json', 'w', encoding='utf-8') as f:
            json.dump(final_db, f, ensure_ascii=False, indent=2)
        print(f"🚀 TOTAL SUCCESS: Saved {len(final_db)} jobs to database.")
    else:
        print("❌ FATAL ERROR: Both robots failed.")
        # Safety net: Save generic backup if everything fails
        sys.exit(1)
