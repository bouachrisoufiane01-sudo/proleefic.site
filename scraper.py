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

def get_headers():
    return {'User-Agent': random.choice(USER_AGENTS)}

def detect_category(title):
    t = title.lower()
    if "technicien" in t or "maintenance" in t or "electricien" in t: return "cat_tech"
    if "ingénieur" in t or "génie" in t or "qualité" in t: return "cat_eng"
    if "commercial" in t or "vendeur" in t or "vente" in t: return "cat_sales"
    if "chauffeur" in t or "logistique" in t: return "cat_transport"
    if "production" in t or "opérateur" in t or "usine" in t or "câblage" in t: return "cat_prod"
    if "développeur" in t or "it " in t or "informatique" in t: return "cat_it"
    if "agent de centre" in t or "téléconseiller" in t: return "cat_call"
    if "infirmier" in t or "médecin" in t or "santé" in t: return "cat_health"
    if "hôtellerie" in t or "réceptionniste" in t or "cuisine" in t: return "cat_hotel"
    if "professeur" in t or "enseignant" in t: return "cat_edu"
    return "cat_prod"

# --- SMART GENERATOR (Backup and Smart Links) ---
def generate_jobs():
    print("🏭 Generating Industrial & Diverse Jobs...")
    jobs = []
    
    roles = [
        ("Opérateur Câblage", "cat_prod", "Tanger"), ("Technicien Maintenance", "cat_tech", "Kenitra"),
        ("Chauffeur Personnel", "cat_transport", "Casa"), ("Infirmier", "cat_health", "Rabat"),
        ("Agent de Centre d'Appel", "cat_call", "Casablanca"), ("Professeur Français", "cat_edu", "Fes")
    ]
    companies = ["Renault", "Yazaki", "OCP", "Particulier", "Société", "Attijariwafa", "Orange"]
    sources = [
        {"name": "LinkedIn", "url": "https://www.linkedin.com/jobs/search/?keywords={}+Maroc"},
        {"name": "Rekrute", "url": "https://www.rekrute.com/offres-emploi-maroc.html?keyword={}"},
        {"name": "MarocAnnonces", "url": "https://www.marocannonces.com/maroc/offres-emploi-b309.html?kw={}"}
    ]

    for i in range(50):
        r = random.choice(roles)
        comp = random.choice(companies)
        src = random.choice(sources)
        
        q = r[0].replace(" ", "+")
        link = src["url"].format(q)
        
        jobs.append({
            "id": i + 1,
            "title": r[0],
            "company": comp,
            "location": r[2],
            "catId": r[1],
            "salary": f"{random.randint(4000, 8000)} MAD",
            "posted": random.randint(0, 3),
            "urgent": random.random() > 0.8,
            "rating": round(random.uniform(3.7, 5.0), 1), # Random rating fix
            "link": link,
            "sourceName": src["name"]
        })
        
    return jobs

# --- MAIN ---
if __name__ == "__main__":
    try:
        data = generate_jobs()
        with open('jobs.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved {len(data)} jobs.")
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        sys.exit(1)
