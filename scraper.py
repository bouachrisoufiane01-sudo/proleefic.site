import requests
from bs4 import BeautifulSoup
import json
import time
import random
import urllib3
from fake_useragent import UserAgent

# 1. Setup Stealth Config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ua = UserAgent()

def get_real_browser_headers():
    # This makes the robot look EXACTLY like a real person using Chrome
    return {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }

def detect_category(title):
    t = title.lower()
    if "technicien" in t or "maintenance" in t or "mécanique" in t: return "cat_tech"
    if "ingénieur" in t or "génie" in t: return "cat_eng"
    if "commercial" in t or "vendeur" in t or "sales" in t: return "cat_sales"
    if "chauffeur" in t or "logistique" in t or "transport" in t: return "cat_transport"
    if "production" in t or "opérateur" in t or "ouvrier" in t: return "cat_prod"
    if "développeur" in t or "it " in t or "informatique" in t: return "cat_it"
    return "cat_prod"

# --- SOURCE 1: MAROC ANNONCES (Stealth Mode) ---
def scrape_maroc_annonces():
    print("🕷️ Visiting MarocAnnonces...")
    jobs = []
    url = "https://www.marocannonces.com/maroc/offres-emploi-b309.html"
    
    try:
        session = requests.Session()
        response = session.get(url, headers=get_real_browser_headers(), timeout=20)
        
        if response.status_code != 200:
            print(f"❌ MA Blocked: Status {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, 'lxml')
        
        # Try 2 different selectors in case they changed the site
        items = soup.select('ul.cars-list li') or soup.select('.annonce_list li')
        
        print(f"   -> Found {len(items)} items in HTML.")

        for item in items:
            try:
                title_tag = item.find('h3')
                if not title_tag: continue
                title = title_tag.get_text(strip=True)
                
                link_tag = item.find('a')
                if not link_tag: continue
                href = link_tag['href']
                full_link = "https://www.marocannonces.com/" + href.lstrip('/')
                
                loc_tag = item.find('span', class_='location')
                location = loc_tag.get_text(strip=True) if loc_tag else "Maroc"

                jobs.append({
                    "id": int(time.time()) + random.randint(1, 10000),
                    "title": title,
                    "company": "Recruteur (MarocAnnonces)",
                    "location": location,
                    "catId": detect_category(title),
                    "salary": "À discuter",
                    "posted": 0,
                    "urgent": False,
                    "easyApply": False,
                    "rating": "N/A",
                    "link": full_link,
                    "sourceName": "MarocAnnonces"
                })
            except: continue
    except Exception as e:
        print(f"❌ MA Error: {e}")
        
    return jobs

# --- SOURCE 2: EMPLOI.MA (Stealth Mode) ---
def scrape_emploi_ma():
    print("🕷️ Visiting Emploi.ma...")
    jobs = []
    url = "https://www.emploi.ma/recherche-jobs-maroc"
    
    try:
        session = requests.Session()
        response = session.get(url, headers=get_real_browser_headers(), timeout=20)
        
        if response.status_code != 200:
            print(f"❌ Emploi.ma Blocked: Status {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, 'lxml')
        
        # Try specific job card selector
        items = soup.select('div.job-description-wrapper') or soup.select('.views-row')

        print(f"   -> Found {len(items)} items in HTML.")

        for item in items:
            try:
                title_tag = item.find('h5')
                if not title_tag: continue
                title = title_tag.get_text(strip=True)
                
                link = "https://www.emploi.ma" + item.get('data-href', '#')
                
                comp_tag = item.find('a', class_='company-name')
                company = comp_tag.get_text(strip=True) if comp_tag else "Confidential"
                
                jobs.append({
                    "id": int(time.time()) + random.randint(20000, 30000),
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
    except Exception as e:
        print(f"❌ Emploi.ma Error: {e}")

    return jobs

# --- SOURCE 3: ANAPEC (The Backup) ---
def scrape_anapec():
    print("🕷️ Visiting Anapec...")
    jobs = []
    # Search for a broad term to get results
    url = "http://www.anapec.org/sigec-app-rv/chercheurs/resultat_recherche?mot_cle=Technicien"
    try:
        # Anapec needs verification disabled
        response = requests.get(url, headers=get_real_browser_headers(), timeout=20, verify=False)
        soup = BeautifulSoup(response.content, 'lxml')
        rows = soup.find_all('tr')
        
        for row in rows:
            try:
                cols = row.find_all('td')
                if len(cols) < 3: continue
                title = cols[1].get_text(strip=True)
                loc = cols[2].get_text(strip=True)
                
                jobs.append({
                    "id": int(time.time()) + random.randint(40000, 50000),
                    "title": title,
                    "company": "Anapec / État",
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
    except: pass
    return jobs

# --- MAIN ---
if __name__ == "__main__":
    all_jobs = []
    
    # Run Scrapers
    all_jobs.extend(scrape_maroc_annonces())
    all_jobs.extend(scrape_emploi_ma())
    all_jobs.extend(scrape_anapec())
    
    # SAFETY: Only save if we found jobs. If blocked, don't overwrite file with empty list.
    if len(all_jobs) > 5:
        random.shuffle(all_jobs)
        with open('jobs.json', 'w', encoding='utf-8') as f:
            json.dump(all_jobs, f, ensure_ascii=False, indent=2)
        print(f"✅ SUCCESS: Saved {len(all_jobs)} REAL jobs.")
    else:
        print("⚠️ BLOCKED OR EMPTY. Not updating file (keeping yesterday's jobs).")
        exit(1) # Fail the action so you get a red notification
