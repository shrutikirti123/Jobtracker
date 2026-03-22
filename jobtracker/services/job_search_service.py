import json
import requests
from core.redis_client import redis_client


def search_jobs(keyword):

    cache_key = f"jobs:{keyword}"

    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    url = f"https://remotive.com/api/remote-jobs?search={keyword}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json().get("jobs", [])
    except:
        return []

    results = []

    for job in data[:20]:

        results.append({
            "title": job.get("title"),
            "company": job.get("company_name"),
            "description": job.get("description"),
            "url": job.get("url")
        })

    redis_client.setex(cache_key, 3600, json.dumps(results))

    return results