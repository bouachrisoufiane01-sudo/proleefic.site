import json
import random
import time

def generate_jobs():
    print("🚀 Generating Jobs with External Sources...")
    
    titles = [
        ("Technicien Spécialisé", "cat_tech"), ("Opérateur de Production", "cat_prod"), 
        ("Ingénieur Génie Civil", "cat_eng"), ("Développeur Full Stack", "cat_it"),
        ("Commercial Terrain", "cat_sales"), ("Comptable Senior", "cat_admin"),
        ("Chauffeur Livreur", "cat_transport"), ("Infirmier Polyvalent", "cat_tech"),
        ("Chargé de Clientèle", "cat_sales"), ("Electricien Bâtiment", "cat_tech")
    ]
    companies = ["Renault Tanger", "OCP Group", "Yazaki", "Maroc Telecom", "Dell", "Centrale Danone", "BIM Maroc", "Marjane", "Attijariwafa Bank"]
    cities = ["Casablanca", "Tanger", "Rabat", "Kenitra", "Marrakech", "Agadir", "Fes", "Meknes", "El Jadida"]
    
    # REAL SOURCES LIST
    sources = [
        {"name": "LinkedIn", "base_url": "https://www.linkedin.com/jobs/search/?keywords={}+Maroc"},
        {"name": "Rekrute", "base_url": "https://www.rekrute.com/offres-emploi-maroc.html?keyword={}"},
        {"name": "Emploi.ma", "base_url": "https://www.emploi.ma/recherche-jobs-maroc?keywords={}"},
        {"name": "Anapec", "base_url": "http://www.anapec.org/sigec-app-rv/chercheurs/resultat_recherche?mot_cle={}"},
        {"name": "MarocAnnonces", "base_url": "https://www.marocannonces.com/maroc/offres-emploi-domaine-informatique-multimedia-internet-b309.html"}
    ]
    
    jobs = []
    
    for i in range(50):
        t = random.choice(titles)
        comp = random.choice(companies)
        src = random.choice(sources)
        
        # Create Search Link (This is safer than direct links because they never expire)
        # It sends the user to a search page on the external site for that job title
        search_query = t[0].replace(" ", "+")
        final_link = src["base_url"].format(search_query)

        job = {
            "id": int(time.time()) + i,
            "title": t[0],
            "company": comp,
            "location": random.choice(cities),
            "catId": t[1],
            "salary": f"{random.randint(4, 15)}000 MAD",
            "posted": random.randint(0, 3),
            "urgent": random.random() > 0.8,
            "easyApply": random.random() > 0.6,
            "rating": str(round(random.uniform(3.8, 5.0), 1)),
            "link": final_link,        # <--- THE EXTERNAL LINK
            "sourceName": src["name"]  # <--- THE SOURCE NAME (e.g. "LinkedIn")
        }
        jobs.append(job)

    print(f"✅ Generated {len(jobs)} jobs pointing to external sources.")
    return jobs

if __name__ == "__main__":
    try:
        data = generate_jobs()
        with open('jobs.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("💾 jobs.json saved.")
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)
