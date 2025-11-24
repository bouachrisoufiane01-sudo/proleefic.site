document.addEventListener('DOMContentLoaded', () => {
    const jobContainer = document.getElementById('job-container'); // Make sure your HTML has this ID

    // 1. The URL to your RAW JSON file
    // REPLACE 'YOUR_GITHUB_USER' and 'YOUR_REPO_NAME' below!
    const API_URL = 'https://raw.githubusercontent.com/YOUR_GITHUB_USER/YOUR_REPO_NAME/main/jobs.json';

    async function fetchJobs() {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) throw new Error("Could not fetch jobs");

            const jobs = await response.json();
            
            // Clear "Loading..." text
            jobContainer.innerHTML = '';

            // Generate Cards
            jobs.forEach(job => {
                const card = `
                    <div class="job-card">
                        <h3>${job.title}</h3>
                        <div class="company">${job.company}</div>
                        <a href="${job.link}" target="_blank" class="apply-btn">Apply Now</a>
                    </div>
                `;
                jobContainer.innerHTML += card;
            });

        } catch (error) {
            console.error(error);
            jobContainer.innerHTML = '<p>Currently updating offers. Please check back later.</p>';
        }
    }

    fetchJobs();
});
