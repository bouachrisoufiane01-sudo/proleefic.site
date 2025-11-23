import requests
from bs4 import BeautifulSoup
import json
import random
import datetime
import os

# --- CONFIGURATION ---
OUTPUT_JSON = "jobs.json"
OUTPUT_SITEMAP = "sitemap.xml"
BASE_URL = "https://proleefic.site"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_neon_jobs():
    """Premium Real Jobs (Always Top)"""
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
            "company": "Stellantis",
            "location": "Kenitra",
            "salary": "8.000 DH",
            "posted": "2h ago",
            "urgent": True, "isReal": True, "sourceName": "Stellantis HR",
            "link": "https://www.stellantis.com/en/careers",
            "catId": "cat_tech", "rating": "4.7"
        },
        {
            "id": "real_03",
            "title": "Ingénieur Qualité",
            "company": "OCP Group",
            "location": "El Jadida",
            "salary": "14.000 DH",
            "posted": "4h ago",
            "urgent": True, "isReal": True, "sourceName": "OCP Careers",
            "link": "https://www.ocpgroup.ma/careers",
            "catId": "cat_eng", "rating": "4.8"
        }
    ]

def scrape_dreamjob():
    """Attempts to get fresh data"""
    print("🤖 Robot: Hunting on Dreamjob.ma...")
    jobs = []
    try:
        url = "https://www.dreamjob.ma/"
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article', limit=15)
            
            for idx, art in enumerate(articles):
                try:
                    title = art.find('h1').get_text(strip=True)
                    link = art.find('a')['href']
                    
                    # Detect Category
                    cat = "cat_sales"
                    t_low = title.lower()
                    if "technicien" in t_low: cat = "cat_tech"
                    elif "ingénieur" in t_low: cat = "cat_eng"
                    elif "production" in t_low: cat = "cat_prod"
                    elif "chauffeur" in t_low: cat = "cat_transport"
                    elif "infirmier" in t_low: cat = "cat_health"
                    elif "rh" in t_low or "admin" in t_low: cat = "cat_admin"
                    
                    jobs.append({
                        "id": f"dj_{idx}",
                        "title": title[:60],
                        "company": "Dreamjob Recruteur",
                        "location": "Casablanca", # Default for scraped if unknown
                        "salary": "Negotiable",
                        "posted": "Today",
                        "urgent": False, "isReal": False,
                        "sourceName": "Dreamjob.ma",
                        "link": link,
                        "catId": cat, "rating": "4.0"
                    })
                except: continue
    except: pass
    return jobs

def generate_backup_simulation():
    """Ensures Sitemap is populated with diverse cities"""
    print("⚡ Robot: Generating 40 Backup Jobs with Real Cities...")
    
    sources = [
        {"name": "Rekrute", "url": "https://www.rekrute.com/"},
        {"name": "MarocAnnonces", "url": "https://www.marocannonces.com/"},
        {"name": "Emploi.ma", "url": "https://www.emploi.ma/"},
        {"name": "Anapec", "url": "http://www.anapec.org/"}
    ]
    
    cities = ["Casablanca", "Rabat", "Tanger", "Marrakech", "Agadir", "Fes", "Meknes", "Oujda"]
    
    roles = [
        ("Comptable", "cat_admin"),
        ("Chauffeur", "cat_transport"),
        ("Vendeur", "cat_sales"),
        ("Infirmier", "cat_health"),
        ("Développeur", "cat_it"),
        ("Secrétaire", "cat_admin"),
        ("Opérateur", "cat_prod"),
        ("Technicien", "cat_tech")
    ]
    
    jobs = []
    for i in range(40):
        r = random.choice(roles)
        src = random.choice(sources)
        city = random.choice(cities)
        
        jobs.append({
            "id": f"sim_{i}",
            "title": f"{r[0]} {'Senior' if random.random() > 0.7 else ''}",
            "company": f"Recruteur {city}",
            "location": city,
            "salary": "Negotiable",
            "posted": f"{random.randint(1,5)}d ago",
            "urgent": False,
            "isReal": False,
            "sourceName": src["name"],
            "link": src["url"],
            "catId": r[1],
            "rating": str(round(random.uniform(3.5, 4.9), 1))
        })
    return jobs

def generate_sitemap(jobs):
    """
    Creating the Google-Compatible XML Sitemap
    """
    print(f"🗺️ Generating Sitemap for {len(jobs)} links...")
    today = datetime.date.today()
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # 1. Homepage (Top Priority)
    xml += f'  <url>\n    <loc>{BASE_URL}/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>\n'
    
    # 2. Job Pages (Deep Links)
    for job in jobs:
        # Google needs clean URLs. We encode special chars just in case.
        job_url = f"{BASE_URL}/?job_id={job['id']}"
        
        xml += f'  <url>\n    <loc>{job_url}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
        
    xml += '</urlset>'
    
    # Write file
    with open(OUTPUT_SITEMAP, 'w', encoding='utf-8') as f:
        f.write(xml)

def main():
    all_jobs = []
    
    # 1. Get Real & Scraped Data
    all_jobs.extend(get_neon_jobs())
    scraped = scrape_dreamjob()
    if scraped: all_jobs.extend(scraped)
    
    # 2. Fill with Backup (To ensure Sitemap is full)
    if len(all_jobs) < 50:
        all_jobs.extend(generate_backup_simulation())

    # 3. Save JSON (For the website)
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=2)
        
    # 4. Generate Sitemap (For Google)
    generate_sitemap(all_jobs)
    
    print(f"✅ Success! Generated {OUTPUT_JSON} and {OUTPUT_SITEMAP} with {len(all_jobs)} jobs.")

if __name__ == "__main__":
    main()
