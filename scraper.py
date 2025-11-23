import requests
from bs4 import BeautifulSoup
import json
import random
import time
from datetime import datetime

# --- CONFIGURATION ---
OUTPUT_FILE = "jobs.json"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_neon_jobs():
    """These are the 3 Hardcoded 'Premium' Jobs with RED NEON"""
    return [
        {
            "id": "real_01",
            "title": "Responsable Production (Câblage)",
            "company": "Yazaki Tanger",
            "location": "Tanger",
            "salary": "12.000 DH",
            "posted": "1h ago",
            "urgent": True, 
            "isReal": True,  # Triggers Neon
            "sourceName": "Yazaki Careers",
            "link": "https://www.linkedin.com/company/yazaki-morocco",
            "catId": "cat_prod",
            "rating": "4.9"
        },
        {
            "id": "real_02",
            "title": "Technicien Maintenance Senior",
            "company": "Stellantis",
            "location": "Kenitra",
            "salary": "8.000 DH",
            "posted": "2h ago",
            "urgent": True,
            "isReal": True,
            "sourceName": "Stellantis HR",
            "link": "https://www.stellantis.com/en/careers",
            "catId": "cat_tech",
            "rating": "4.7"
        },
        {
            "id": "real_03",
            "title": "Ingénieur Qualité",
            "company": "OCP Group",
            "location": "Jorf Lasfar",
            "salary": "14.000 DH",
            "posted": "4h ago",
            "urgent": True,
            "isReal": True,
            "sourceName": "OCP Careers",
            "link": "https://www.ocpgroup.ma/careers",
            "catId": "cat_eng",
            "rating": "4.8"
        }
    ]

def scrape_dreamjob():
    """Scrapes Real Jobs from Dreamjob.ma"""
    print("🤖 Robot: Connecting to Dreamjob.ma...")
    jobs = []
    try:
        # We scrape the main feed
        url = "https://www.dreamjob.ma/"
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find all article links
            articles = soup.find_all('article', limit=15)
            
            for idx, art in enumerate(articles):
                try:
                    # Extract Title
                    title_tag = art.find('h1') or art.find('h2') or art.find('h3')
                    if not title_tag: continue
                    
                    title = title_tag.get_text(strip=True)
                    
                    # Extract Link (The most important part)
                    link_tag = art.find('a')
                    real_link = link_tag['href'] if link_tag else f"https://www.google.com/search?q={title}+Maroc"
                    
                    # Determine Category (Simple logic)
                    cat = "cat_sales" # Default
                    if "technicien" in title.lower(): cat = "cat_tech"
                    elif "ingénieur" in title.lower(): cat = "cat_eng"
                    elif "chauffeur" in title.lower(): cat = "cat_transport"
                    elif "production" in title.lower(): cat = "cat_prod"

                    job = {
                        "id": f"dj_{idx}",
                        "title": title[:60], # Shorten title
                        "company": "Dreamjob Recruteur",
                        "location": "Maroc",
                        "salary": "Negotiable",
                        "posted": "Today",
                        "urgent": False, # Scraped jobs are NOT urgent
                        "isReal": False, # No Neon for scraped
                        "sourceName": "Dreamjob.ma",
                        "link": real_link, # <--- THIS FIXES THE APPLY BUTTON
                        "catId": cat,
                        "rating": "4.0"
                    }
                    jobs.append(job)
                except:
                    continue
            print(f"✅ Successfully scraped {len(jobs)} jobs from Dreamjob.")
    except Exception as e:
        print(f"⚠️ Scraping failed: {e}")
        # If scraping fails, we fallback to simulation so site isn't empty
        return generate_simulation()
    
    if len(jobs) == 0: return generate_simulation()
    return jobs

def generate_simulation():
    """Fallback: Generates jobs if website is blocked"""
    print("⚡ Robot: Generating Smart Backup Jobs...")
    roles = [
        ("Comptable Confirmé", "Fiduciaire Leader", "Casablanca"),
        ("Vendeuse Showroom", "Zara Home", "Marrakech"),
        ("Chauffeur Livreur", "Jumia Logistics", "Tanger"),
        ("Infirmier Polyvalent", "Clinique Sud", "Agadir")
    ]
    data = []
    for i, r in enumerate(roles):
        # SMART LINK: Creates a working Google Search link
        smart_link = f"https://www.google.com/search?q={r[0].replace(' ', '+')}+{r[1].replace(' ', '+')}+Maroc"
        
        data.append({
            "id": f"sim_{i}",
            "title": r[0],
            "company": r[1],
            "location": r[2],
            "salary": "Confidential",
            "posted": "1d ago",
            "urgent": False,
            "isReal": False,
            "sourceName": "Rekrute.com",
            "link": smart_link, # <--- Valid Link
            "catId": "cat_sales",
            "rating": "3.5"
        })
    return data

def main():
    print("🚀 Proleefic Robot Starting...")
    all_jobs = []
    
    # 1. Add the 3 Neon Jobs (Real)
    all_jobs.extend(get_neon_jobs())
    
    # 2. Add Scraped Jobs (Dreamjob)
    all_jobs.extend(scrape_dreamjob())
    
    # 3. Save
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=2)
    print("✅ jobs.json updated successfully.")

if __name__ == "__main__":
    main()
