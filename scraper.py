import requests
from bs4 import BeautifulSoup
import json
import os
import time

# --- 🔧 SETTINGS (Inspect the website to verify these) ---
# Target URL (Rekrute search page)
URL = "https://www.rekrute.com/offres-emploi-maroc.html"

# CSS Selectors (Right-click a job on the site -> Inspect to verify)
# 1. The Box: The HTML tag that holds ONE entire job offer
JOB_CARD_CLASS = "post-item" 

# 2. The Title: The tag inside the box that has the job title
TITLE_TAG = "h2"

# 3. The Company: The class inside the box with the company name/logo
COMPANY_CLASS = "photo"
# ---------------------------------------------------------

def scrape_jobs():
    print(f"🚀 Starting scraper for: {URL}")
    
    # Fake a browser visit to avoid being blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status() # Check for errors (404, 500)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all job boxes
        job_cards = soup.find_all('div', class_=JOB_CARD_CLASS)
        
        # SAFETY CHECK
        if not job_cards:
            print(f"⚠️ WARNING: No jobs found! The class name '{JOB_CARD_CLASS}' might be wrong.")
            print("Did the website change? Check the HTML.")
            return []

        print(f"✅ Found {len(job_cards)} job cards. extracting data...")
        
        jobs_data = []
        
        # Loop through the first 20 jobs
        for card in job_cards[:20]:
            try:
                # 1. Get Title
                title_el = card.find(TITLE_TAG)
                title = title_el.text.strip() if title_el else "Offre Spéciale"

                # 2. Get Company
                # (Rekrute often puts company name in an <img> alt tag inside the 'photo' div)
                company_div = card.find(class_=COMPANY_CLASS)
                company = "Confidential"
                if company_div:
                    img = company_div.find('img')
                    if img and img.get('alt'):
                        company = img.get('alt') # Use the image text
                    else:
                        company = company_div.text.strip() # Use the text

                # 3. Get Link
                link_el = card.find('a', class_='titreJob') # Specific class often used for the link
                # Fallback if specific class not found
                if not link_el:
                    link_el = card.find('a')
                
                full_link = "https://www.rekrute.com" + link_el['href'] if link_el else "#"

                # Add to list
                jobs_data.append({
                    "title": title,
                    "company": company,
                    "link": full_link,
                    "date": time.strftime("%Y-%m-%d")
                })

            except Exception as e:
                print(f"Skipped a job due to error: {e}")
                continue

        return jobs_data

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        return []

if __name__ == "__main__":
    jobs = scrape_jobs()
    
    # Save to 'jobs.json'
    if jobs:
        with open('jobs.json', 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
        print(f"🎉 Success! Saved {len(jobs)} jobs to jobs.json")
    else:
        print("❌ Failed. No jobs saved.")
