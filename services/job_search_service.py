import requests
import redis
import os

REMOTIVE_API = "https://remotive.com/api/remote-jobs"


def search_jobs(keyword: str):

    response = requests.get(REMOTIVE_API)

    data = response.json()

    jobs = []

    for job in data["jobs"]:

        if keyword.lower() in job["title"].lower():

            jobs.append({
                "title": job["title"],
                "company": job["company_name"],
                "description": job["description"],
                "url": job["url"]
            })

    return jobs[:10]



REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)