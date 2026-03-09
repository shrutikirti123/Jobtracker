import json
from core.redis_client import redis_client
import requests


def search_jobs(keyword):

    cache_key = f"jobs:{keyword}"

    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    url = f"https://remotive.com/api/remote-jobs?search={keyword}"

    response = requests.get(url)
    data = response.json()["jobs"]

    results = []

    for job in data[:20]:

        results.append({
            "title": job["title"],
            "company": job["company_name"],
            "description": job["description"],
            "url": job["url"]
        })

    redis_client.setex(cache_key, 3600, json.dumps(results))

    return results