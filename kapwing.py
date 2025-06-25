import requests


def extract_video_metadata(video_url: str) -> dict:
    url = "https://us-east1-kapwing-prod.cloudfunctions.net/extract"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0",
        "Content-Type": "application/json",
        "X-Client-Version": "v2025.04.24.6",
        "Referer": "https://www.kapwing.com/",
        "Origin": "https://www.kapwing.com"
    }
    payload = {
        "url": video_url,
        "doDuplicateHandling": False
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def get_content_bytes(initial_url: str) -> bytes:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0",
        "Referer": "https://www.kapwing.com/",
        "Origin": "https://www.kapwing.com"
    }
    response = requests.get(initial_url, headers=headers)
    response.raise_for_status()
    return response.content


def get_video_content(video_url: str, video_metadata: dict) -> bytes | None:
    url = "https://www.kapwing.com/api/trpc/asset.createFromLink"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0",
        "Content-Type": "application/json",
        "Referer": "https://www.kapwing.com/",
        "X-Client-Version": "v2025.04.24.6",
        "X-Access-Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NDQzZTk5YTE4NDE5YzAwMjU0ZDk4ZmQiLCJhY2NvdW50VHlwZSI6MCwibmFtZSI6IkR3aWdodCBBUEkiLCJlbWFpbCI6ImFwaWR3aWdodEBnbWFpbC5jb20iLCJyb2xlIjoiZGVmYXVsdCIsImlhdCI6MTc0NTY0Mjk4MywiZXhwIjoxNzc3MTc4OTgzfQ.9XNWP97slXVD7LpqhNG_qC1AKQgQfbTq5KQitbOF8y4",
        "Origin": "https://www.kapwing.com"
    }
    payload = {
        "extract_info": video_metadata,
        "url": video_metadata.get("originalUrl", video_url),
        "forceNewAssets": False
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    ffmpeg_status = data["result"]["data"]["asset"]["status"]

    if ffmpeg_status not in {1, 2}:
        return None

    video_url = data["result"]["data"]["asset"]["url"]
    return get_content_bytes(video_url)