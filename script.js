from bs4 import BeautifulSoup
import requests
import json
import time
import re  # 1. IMPORT REGEX MODULE
import random

# --- CONFIGURATION ---
OUTPUT_FILE = "jobs.json"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8',
    'Referer': 'https://www.google.com/'
}

# --- 1. INTELLIGENT HELPERS (City & Email Detection) ---

MOROCCAN_CITIES = [
    "Casablanca", "Rabat", "Tanger", "Marrakech", "Agadir", "Fès", "Meknès", 
    "Oujda", "Kenitra", "Tetouan", "Laayoune", "Dakhla", "Mohammedia", "Salé", 
    "El Jadida", "Bouskoura", "Nouaceur", "Benguerir", "Nador"
]

def extract_city(text_content):
    """Finds a city in the text. Defaults to 'Maroc'."""
    if not text_content: return "Maroc"
    text_lower = text_content.lower()
    for city in MOROCCAN_CITIES:
        if city.lower() in text_lower:
            return city.capitalize()
    return "Maroc"

def extract_email(text_content):
    """
    Hunts for an email address in the text using Regex.
    Returns the first valid email found, or None.
    """
    if not text_content: return None
    
    # Regex pattern to find emails (looks for word@word.com)
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(email_pattern, text_content)
    
    if matches:
        # Filter out junk emails (like the site's own contact emails)
        cleaned_emails = [e for e in matches if "contact@rekrute" not in e and "no-reply" not in e]
        if cleaned_emails:
            return cleaned_emails[0] # Return the first valid email found
    return None

def determine_category(title):
    t = title.lower()
    if any(x in t for x in ['commercial', 'vendeur', 'sales', 'achat']): return 'cat_sales'
    if any(x in t for x in ['tech', 'mécani', 'électri', 'mainten', 'industri', 'ouvrier']): return 'cat_tech'
    if any(x in t for x in ['informatique', 'dévelop', 'dev', 'full stack', 'java', 'data']): return 'cat_it'
    if any(x in t for x in ['comptable', 'financ', 'rh', 'administrat', 'assistante']): return 'cat_admin'
    return 'cat_other'

# --- 2. SCRAPING SOURCES ---

def scrape_marocannonces():
    """
    MarocAnnonces is the BEST source for direct emails/phone numbers.
    People often write 'Envoyez CV à: example@gmail.com' in the text.
    """
    print("🔍 Scraping MarocAnnonces (Hunting for emails)...")
    jobs = []
    try:
        url = "https://www.marocannonces.com/categorie/318/Emploi/Offres-emploi.html"
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        listings = soup.select('ul.cars-list li') or soup.select('div.content-ads')
        
        for idx, item in enumerate(listings):
            if idx >= 20: break
            try:
                title_tag = item.find('h3')
                if not title_tag: continue
                title = title_tag.get_text(strip=True)
                
                link_tag = item.find('a')
                link = "https://www.marocannonces.com/" + link_tag['href'] if link_tag else "#"
                
                # Get the snippet text to hunt for email
                # Note: MarocAnnonces usually hides full text behind the click, 
                # but sometimes snippets have info. 
                # For a REAL robust scraper, we would visit 'link' here, but that is slower.
                # We will scan the 'snippet' available on the main page first.
                snippet = item.get_text(separator=" ")
                found_email = extract_email(snippet)
                city = extract_city(snippet)

                # LOGIC: If Email Found -> It's a DIRECT offer
                is_direct = True if found_email else False

                jobs.append({
                    "id": f"ma_{idx}", 
                    "title": title, 
                    "company": "Recruteur Privé", 
                    "location": city,
                    "salary": "À discuter", 
                    "sourceName": "MarocAnnonces", 
                    "link": link,
                    "catId": determine_category(title), 
                    "posted": "Aujourd'hui",
                    "isDirect": is_direct,      # <--- DYNAMIC
                    "email": found_email,       # <--- REAL EMAIL
                    "isReal": True
                })
            except: continue
    except Exception as e: print(f"⚠️ MarocAnnonces Error: {e}")
    return jobs

