from bs4 import BeautifulSoup
import requests
import json
import time
import random
import re

# --- CONFIGURATION ---
OUTPUT_FILE = "jobs.json"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://www.google.com/'
}

# --- 1. INTELLIGENCE (Helpers) ---

MOROCCAN_CITIES = [
    "Casablanca", "Rabat", "Tanger", "Marrakech", "Agadir", "Fès", "Fes",
    "Meknès", "Oujda", "Kenitra", "Tetouan", "Laayoune", "Dakhla", 
    "Mohammedia", "Salé", "El Jadida", "Bouskoura", "Nouaceur", "Berrechid"
]

CATEGORIES_MAP = {
    "cat_tech": ["technicien", "mécanicien", "electricien", "maintenance", "industriel", "froid", "ouvrier", "soudeur"],
    "cat_prod": ["production", "qualité", "usine", "opérateur", "chef d'équipe", "manufacturing", "câblage"],
    "cat_sales": ["commercial", "vendeur", "sales", "vente", "magasinier", "comptoir"],
    "cat_admin": ["comptable", "assistante", "secrétaire", "rh", "ressources humaines", "office", "réception"],
    "cat_call": ["centre d'appel", "téléconseiller", "francophone", "chargé de clientèle", "bilingue"],
    "cat_it": ["développeur", "informatique", "devops", "full stack", "java", "php", "système", "réseau"],
    "cat_transport": ["chauffeur", "livreur", "coursier", "transport", "logistique", "permis"],
    "cat_health": ["infirmier", "infirmière", "médecin", "pharmacie", "santé", "clinique"],
    "cat_edu": ["enseignant", "professeur", "éducatrice", "français", "anglais", "crèche"]
}

def extract_city(text_content):
    """Finds a city in a text, defaults to 'Maroc'."""
    if not text_content: return "Maroc"
    text_lower = text_content.lower()
    for city in MOROCCAN_CITIES:
        if city.lower() in text_lower:
            return city
    return "Maroc"

def detect_category(title):
    """Auto-assigns a category ID based on keywords in the title."""
    title_lower = title.lower()
    for cat_id, keywords in CATEGORIES_MAP.items():
        for keyword in keywords:
            if keyword in title_lower:
                return cat_id
    return "cat_admin" # Default fallback

# --- 2. THE SOURCES ---

def get_direct_jobs():
    """Your High-Priority 'Premium' Listings"""
    print("⚡ Adding Direct Hiring Offers...")
    return [
        {
            "id": "d_01", "title": "Responsable Production (Câblage)", "company": "Yazaki Tanger", "location": "Tanger",
            "salary": "12.000 DH", "posted": "1h", "urgent": True, "isReal": True, "isDirect": True,
            "sourceName": "Direct HR", "email": "rh.tanger@yazaki-group.com", "catId": "cat_prod",
            "reqs": ["Bac+5 Ingénieur", "5 ans expérience", "Anglais courant"]
        },
        {
            "id": "d_02", "title": "Vendeur Showroom", "company": "Marjane Market", "location": "Casablanca",
            "salary": "4.000 DH", "posted": "2h", "urgent": True, "isReal": True, "isDirect": True,
            "sourceName": "Direct HR", "email": "recrutement@marjane.co.ma", "catId": "cat_sales",
            "reqs": ["Niveau Bac", "Bonne présentation", "Dynamique"]
        }
    ]

def scrape_marocannonces():
    """
    TARGET: MarocAnnonces (Huge for technicians/blue collar)
    """
    print("🔍 Scraping MarocAnnonces...")
    jobs = []
    try:
        # Focusing on the "Job Offers" category
        url = "https://www.marocannonces.com/maroc/offres-emploi-domaine-b309.html"
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Their list is usually in <ul class="cars-list">
        listings = soup.find_all('li', attrs={'itemtype': 'http://schema.org/Product'})
        
        for idx, item in enumerate(listings):
            try:
                title_tag = item.find('h3')
                if not title_tag: continue
                
                title = title_tag.get_text(strip=True)
                link = "https://www.marocannonces.com/" + item.find('a')['href']
                
                # City is often in a specific span or div
                location_tag = item.find('span', class_='location')
                raw_loc = location_tag.get_text(strip=True) if location_tag else ""
                city = extract_city(raw_loc)
                if city == "Maroc": city = extract_city(title) # Try title if loc fails

                jobs.append({
                    "id": f"ma_{idx}",
                    "title": title,
                    "company": "Confidential", # MarocAnnonces often hides company names
                    "location": city,
                    "salary": "A discuter",
                    "posted": "Auj.",
                    "urgent": False, "isReal": True, "isDirect": False,
                    "sourceName": "MarocAnnonces",
                    "link": link,
                    "catId": detect_category(title)
                })
            except: continue
    except Exception as e:
        print(f"⚠️ MarocAnnonces Error: {e}")
    return jobs

