# Add this function to your scraper.py inside generate_backup_simulation
# It mixes standard link jobs with "Direct Contact" jobs

def generate_direct_hiring_jobs():
    """Generates high-value jobs with Email/Phone contacts"""
    direct_jobs = [
        {
            "id": "d_101",
            "title": "Assistant Administratif",
            "company": "Cabinet Notaire Fes",
            "location": "Fes",
            "salary": "4000 DH",
            "posted": "1d ago",
            "urgent": True,
            "isReal": True,
            "isDirect": True,  # <--- Critical flag
            "email": "contact@cabinet-fes.ma",
            "reqs": ["Bac+2 Gestion", "Maîtrise Word/Excel", "Serieux et ponctuel"],
            "sourceName": "Direct HR",
            "catId": "cat_admin",
            "rating": "4.5"
        },
        {
            "id": "d_102",
            "title": "Vendeuse Prêt-à-porter",
            "company": "Boutique Zara",
            "location": "Marrakech",
            "salary": "3500 DH + Com",
            "posted": "2d ago",
            "urgent": False,
            "isReal": True,
            "isDirect": True,
            "email": "recrutement@zara-maroc.com",
            "reqs": ["Bonne présentation", "Expérience vente", "Français correct"],
            "sourceName": "Direct HR",
            "catId": "cat_sales",
            "rating": "4.2"
        }
    ]
    return direct_jobs
