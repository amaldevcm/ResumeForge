import uuid
import re
import requests
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

# HEADERS = {
#     "User-Agent": "Mozilla/5.0"
# }

JSEARCH_URL = "https://jsearch.p.rapidapi.com/search"
HEADERS = {
    "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

allJobs = []

# 
def get_jobs(role, location):
    global allJobs
    allJobs = get_jobs_jsearch(keyword=role, location=location)
    return allJobs

# Get job details by URL
def get_job_details(url):
    job = next((j for j in allJobs if j["link"] == url), None)
    if not job:
        return None
    return fetch_job_details(job["link"])

# Fetch jobs using JSearch API
def get_jobs_jsearch(keyword, location, page=1):
    params = {
        "query": f"{keyword} in {location}",
        "page": str(page),
        "num_results": "10"
    }
    
    response = requests.get(JSEARCH_URL, headers=HEADERS, params=params)
    
    if response.status_code != 200:
        return []
    
    jobs = response.json().get("data", [])
    
    return [{
        "id": str(uuid.uuid4()),
        "title": job["job_title"],
        "company": job["employer_name"],
        "location": job["job_city"],
        "description": parse_job_description(job["job_description"]),
        "link": job["job_apply_link"],
        "logo": job["employer_logo"]
    } for job in jobs]


# Parse job description to extract key details (skills, experience, etc.)
SECTION_HEADERS = {
    "responsibilities": [
        "responsibilities", "what you'll do", "your role", "duties", "what you will do"
    ],
    "requirements": [
        "requirements", "qualifications", "what you'll need", "skills", "who you are", "what we're looking for"
    ],
    "company": [
        "about us", "company", "who we are", "our story", "why us", "Working at "
    ],
    "benefits": [
        "benefits", "perks", "what we offer", "compensation", "why join us"
    ]
}

def parse_job_description(description):
    result = {"summary": [], "responsibilities": [], "requirements": [], "benefits": []}
    current_section = "summary"
    
    for line in description.split("\n"):
        line = line.strip()
        if not line:
            continue
        
        # check if line is a section header
        lower_line = line.lower().strip(":#*")
        matched_section = None
        for section, keywords in SECTION_HEADERS.items():
            if any(keyword in lower_line for keyword in keywords):
                matched_section = section
                break
        
        if matched_section:
            current_section = matched_section
            continue
        
        # add line to current section
        if current_section:
            cleaned = re.sub(r'^[-•*]\s*', '', line)  # remove bullet points
            if cleaned:
                result[current_section].append(cleaned)

        
    result["summary"] = " ".join(result["summary"])
    
    return result



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
                "logo": (
                            logo.get("data-delayed-url") or
                            logo.get("src")
                        ) if logo else None
            }

            jobs_data.append(job_info)

        # polite delay to avoid getting blocked
        time.sleep(2)

    return jobs_data


# Helper function to fetch job details from job detail page
def fetch_job_details(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    # get all job details from the url
    title = soup.find("h1", class_="jobs-details__title")
    company = soup.find("a", class_="jobs-details-top-card__company-url")
    location = soup.find("span", class_="jobs-details-top-card__bullet")
    salary = soup.find("span", class_="jobs-details-top-card__salary")
    desc = soup.find("div", class_="show-more-less-html__markup")
    logo = soup.find("img", class_="artdeco-entity-image")

    return {
        "title": title.text.strip() if title else None,
        "company": company.text.strip() if company else None,
        "location": location.text.strip() if location else None,
        "salary": salary.text.strip() if salary else None,
        "description": desc.text.strip() if desc else None,
        "logo": (
                    logo.get("data-delayed-url") or
                    logo.get("src")
                ) if logo else None
    }