def scrape_emploi_ma():
    """
    TARGET: Emploi.ma (The "Emploitic" of Morocco)
    """
    print("🔍 Scraping Emploi.ma...")
    jobs = []
    try:
        url = "https://www.emploi.ma/recherche-jobs-maroc"
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for job cards
        cards = soup.find_all('div', class_='job-description-wrapper')
        
        for idx, card in enumerate(cards):
            try:
                # Title
                title_tag = card.find('h5')
                if not title_tag: continue
                title = title_tag.get_text(strip=True)
                
                # Link
                link_tag = title_tag.find('a')
                link = "https://www.emploi.ma" + link_tag['href'] if link_tag else "#"
                
                # Company
                company_tag = card.find('a', class_='company-name')
                company = company_tag.get_text(strip=True) if company_tag else "Entreprise"
                
                # Location (Text search in the card)
                full_text = card.get_text(separator=" ")
                city = extract_city(full_text)

                jobs.append({
                    "id": f"emp_{idx}",
                    "title": title,
                    "company": company,
                    "location": city,
                    "salary": "N/A",
                    "posted": "Recent",
                    "urgent": False, "isReal": True, "isDirect": False,
                    "sourceName": "Emploi.ma",
                    "link": link,
                    "catId": detect_category(title)
                })
            except: continue
    except Exception as e:
        print(f"⚠️ Emploi.ma Error: {e}")
    return jobs

def scrape_rekrute():
    """
    TARGET: Rekrute.com (Corporate jobs)
    """
    print("🔍 Scraping Rekrute...")
    jobs = []
    try:
        url = "https://www.rekrute.com/offres.html"
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        items = soup.find_all('li', class_='post-id')
        
        for idx, item in enumerate(items):
            try:
                title_tag = item.find('h2') or item.find('a', class_='titreJob')
                if not title_tag: continue
                title = title_tag.get_text(strip=True)
                
                link = "https://www.rekrute.com" + item.find('a', class_='titreJob')['href']
                
                # Image/Company
                img_tag = item.find('img', class_='photo')
                company = img_tag['alt'] if img_tag else "Rekrute Client"
                
                # Location info usually in text
                info_text = item.get_text(separator=" ")
                city = extract_city(info_text)

                jobs.append({
                    "id": f"rek_{idx}",
                    "title": title,
                    "company": company,
                    "location": city,
                    "salary": "N/A",
                    "posted": "Active",
                    "urgent": False, "isReal": True, "isDirect": False,
                    "sourceName": "Rekrute",
                    "link": link,
                    "catId": detect_category(title)
                })
            except: continue
    except Exception as e:
        print(f"⚠️ Rekrute Error: {e}")
    return jobs

# --- 3. MAIN EXECUTION ---

def main():
    print("🤖 Proleefic Bot Started...")
    all_jobs = []

    # 1. Direct Jobs (Always first)
    all_jobs.extend(get_direct_jobs())

    # 2. Scrape Real Sources
    # We add delays to be polite and avoid blocking
    all_jobs.extend(scrape_marocannonces())
    time.sleep(2) 
    all_jobs.extend(scrape_emploi_ma())
    time.sleep(2)
    all_jobs.extend(scrape_rekrute())

    # 3. Save
    print(f"💾 Saving {len(all_jobs)} REAL jobs to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=2)
    
    print("✅ DONE! You have real data now.")

if __name__ == "__main__":
    main()
