
import json, time, random, requests
from bs4 import BeautifulSoup

def generate_jobs():
    print("Generating Individual & Industrial Jobs...")
    
    # Real mix of factory and individual jobs
    roles = [
        ("Opérateur Câblage", "cat_prod", "Yazaki"), 
        ("Chauffeur Personnel", "cat_transport", "Particulier"),
        ("Technicien Maintenance", "cat_tech", "Renault"),
        ("Jardinier", "cat_prod", "Particulier"),
        ("Femme de Ménage", "cat_prod", "Particulier"),
        ("Ingénieur Qualité", "cat_eng", "Stellantis"),
        ("Electricien Bâtiment", "cat_tech", "Société BTP"),
        ("Magasinier", "cat_transport", "Marjane")
    ]
    cities = ["Tanger", "Casablanca", "Rabat", "Agadir", "Kenitra"]
    
    jobs = []
    for i in range(60):
        r = random.choice(roles)
        city = random.choice(cities)
        
        # If it is a big company, link to LinkedIn search
        # If it is "Particulier", link to MarocAnnonces search (where individuals post)
        if r[2] == "Particulier":
            link = f"https://www.marocannonces.com/maroc/offres-emploi-b309.html?kw={r[0].replace(' ','+')}"
            source = "MarocAnnonces"
        else:
            link = f"https://www.linkedin.com/jobs/search/?keywords={r[0].replace(' ','+')}+{r[2]}+Maroc"
            source = "LinkedIn"

        jobs.append({
            "id": int(time.time()) + i,
            "title": r[0],
            "company": r[2],
            "location": city,
            "catId": r[1],
            "salary": "À discuter",
            "posted": random.randint(0,2),
            "urgent": True,
            "easyApply": True,
            "rating": "4.5",
            "link": link,
            "sourceName": source
        })
        
    return jobs

if __name__ == "__main__":
    data = generate_jobs()
    with open('jobs.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ Saved jobs.json")
