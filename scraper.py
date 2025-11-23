import requests
from bs4 import BeautifulSoup
import json
import time
import random
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

def detect_category(title):
    t = title.lower()
    if "technicien" in t or "maintenance" in t or "mécanique" in t: return "cat_tech"
    if "ingénieur" in t or "génie" in t or "qualité" in t: return "cat_eng"
    if "commercial" in t or "vendeur" in t: return "cat_sales"
    if "chauffeur" in t or "logistique" in t: return "cat_transport"
    if "production" in t or "opérateur" in t or "câblage" in t or "usine" in t: return "cat_prod"
    if "développeur" in t or "it " in t: return "cat_it"
    return "cat_prod"

# --- THE INDUSTRIAL GENERATOR (Fail-Safe) ---
# This ensures your site is full of factory jobs even if scraping is blocked
def generate_industrial_backup():
    print("🏭 Generating Industrial Jobs...")
    jobs = []
    
    # REAL INDUSTRIAL ROLES IN MOROCCO
    roles = [
        ("Opérateur de Câblage", "Tanger Free Zone", "cat_prod"),
        ("Technicien de Maintenance", "Kenitra (Atlantic Free Zone)", "cat_tech"),
        ("Contrôleur Qualité", "Casablanca", "cat_tech"),
        ("Chef d'équipe Production", "Tanger", "cat_prod"),
        ("Magasinier Cariste", "Agadir", "cat_transport"),
        ("Ingénieur Process", "Tanger", "cat_eng"),
        ("Opérateur Machine", "Mohammedia", "cat_prod"),
        ("Soudeur Industriel", "Jorf Lasfar", "cat_tech"),
        ("Electricien Industriel", "Casablanca", "cat_tech"),
        ("Responsable HSE", "Kenitra", "cat_eng")
    ]
    
    # BIG FACTORY COMPANIES
    companies = ["Yazaki", "Renault Group", "Lear Corporation", "Aptiv", "Sumitomo Electric", "Stellantis", "OCP Group", "Fujikura", "Leoni"]
    
    sources = [
        {"name": "MarocAnnonces", "url": "https://www.marocannonces.com/maroc/offres-emploi-b309.html?kw={}"},
        {"name": "Rekrute", "url": "https://www.rekrute.com/offres-emploi-maroc.html?keyword={}"},
        {"name": "Anapec", "url": "http://www.anapec.org/sigec-app-rv/chercheurs/resultat_recherche?mot_cle={}"}
    ]

    for i in range(50): # Generate 50 Industrial Jobs
        role = random.choice(roles)
        comp = random.choice(companies)
        src = random.choice(sources)
        q = role[0].replace(" ", "+")
        
        jobs.append({
            "id": int(time.time()) + i,
            "title": role[0],
            "company": comp,
            "location": role[1],
            "catId": role[2],
            "salary": f"{random.randint(3000, 5000)} - {random.randint(6000, 9000)} MAD",
            "posted": random.randint(0, 2),
            "urgent": True, # Factory jobs are always urgent
            "easyApply": True,
            "rating": "4.5",
            "link": src['url'].format(q),
            "sourceName": src['name']
        })
    return jobs

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    all_jobs = []
    
    # PRIORITIZE INDUSTRIAL JOBS
    all_jobs.extend(generate_industrial_backup())
    
    # Shuffle to look natural
    random.shuffle(all_jobs)
    
    with open('jobs.json', 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=2)
    
    print(f"✅ SUCCESS: Saved {len(all_jobs)} Industrial & Technical jobs.")
