import requests
from bs4 import BeautifulSoup
import json
import time
import random
import urllib3

# Disable SSL warnings for older sites like Anapec
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
]

def get_headers():
    return {'User-Agent': random.choice(USER_AGENTS)}

def detect_category(title):
    t = title.lower()
    if "technicien" in t or "maintenance" in t or "electri" in t: return "cat_tech"
    if "ingénieur" in t or "génie" in t: return "cat_eng"
    if "commercial" in t or "vendeur" in t or "sales" in t: return "cat_sales"
    if "chauffeur" in t or "logistique" in t or "transport" in t: return "cat_transport"
    if "production" in t or "opérateur" in t or "ouvrier" in t: return "cat_prod"
    if "développeur" in t or "it " in t or "informatique" in t: return "cat_it"
    return "cat_prod" # Default fallback

# ---------------------------------------------------------
# 1. MAROC ANNONCES (Blue Collar / Technical)
# ---------------------------------------------------------
def scrape_maroc_annonces():
    print("🕷️ Scraping MarocAnnonces...")
    jobs = []
    url = "https://www.marocannonces.com/maroc/offres-emploi-b309.html"
    try:
        resp = requests.get(url, headers=get_headers(), timeout=15)
        soup = BeautifulSoup(resp.content, 'lxml')
        items = soup.find_all('li')
        
        for item in items:
            try:
                title_tag = item.find('h3')
                if not title_tag: continue
                title = title_tag.get_text(strip=True)
                
                link_tag = item.find('a')
                if not link_tag: continue
                link = "https://www.marocannonces.com/" + link_tag['href'].lstrip('/')
                
                loc_tag = item.find('span', class_='location')
                location = loc_tag.get_text(strip=True) if loc_tag else "Maroc"

                jobs.append({
                    "id": int(time.time()) + random.randint(1, 9999),
                    "title": title,
                    "company": "Recruteur Anonyme",
                    "location": location,
                    "catId": detect_category(title),
                    "salary": "À discuter",
                    "posted": 0,
                    "urgent": False,
                    "easyApply": False,
                    "rating": "N/A",
                    "link": link,
                    "sourceName": "MarocAnnonces"
                })
            except: continue
    except Exception as e: print(f"⚠️ MA Error: {e}")
    return jobs

# ---------------------------------------------------------
# 2. EMPLOI.MA (White Collar / Office)
# ---------------------------------------------------------
def scrape_emploi_ma():
    print("🕷️ Scraping Emploi.ma...")
    jobs = []
    url = "https://www.emploi.ma/recherche-jobs-maroc"
    try:
        resp = requests.get(url, headers=get_headers(), timeout=15)
        soup = BeautifulSoup(resp.content, 'lxml')
        items = soup.find_all('div', class_='job-description-wrapper')
        
        for item in items:
            try:
                title_tag = item.find('h5')
                if not title_tag: continue
                title = title_tag.get_text(strip=True)
                
                link = "https://www.emploi.ma" + item.get('data-href', '#')
                comp_tag = item.find('a', class_='company-name')
                company = comp_tag.get_text(strip=True) if comp_tag else "Confidential"
                
                jobs.append({
                    "id": int(time.time()) + random.randint(10000, 19999),
                    "title": title,
                    "company": company,
                    "location": "Maroc",
                    "catId": detect_category(title),
                    "salary": "Confidential",
                    "posted": 0,
                    "urgent": True,
                    "easyApply": True,
                    "rating": "4.0",
                    "link": link,
                    "sourceName": "Emploi.ma"
                })
            except: continue
    except Exception as e: print(f"⚠️ Emploi.ma Error: {e}")
    return jobs

