from Services.JobScrapper import fetch_job_details, scrape_linkedin_jobs

jobs = []

def get_jobs(role, location):
    global jobs
    jobs = scrape_linkedin_jobs(keyword=role, location=location)
    return jobs

def get_job_details(url):
    job = next((j for j in jobs if j["link"] == url), None)
    if not job:
        return None
    return fetch_job_details(job["link"])