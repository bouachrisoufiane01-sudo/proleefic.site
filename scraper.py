import json
import random
import datetime
import os

# Try to import tools. If missing, we switch to "Backup Mode" automatically.
try:
    import requests
    from bs4 import BeautifulSoup
    TOOLS_AVAILABLE = True
except ImportError:
    print("⚠️ Tools (requests/bs4) not installed. Running in SAFE MODE.")
    TOOLS_AVAILABLE = False

# --- CONFIGURATION ---
OUTPUT_JSON = "jobs.json"
OUTPUT_SITEMAP = "sitemap.xml"
BASE_URL = "https://proleefic.site"

def get_neon_jobs():
    """Your Hardcoded Premium Jobs"""
    return [
        {
            "id": "real_01",
            "title": "Responsable Production (Câblage)",
            "company": "Yazaki Tanger",
            "location": "Tanger",
            "salary": "12.000 DH",
            "posted": "1h ago",
            "urgent": True, "isReal": True, "sourceName": "Yazaki Careers",
            "link": "https://www.linkedin.com/company/yazaki-morocco",
            "catId": "cat_prod", "rating": "4.9"
        },
        {
            "id": "real_02",
            "title": "Technicien Maintenance Senior",
            "company": "Stellantis Kenitra",
            "location": "Kenitra",
            "salary": "8.000 DH",
            "posted": "2h ago",
            "urgent": True, "isReal": True, "sourceName": "Stellantis HR",
            "link": "https://www.stellantis.com/en/careers",
            "catId": "cat_tech", "rating": "4.7"
        }
    ]

def scrape_dreamjob():
    if not TOOLS_AVAILABLE: return []
    
    print("🤖 Robot: Connecting to Dreamjob.ma...")
    jobs = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get("https://www.dreamjob.ma/", headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ Blocked by website (Status {response.status_code}).")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article', limit=15)
        
        for idx, art in enumerate(articles):
            try:
                title_tag = art.find('h1') or art.find('h2')
                if not title_tag: continue
                
                link_tag = art.find('a')
                real_link = link_tag['href'] if link_tag else "#"
                
                jobs.append({
                    "id": f"dj_{idx}",
                    "title": title_tag.get_text(strip=True)[:60],
                    "company": "Dreamjob Recruteur",
                    "location": "Maroc",
                    "salary": "Negotiable",
                    "posted": "Today",
                    "urgent": False, "isReal": False,
                    "sourceName": "Dreamjob.ma",
                    "link": real_link,
                    "catId": "cat_sales", "rating": "4.0"
                })
            except: continue
    except Exception as e:
        print(f"⚠️ Scraping Warning: {e}")
        
    return jobs

def generate_backup():
    """Fills the file if scraping fails so the site is never empty"""
    print("⚡ Robot: Generating Backup Jobs...")
    roles = [("Comptable", "Fiduciaire"), ("Vendeur", "Zara"), ("Chauffeur", "Transport MA")]
    jobs = []
    for i, r in enumerate(roles):
        jobs.append({
            "id": f"bk_{i}",
            "title": r[0], "company": r[1], "location": "Casablanca",
            "salary": "Confidential", "posted": "1d ago",
            "urgent": False, "isReal": False, "sourceName": "Rekrute",
            "link": f"https://www.google.com/search?q={r[0]}+job",
            "catId": "cat_sales", "rating": "3.5"
        })
    return jobs

def main():
    print("🚀 Proleefic Robot Started...")
    all_jobs = []
    
    # 1. Get Neon Jobs
    all_jobs.extend(get_neon_jobs())
    
    # 2. Try Scraping
    scraped = scrape_dreamjob()
    if scraped:
        print(f"✅ Scraped {len(scraped)} jobs.")
        all_jobs.extend(scraped)
    else:
        print("⚠️ Scraping returned 0 jobs. Using Backup.")
        all_jobs.extend(generate_backup())

    # 3. Save JSON
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=2)
        
    # 4. Create Sitemap
    with open(OUTPUT_SITEMAP, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        for job in all_jobs:
            f.write(f'<url><loc>{BASE_URL}/?job_id={job["id"]}</loc></url>')
        f.write('</urlset>')

    print("✅ SUCCESS: Files updated.")

if __name__ == "__main__":
    main()
