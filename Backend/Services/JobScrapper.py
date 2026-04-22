import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Scrape LinkedIn for job postings based on role and location
def scrape_linkedin_jobs(keyword="Full Stack Developer", location="United States", pages=3):
    jobs_data = []

    for page in range(pages):
        start = page * 25

        params = {
            "keywords": keyword,
            "location": location,
            "start": start,
            "f_TPR": "r86400",      # last 24 hours
            # "f_WT": "2",            # remote
            "f_E": "2,3",           # entry + associate
            "sortBy": "DD"          # most recent
        }
        response = requests.get(BASE_URL, headers=HEADERS, params=params)

        if response.status_code != 200:
            print(f"Request failed: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("li")

        for job in job_cards:
            title_tag = job.find("h3")
            company_tag = job.find("h4")
            location_tag = job.find(class_="job-search-card__location")
            link_tag = job.find("a", href=True)
            logo = job.find("img", class_="artdeco-entity-image")


            job_info = {
                "title": title_tag.text.strip() if title_tag else None,
                "company": company_tag.text.strip() if company_tag else None,
                "location": location_tag.text.strip() if location_tag else None,
                "link": link_tag["href"] if link_tag else None,
                "logo": logo["src"] if logo else None
            }

            jobs_data.append(job_info)

        # polite delay to avoid getting blocked
        time.sleep(2)

    return jobs_data


# Helper function to fetch job details from job detail page
def fetch_job_details(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    desc = soup.find("div", class_="show-more-less-html__markup")
    return desc.text.strip() if desc else None  