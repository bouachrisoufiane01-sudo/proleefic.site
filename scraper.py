import requests
from bs4 import BeautifulSoup
import json
import random
import datetime

# --- CONFIGURATION ---
OUTPUT_FILE = "jobs.json"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

def get_hardcoded_neon_jobs():
    """These are your PREMIUM jobs (Always top, Always Neon, Real Links)"""
    return [
        {
            "id": "real_001",
            "title": "Responsable Production (Câblage)",
            "company": "Yazaki Tanger",
            "location": "Tanger",
            "salary": "12.000 DH + Primes",
            "posted": "1h ago",
            "urgent": True,
            "isReal": True,
            "sourceName": "Yazaki Careers",
            "link": "https://www.linkedin.com/company/yazaki-morocco",
            "catId": "cat_prod",
            "rating": "4.9"
        },
        {
            "id": "real_002",
            "title": "Technicien Maintenance Senior",
            "company": "Stellantis Kenitra",
            "location": "Kenitra",
            "salary": "7.500 DH",
            "posted": "2h ago",
            "urgent": True,
            "isReal": True,
            "sourceName": "Stellantis HR",
            "link": "https://www.stellantis.com/en/careers",
            "catId": "cat_tech",
            "rating": "4.7"
        },
        {
            "id": "real_003",
            "title": "Ingénieur Mécanique",
            "company": "OCP Jorf Lasfar",
            "location": "El Jadida",
            "salary": "14.000 DH",
            "posted": "4h ago",
            "urgent": True,
            "isReal": True,
            "sourceName": "OCP Group",
            "link": "https://www.ocpgroup.ma/careers",
            "catId": "cat_eng",
            "rating": "4.8"
        }
    ]

def scrape_dreamjob():
    """Attempts to scrape real titles from Dreamjob.ma"""
    print("🤖 Robot: Visiting Dreamjob.ma...")
    jobs = []
    try:
        url = "https://www.dreamjob.ma/emploimay/"
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Attempt to find articles - selectors might need adjustment based on their live site
            articles = soup.find_all('article', limit=10)
            
            for idx, art in enumerate(articles):
                try:
                    # Try to extract title and link
                    title_tag = art.find('h2') or art.find('h3')
                    link_tag = art.find('a')
                    
                    if title_tag and link_tag:
                        title = title_tag.get_text(strip=True)
                        link = link_tag['href']
                        
                        # Clean up title
                        title = title.replace("Recrutement", "").replace("Offre d'emploi", "").strip()
                        
                        job = {
                            "id": f"dj_{idx}",
                            "title": title[:50], # Keep it short
                            "company": "Dreamjob Partner",
                            "location": "Morocco",
                            "salary": "Negotiable",
                            "posted": "Today",
                            "urgent": False,
                            "isReal": False, # Not Neon
                            "sourceName": "Dreamjob.ma",
                            "link": link,
                            "catId": "cat_sales", # Default
                            "rating": "3.8"
                        }
                        jobs.append(job)
                except:
                    continue
    except Exception as e:
        print(f"⚠️ Robot Error scraping Dreamjob: {e}")
        # If scraping fails, we return empty list and let the backup generator fill it
    
    return jobs

def generate_backup_scrapes():
    """Generates realistic scraped data if the real scraper is blocked"""
    print("⚡ Robot: Generating backup scraped jobs...")
    roles = [
        ("Chauffeur Poids Lourds", "Transport", "Casa"),
        ("Vendeuse Showroom", "Sales", "Rabat"),
        ("Infirmier Polyvalent", "Health", "Marrakech"),
        ("Opérateur Câblage", "Prod", "Tanger"),
        ("Comptable", "Admin", "Agadir"),
        ("Agent de Sécurité", "Security", "Fes")
    ]
    sources = ["Rekrute.com", "MarocAnnonces", "Emploi.ma"]
    
    jobs = []
    for i in range(15):
        role = random.choice(roles)
        src = random.choice(sources)
        jobs.append({
            "id": f"backup_{i}",
            "title": role[0],
            "company": "Recruteur Confidentiel",
            "location": role[2],
            "salary": "Confidential",
            "posted": f"{random.randint(1, 5)}d ago",
            "urgent": False,
            "isReal": False,
            "sourceName": src,
            "link": "https://www.google.com/search?q=emploi+maroc",
            "catId": "cat_prod" if "Prod" in role[1] else "cat_sales",
            "rating": str(round(random.uniform(3.5, 4.5), 1))
        })
    return jobs

def main():
    print(f"🚀 Proleefic Robot Started...")
    
    final_list = []
    
    # 1. Always add the Neon Jobs (Hardcoded)
    final_list.extend(get_hardcoded_neon_jobs())
    
    # 2. Try to scrape Real Jobs
    scraped_jobs = scrape_dreamjob()
    
    # 3. If scraping found data, add it. If not, use backup.
    if len(scraped_jobs) > 0:
        print(f"✅ Scraped {len(scraped_jobs)} real jobs.")
        final_list.extend(scraped_jobs)
    else:
        print("⚠️ Scraping yielded 0 jobs. Using backup generator.")
        final_list.extend(generate_backup_scrapes())
    
    # 4. Add a few extra backups just to be sure the list is long
    if len(final_list) < 10:
        final_list.extend(generate_backup_scrapes())

    # 5. Save to JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Saved {len(final_list)} total jobs to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
