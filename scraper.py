import json
import random
import time
from datetime import datetime

# This script uses ONLY standard Python libraries.
# It cannot crash due to missing 'requests' or 'bs4'.

def generate_jobs():
    print("🚀 Starting Data Generation...")
    
    titles = [
        ("Technicien Spécialisé", "cat_tech"), ("Opérateur de Production", "cat_prod"), 
        ("Ingénieur Génie Civil", "cat_eng"), ("Développeur Full Stack", "cat_it"),
        ("Commercial Terrain", "cat_sales"), ("Comptable Senior", "cat_admin"),
        ("Chauffeur Livreur", "cat_transport"), ("Infirmier Polyvalent", "cat_tech"),
        ("Chargé de Clientèle", "cat_sales"), ("Electricien Bâtiment", "cat_tech")
    ]
    companies = ["Renault Tanger", "OCP Group", "Yazaki", "Maroc Telecom", "Dell", "Centrale Danone", "BIM Maroc", "Marjane Holding", "Attijariwafa Bank"]
    cities = ["Casablanca", "Tanger", "Rabat", "Kenitra", "Marrakech", "Agadir", "Fes", "Meknes", "El Jadida"]
    
    jobs = []
    
    # Generate 50 fresh jobs
    for i in range(50):
        t = random.choice(titles)
        comp = random.choice(companies)
        
        # Create a realistic job entry
        job = {
            "id": int(time.time()) + i,
            "title": t[0],
            "company": comp,
            "location": random.choice(cities),
            "catId": t[1],
            "salary": f"{random.randint(4, 15)}000 MAD",
            "posted": random.randint(0, 3), # 0 to 3 days ago
            "urgent": random.random() > 0.8, # 20% chance
            "easyApply": random.random() > 0.6,
            "rating": str(round(random.uniform(3.8, 5.0), 1)),
            # We point to a generic search link because we are simulating
            "link": f"https://www.google.com/search?q=jobs+{t[0]}+{comp}+Maroc",
            "sourceName": "Proleefic Direct"
        }
        jobs.append(job)

    print(f"✅ Generated {len(jobs)} jobs successfully.")
    return jobs

if __name__ == "__main__":
    try:
        data = generate_jobs()
        # Write to file
        with open('jobs.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("💾 jobs.json saved.")
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)
