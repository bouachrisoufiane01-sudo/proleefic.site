import requests
from bs4 import BeautifulSoup
import json
import time

# Configuration
SOURCES = {
    'rekrute': 'https://www.rekrute.com/offres.html',
    'dreamjob': 'https://www.dreamjob.ma/emploi/',
}

def scrape_rekrute():
    """Scrape jobs from Rekrute"""
    jobs = []
    try:
        response = requests.get(SOURCES['rekrute'])
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find job listings (adjust selectors based on actual site)
        job_cards = soup.find_all('div', class_='job-item')
        
        for card in job_cards:
            job = {
                'id': f"rek_{len(jobs)}",
                'title': card.find('h3').text.strip(),
                'company': card.find('span', class_='company').text.strip(),
                'location': card.find('span', class_='location').text.strip(),
                'link': card.find('a')['href'],
                'catId': 'cat_prod',  # Categorize based on keywords
                'salary': 'Négociable',
                'urgent': False,
                'isReal': False,
                'isDirect': False,
                'sourceName': 'Rekrute'
            }
            jobs.append(job)
            
    except Exception as e:
        print(f"Error scraping Rekrute: {e}")
    
    return jobs

def scrape_dreamjob():
    """Scrape jobs from DreamJob"""
    jobs = []
    try:
        response = requests.get(SOURCES['dreamjob'])
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Adjust selectors based on actual site structure
        job_cards = soup.find_all('article', class_='job-post')
        
        for card in job_cards:
            job = {
                'id': f"dream_{len(jobs)}",
                'title': card.find('h2').text.strip(),
                'company': card.find('div', class_='company-name').text.strip(),
                'location': card.find('span', class_='job-location').text.strip(),
                'link': card.find('a')['href'],
                'catId': 'cat_admin',
                'salary': 'Négociable',
                'urgent': False,
                'isReal': False,
                'isDirect': False,
                'sourceName': 'DreamJob'
            }
            jobs.append(job)
            
    except Exception as e:
        print(f"Error scraping DreamJob: {e}")
    
    return jobs

def main():
    """Main scraper function"""
    print("🤖 Starting job scraper...")
    
    all_jobs = []
    
    # Scrape each source
    print("📊 Scraping Rekrute...")
    all_jobs.extend(scrape_rekrute())
    time.sleep(2)  # Be polite, wait between requests
    
    print("📊 Scraping DreamJob...")
    all_jobs.extend(scrape_dreamjob())
    
    # Save to jobs.json
    with open('jobs.json', 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Scraped {len(all_jobs)} jobs successfully!")

if __name__ == "__main__":
    main()
