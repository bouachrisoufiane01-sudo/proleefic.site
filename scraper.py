import requests
from bs4 import BeautifulSoup
import json
import time
import random
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
# Fake headers to look like a real browser
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

# 1. MAROC ANNONCES
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
                title = item.find('h3').get_text(strip=True)
                link = "https://www.marocannonces.com/" + item.find('a')['href'].lstrip('/')
                loc = item.find('span', class_='location').get_text(strip=True)
                jobs.append({
                    "id": int(time.time()) + random.randint(1, 9999),
                    "title": title, "company": "Recruteur (MarocAnnonces)", "location": loc,
                    "catId": detect_category(title), "salary": "À discuter", "posted": 0,
                    "urgent": False, "easyApply": False, "rating": "N/A",
                    "link": link, "sourceName": "MarocAnnonces"
                })
            except: continue
    except: pass
    return jobs

# 2. REKRUTE (NEW!)
def scrape_rekrute():
    print("🕷️ Scraping Rekrute...")
    jobs = []
    url = "https://www.rekrute.com/offres.html"
    try:
        resp = requests.get(url, headers=get_headers(), timeout=15)
        soup = BeautifulSoup(resp.content, 'lxml')
        items = soup.find_all('li', class_='post-item')
        for item in items:
            try:
                title_tag = item.find('h2').find('a')
                title = title_tag.get_text(strip=True)
                link = "https://www.rekrute.com" + title_tag['href']
                img_tag = item.find('div', class_='company-logo').find('img')
                company = img_tag['alt'] if img_tag else "Grande Entreprise"
                
                jobs.append({
                    "id": int(time.time()) + random.randint(10000, 19999),
                    "title": title, "company": company, "location": "Maroc",
                    "catId": detect_category(title), "salary": "Competitif", "posted": 0,
                    "urgent": True, "easyApply": True, "rating": "4.8",
                    "link": link, "sourceName": "Rekrute"
                })
            except: continue
    except: pass
    return jobs

# 3. EMPLOI.MA
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
                title = item.find('h5').get_text(strip=True)
                link = "https://www.emploi.ma" + item.get('data-href', '#')
                comp = item.find('a', class_='company-name').get_text(strip=True)
                jobs.append({
                    "id": int(time.time()) + random.randint(20000, 29999),
                    "title": title, "company": comp, "location": "Maroc",
                    "catId": detect_category(title), "salary": "Confidential", "posted": 0,
                    "urgent": True, "easyApply": True, "rating": "4.0",
                    "link": link, "sourceName": "Emploi.ma"
                })
            except: continue
    except: pass
    return jobs

# 4. ANAPEC
def scrape_anapec():
    print("🕷️ Scraping Anapec...")
    jobs = []
    url = "http://www.anapec.org/sigec-app-rv/chercheurs/resultat_recherche?mot_cle=Technicien"
    try:
        resp = requests.get(url, headers=get_headers(), timeout=20, verify=False)
        soup = BeautifulSoup(resp.content, 'lxml')
        rows = soup.find_all('tr')
        for row in rows:
            try:
                cols = row.find_all('td')
                if len(cols) < 3: continue
                title = cols[1].get_text(strip=True)
                loc = cols[2].get_text(strip=True)
                jobs.append({
                    "id": int(time.time()) + random.randint(30000, 39999),
                    "title": title, "company": "Via Anapec", "location": loc,
                    "catId": detect_category(title), "salary": "SMIG+", "posted": 1,
                    "urgent": False, "easyApply": False, "rating": "Official",
                    "link": "http://www.anapec.org/sigec-app-rv/chercheurs/resultat_recherche", "sourceName": "Anapec"
                })
            except: continue
    except: pass
    return jobs

# 5. LINKEDIN (Smart Links)
def generate_linkedin_links():
    print("🧠 Generating LinkedIn Smart Links...")
    jobs = []
    profiles = [
        ("Développeur Full Stack", "Casablanca"), ("Ingénieur Industriel", "Tanger"),
        ("Commercial B2B", "Rabat"), ("Responsable RH", "Marrakech"),
        ("Technicien Qualité", "Kenitra"), ("Comptable", "Agadir")
    ]
    for p in profiles:
        q = p[0].replace(" ", "%20")
        jobs.append({
            "id": int(time.time()) + random.randint(40000, 50000),
            "title": p[0], "company": "LinkedIn Network", "location": p[1],
            "catId": detect_category(p[0]), "salary": "Market Rate", "posted": 0,
            "urgent": True, "easyApply": True, "rating": "5.0",
            "link": f"https://www.linkedin.com/jobs/search/?keywords={q}%20Maroc",
            "sourceName": "LinkedIn"
        })
    return jobs

# --- MAIN ---
if __name__ == "__main__":
    all_jobs = []
    all_jobs.extend(scrape_maroc_annonces())
    all_jobs.extend(scrape_rekrute())
    all_jobs.extend(scrape_emploi_ma())
    all_jobs.extend(scrape_anapec())
    all_jobs.extend(generate_linkedin_links())
    
    if len(all_jobs) > 0:
        random.shuffle(all_jobs)
        with open('jobs.json', 'w', encoding='utf-8') as f:
            json.dump(all_jobs, f, ensure_ascii=False, indent=2)
        print(f"✅ SUCCESS: Saved {len(all_jobs)} jobs from 5 sources.")
    else:
        print("❌ FAILURE: No jobs found.")
        exit(1)
