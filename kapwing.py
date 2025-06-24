import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Content-Type": "application/json",
    "Referer": "https://www.kapwing.com/",
    "X-Client-Version": "v2025.04.24.6",
    "Origin": "https://www.kapwing.com"
}
AUTH_HEADERS = {
    "X-Access-Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NDQzZTk5YTE4NDE5YzAwMjU0ZDk4ZmQiLCJhY2NvdW50VHlwZSI6MCwibmFtZSI6IkR3aWdodCBBUEkiLCJlbWFpbCI6ImFwaWR3aWdodEBnbWFpbC5jb20iLCJyb2xlIjoiZGVmYXVsdCIsImlhdCI6MTc0NTY0Mjk4MywiZXhwIjoxNzc3MTc4OTgzfQ.9XNWP97slXVD7LpqhNG_qC1AKQgQfbTq5KQitbOF8y4"
}


def extract_video_metadata(video_url: str) -> dict:
    url = "https://us-east1-kapwing-prod.cloudfunctions.net/extract"
    payload = {
        "url": video_url,
        "doDuplicateHandling": False
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()


def get_final_google_video_url(initial_url: str) -> str:
    response = requests.get(initial_url, headers=HEADERS)
    response.raise_for_status()
    return response.url


def get_asset_url(video_url: str, video_metadata: dict) -> str | None:
    url = "https://www.kapwing.com/api/trpc/asset.createFromLink"
    payload = {
        "extract_info": video_metadata,
        "url": video_metadata.get("originalUrl", video_url),
        "forceNewAssets": False
    }
    response = requests.post(url, headers=HEADERS | AUTH_HEADERS, json=payload)
    response.raise_for_status()
    data = response.json()
    ffmpeg_status = data["result"]["data"]["asset"]["status"]

    if ffmpeg_status not in {1, 2}:
        return None

    asset_link = data["result"]["data"]["asset"]["url"]

    if "googlevideo.com" in asset_link:
        try:
            asset_link = get_final_google_video_url(asset_link)
        except requests.HTTPError:
            return None

    return asset_link