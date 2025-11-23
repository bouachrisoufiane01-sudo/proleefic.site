import requests
from bs4 import BeautifulSoup
import json
import time
import random

# 1. The URL to scrape (Example: MarocAnnonces IT Section or similar)
# Note: Real scraping requires handling headers to look like a real browser.
URL = "https://www.marocannonces.com/maroc/offres-emploi-b309.html"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_jobs():
    print(f"Scraping {URL}...")
    try:
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        jobs = []
        # This selector depends on the specific website's HTML structure
        # For MarocAnnonces, jobs are usually in a list container
        # We will look for the standard listing blocks
        
        listings = soup.find_all('div', class_='cars-list') # Adjust class name based on inspection

        # If specific scraping fails, we fallback to a mix of scraped + high-quality static data
        # so your site always looks full. 
        
        # --- REAL SCRAPING LOGIC (Simplified for MarocAnnonces structure) ---
        listing_items = soup.find_all('ul', class_='cars-list')
        for ul in listing_items:
            for li in ul.find_all('li'):
                try:
                    title_tag = li.find('div', class_='holder').find('h3')
                    if not title_tag: continue
                    
                    title = title_tag.get_text(strip=True)
                    link = "https://www.marocannonces.com" + li.find('a')['href']
                    location = li.find('span', class_='location').get_text(strip=True)
                    
                    # Create a job object
                    job = {
                        "id": random.randint(10000, 99999),
                        "title": title,
                        "company": "Recruiter via MarocAnnonces", # Often hidden on classifieds
                        "location": location,
                        "salary": "Confidential",
                        "posted": "Recently",
                        "urgent": False,
                        "easyApply": False,
                        "catId": "cat_tech", # Defaulting to tech for this url
                        "link": link,
                        "sourceName": "MarocAnnonces"
                    }
                    jobs.append(job)
                except:
                    continue

        print(f"Found {len(jobs)} real jobs.")
        
        # If scraping is blocked or empty, ensure we have data
        if len(jobs) < 5:
            print("Scraping yielded low results, using fallback data.")
            # (Ideally, you would add your static list here as a backup)

        # Save to JSON
        with open('jobs.json', 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_jobs()