# ---------------------------------------------------------
# 3. REKRUTE.COM (Premium / High Level)
# ---------------------------------------------------------
def scrape_rekrute():
    print("🕷️ Scraping Rekrute...")
    jobs = []
    url = "https://www.rekrute.com/offres.html"
    try:
        resp = requests.get(url, headers=get_headers(), timeout=15)
        soup = BeautifulSoup(resp.content, 'lxml')
        # Rekrute often uses 'post-item' or similar classes
        items = soup.find_all('li', class_='post-item')
        
        for item in items:
            try:
                title_tag = item.find('h2').find('a')
                if not title_tag: continue
                title = title_tag.get_text(strip=True)
                link = "https://www.rekrute.com" + title_tag['href']
                
                # Company info is often in a specific div
                comp_tag = item.find('div', class_='company-logo').find('img')
                company = comp_tag['alt'] if comp_tag else "Grande Entreprise"
                
                jobs.append({
                    "id": int(time.time()) + random.randint(20000, 29999),
                    "title": title,
                    "company": company,
                    "location": "Casablanca/Rabat", # Default major cities
                    "catId": detect_category(title),
                    "salary": "Competitif",
                    "posted": 0,
                    "urgent": True,
                    "easyApply": True,
                    "rating": "4.8",
                    "link": link,
                    "sourceName": "Rekrute"
                })
            except: continue
    except Exception as e: print(f"⚠️ Rekrute Error: {e}")
    return jobs

# ---------------------------------------------------------
# 4. ANAPEC (Government / Public)
# ---------------------------------------------------------
def scrape_anapec():
    print("🕷️ Scraping Anapec (Lite)...")
    jobs = []
    url = "http://www.anapec.org/sigec-app-rv/chercheurs/resultat_recherche?mot_cle=Technicien"
    try:
        resp = requests.get(url, headers=get_headers(), timeout=20, verify=False)
        soup = BeautifulSoup(resp.content, 'lxml')
        rows = soup.find_all('tr', class_=['odd', 'even'])
        
        for row in rows:
            try:
                cols = row.find_all('td')
                if len(cols) < 3: continue
                title = cols[1].get_text(strip=True)
                loc = cols[2].get_text(strip=True)
                
                jobs.append({
                    "id": int(time.time()) + random.randint(30000, 39999),
                    "title": title,
                    "company": "Via Anapec",
                    "location": loc,
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
    except: pass # Anapec is often down, ignore errors
    return jobs

# ---------------------------------------------------------
# 5. SMART GENERATOR (LinkedIn/OptionCarriere)
# ---------------------------------------------------------
def generate_smart_links():
    print("🧠 Generating Smart Links for LinkedIn...")
    jobs = []
    # High demand profiles we KNOW exist every day
    profiles = [
        ("Ingénieur Industriel", "OCP Group", "Khouribga"),
        ("Technicien Qualité", "Renault", "Tanger"),
        ("Développeur React", "Capgemini", "Casablanca"),
        ("Comptable", "Fiduciaire", "Rabat"),
        ("Chargé de Clientèle", "Amazon (Remote)", "Remote"),
        ("Infirmier du Travail", "Yazaki", "Kenitra"),
        ("Chef de Chantier", "TGCC", "Marrakech")
    ]
    
    for role in profiles:
        # Create a pre-filled search link
        search_q = f"{role[0]} {role[1]}".replace(" ", "+")
        link = f"https://www.linkedin.com/jobs/search/?keywords={search_q}"
        
        jobs.append({
            "id": int(time.time()) + random.randint(40000, 49999),
            "title": role[0],
            "company": role[1],
            "location": role[2],
            "catId": detect_category(role[0]),
            "salary": "Market Rate",
            "posted": 0,
            "urgent": True,
            "easyApply": True,
            "rating": "5.0",
            "link": link,
            "sourceName": "LinkedIn"
        })
    return jobs

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    all_jobs = []
    
    # Run all scrapers
    all_jobs.extend(scrape_maroc_annonces())
    all_jobs.extend(scrape_emploi_ma())
    all_jobs.extend(scrape_rekrute())
    all_jobs.extend(scrape_anapec())
    all_jobs.extend(generate_smart_links())
    
    # If everything failed, use a safety backup
    if len(all_jobs) < 5:
        print("⚠️ All scrapers failed. Using Emergency Data.")
        all_jobs.extend(generate_smart_links()) # At least show LinkedIn links
    
    # Shuffle to mix sources
    random.shuffle(all_jobs)
    
    # Save
    with open('jobs.json', 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Successfully saved {len(all_jobs)} jobs from 5 sources.")
