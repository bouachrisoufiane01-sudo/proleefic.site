import requests
from bs4 import BeautifulSoup
import json
import random
import datetime

# CONFIGURATION
OUTPUT_JSON = "jobs.json"
OUTPUT_SITEMAP = "sitemap.xml" # <-- NEW: Google needs this
BASE_URL = "https://proleefic.site" # Change this to your real domain if different

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_neon_jobs():
    """Hardcoded Premium Jobs (Always top)"""
    return [
        {
            "id": "real_01",
            "title": "Responsable Production (Câblage)",
            "company": "Yazaki Tanger",
            "location": "Tanger",
            "salary": "12.000 DH",
            "posted": "1h ago",
            "urgent": True, 
            "isReal": True, 
            "sourceName": "Yazaki Careers",
            "link": "https://www.linkedin.com/company/yazaki-morocco",
            "catId": "cat_prod",
            "rating": "4.9"
        },
        {
            "id": "real_02",
            "title": "Technicien Maintenance",
            "company": "Stellantis Kenitra",
            "location": "Kenitra",
            "salary": "8.000 DH",
            "posted": "2h ago",
            "urgent": True,
            "isReal": True,
            "sourceName": "Stellantis HR",
            "link": "https://www.stellantis.com/en/careers",
            "catId": "cat_tech",
            "rating": "4.7"
        }
    ]

def scrape_dreamjob():
    print("🤖 Robot: Hunting on Dreamjob.ma...")
    jobs = []
    try:
        url = "https://www.dreamjob.ma/"
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Adjust selector for their current layout
        articles = soup.find_all('article', limit=15)
        
        for idx, art in enumerate(articles):
            try:
                title_tag = art.find('h1') or art.find('h2') or art.find('h3')
                if not title_tag: continue
                
                title = title_tag.get_text(strip=True)
                link_tag = art.find('a')
                real_link = link_tag['href'] if link_tag else "#"
                
                job = {
                    "id": f"dj_{idx}",
                    "title": title[:60],
                    "company": "Recrutement Maroc",
                    "location": "Maroc",
                    "salary": "Negotiable",
                    "posted": "Today",
                    "urgent": False,
                    "isReal": False,
                    "sourceName": "Dreamjob.ma",
                    "link": real_link,
                    "catId": "cat_sales", # Default category
                    "rating": "4.0"
                }
                jobs.append(job)
            except: continue
    except Exception as e:
        print(f"⚠️ Scraping error: {e}")
    
    # Fallback if scraping fails (so file isn't empty)
    if not jobs:
        print("⚡ Using backup generator for scraped data...")
        jobs = [
            {"id": "bk_1", "title": "Chauffeur Livreur", "company": "Transport MA", "location": "Casa", "salary": "4000 DH", "urgent": False, "isReal": False, "sourceName": "MarocAnnonces", "link": "#", "catId": "cat_transport", "rating": "3.5"},
            {"id": "bk_2", "title": "Vendeuse Showroom", "company": "Zara", "location": "Marrakech", "salary": "4500 DH", "urgent": False, "isReal": False, "sourceName": "Rekrute", "link": "#", "catId": "cat_sales", "rating": "3.8"}
        ]
        
    return jobs

def generate_sitemap(jobs):
    """Creates the map for Google to find your jobs"""
    print("🗺️ Generating Sitemap for Google...")
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Add Homepage
    xml_content += f'  <url><loc>{BASE_URL}/</loc><changefreq>daily</changefreq></url>\n'
    
    # Add Each Job (Deep Links)
    for job in jobs:
        # Google needs a unique URL for each job. We use the ?job_id parameter.
        job_url = f"{BASE_URL}/?job_id={job['id']}"
        xml_content += f'  <url><loc>{job_url}</loc><changefreq>daily</changefreq></url>\n'
        
    xml_content += '</urlset>'
    
    with open(OUTPUT_SITEMAP, 'w', encoding='utf-8') as f:
        f.write(xml_content)

def main():
    print("🚀 Proleefic Robot Started...")
    all_jobs = []
    
    # 1. Get Jobs
    all_jobs.extend(get_neon_jobs())
    all_jobs.extend(scrape_dreamjob())
    
    # 2. Save JSON (For the website)
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=2)
        
    # 3. Generate Sitemap (For Google)
    generate_sitemap(all_jobs)
    
    print(f"✅ Done! Saved {len(all_jobs)} jobs and generated sitemap.")

if __name__ == "__main__":
    main()