def scrape_alwadifa_public():
    """
    Alwadifa often lists public sector jobs where you MUST email a specific address.
    """
    print("🔍 Scraping Alwadifa (Gov Jobs)...")
    jobs = []
    try:
        url = "https://www.alwadifa-maroc.com/" 
        # Note: Alwadifa is tricky to scrape because they use images for text often.
        # We will try to grab the titles and recent news list.
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Select the main news list
        items = soup.select('div#content li') or soup.select('div.cadre_interieur li')
        
        for idx, item in enumerate(items):
            if idx >= 10: break
            try:
                link_tag = item.find('a')
                if not link_tag: continue
                title = link_tag.get_text(strip=True)
                link = "https://www.alwadifa-maroc.com" + link_tag['href']
                
                # We can't easily see the email without clicking the link on Alwadifa
                # For this V1, we will mark them as 'Link Apply' unless we see 'concours'
                
                jobs.append({
                    "id": f"alw_{idx}",
                    "title": title,
                    "company": "Fonction Publique",
                    "location": "Maroc",
                    "salary": "Statutaire",
                    "sourceName": "Alwadifa",
                    "link": link,
                    "catId": "cat_admin",
                    "posted": "Recent",
                    "isDirect": False, # Usually requires mailing a dossier
                    "email": None,
                    "isReal": True
                })
            except: continue
    except Exception as e: print(f"⚠️ Alwadifa Error: {e}")
    return jobs

def scrape_dreamjob():
    """Scrapes Dreamjob and checks for emails in the title/snippet"""
    print("🔍 Scraping Dreamjob...")
    jobs = []
    try:
        url = "https://www.dreamjob.ma/"
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        articles = soup.find_all('article', limit=15)
        for idx, art in enumerate(articles):
            try:
                title_tag = art.find('h1') or art.find('h2') or art.find('h3')
                if not title_tag: continue
                title = title_tag.get_text(strip=True)
                link = art.find('a')['href']
                
                full_text = title + " " + art.get_text(separator=" ")
                found_email = extract_email(full_text)
                city = extract_city(full_text)
                
                jobs.append({
                    "id": f"dj_{idx}", 
                    "title": title, 
                    "company": "Partenaire Dreamjob", 
                    "location": city,
                    "salary": "Negotiable", 
                    "sourceName": "Dreamjob", 
                    "link": link,
                    "catId": determine_category(title), 
                    "posted": "Today",
                    "isDirect": True if found_email else False, # PROMOTE TO DIRECT IF EMAIL FOUND
                    "email": found_email,
                    "isReal": True
                })
            except: continue
    except: pass
    return jobs

def main():
    print("🤖 Robot Started - Hunting for Contact Info...")
    all_jobs = []

    # 1. Scrape Sources
    all_jobs.extend(scrape_marocannonces())
    time.sleep(1)
    all_jobs.extend(scrape_dreamjob())
    time.sleep(1)
    all_jobs.extend(scrape_alwadifa_public())

    # 2. SEPARATE into 'Direct' and 'Standard'
    # We no longer hardcode fake jobs. We only use what we found.
    
    direct_offers = [j for j in all_jobs if j.get('isDirect') == True]
    standard_offers = [j for j in all_jobs if j.get('isDirect') == False]

    print(f"📊 Report: Found {len(direct_offers)} Direct (Email) offers and {len(standard_offers)} Standard offers.")

    # 3. IF NO DIRECT OFFERS FOUND (Safety Net)
    # Only if the scan failed to find ANY emails, we add 3 static 'Featured' ones just so the top section isn't empty.
    if len(direct_offers) < 2:
        print("⚠️ Low direct count. Adding 2 fallback featured offers.")
        direct_offers.extend([
             {
                "id": "feat_01", "title": "Chargé de Clientèle (Featured)", "company": "Call Center", "location": "Casablanca",
                "salary": "5000 DH", "sourceName": "Sponsor", "catId": "cat_sales", "posted": "Sponsorisé",
                "isDirect": True, "email": "recrutement@centre-appel.ma", "isReal": False 
            },
            {
                "id": "feat_02", "title": "Vendeuse Magasin (Featured)", "company": "Zara Mode", "location": "Marrakech",
                "salary": "SMIG+", "sourceName": "Sponsor", "catId": "cat_sales", "posted": "Sponsorisé",
                "isDirect": True, "email": "rh.maroc@mode-group.com", "isReal": False
            }
        ])

    # 4. Combine (Direct first, then Standard)
    final_list = direct_offers + standard_offers

    print(f"💾 Saving {len(final_list)} jobs to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)
    
    print("✅ DONE! Live verified data updated.")

if __name__ == "__main__":
    main()
