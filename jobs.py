import requests

def fetch_jobs(search: str, limit: int = 10) -> list[dict]:
    r = requests.get(
        "https://remotive.com/api/remote-jobs",
        params={"search": search, "limit": limit},
        timeout=15
    )
    r.raise_for_status()
    return r.json()["jobs"]

if __name__ == "__main__":
    for job in fetch_jobs("python", 5):
        print(job["title"], "|",job["company_name"])