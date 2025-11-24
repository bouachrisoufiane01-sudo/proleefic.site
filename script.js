document.addEventListener('DOMContentLoaded', () => {
    const jobContainer = document.getElementById('job-container');

    // 👇 REPLACE THIS with your actual GitHub Raw URL
    const API_URL = 'https://raw.githubusercontent.com/YOUR_GITHUB_USER/YOUR_REPO_NAME/main/jobs.json';
    
    // 👇 REPLACE THIS with the email where you want to receive CVs
    const MY_EMAIL = "contact@proleefic.com"; 

    async function fetchJobs() {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) throw new Error("Could not fetch jobs");

            const jobs = await response.json();
            
            jobContainer.innerHTML = '';

            jobs.forEach(job => {
                // 1. Create the "Direct Apply" Mailto Link
                // Result: mailto:contact@proleefic.com?subject=Candidature: Job Title
                const emailSubject = encodeURIComponent(`Candidature: ${job.title}`);
                const directLink = `mailto:${MY_EMAIL}?subject=${emailSubject}`;

                // 2. Create the Card HTML
                const card = document.createElement('div');
                card.className = 'job-card'; // Make sure this matches your CSS class
                
                card.innerHTML = `
                    <h3>${job.title}</h3>
                    <div class="company">🏢 ${job.company}</div>
                    <div class="date">📅 ${job.date || 'Récent'}</div>
                    
                    <div class="button-group">
                        <a href="${directLink}" class="btn btn-direct">
                            ⚡ Postuler Direct
                        </a>

                        <a href="${job.link}" target="_blank" class="btn btn-source">
                            🔗 Voir Source
                        </a>
                    </div>
                `;
                jobContainer.appendChild(card);
            });

        } catch (error) {
            console.error(error);
            jobContainer.innerHTML = '<p style="text-align:center">Chargement des offres en cours...</p>';
        }
    }

    fetchJobs();
});
