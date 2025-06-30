import requests
import os
from dotenv import load_dotenv


load_dotenv()

KAPWING_VERSION = os.environ.get("KAPWING_VERSION")
KAPWING_ACCESS_TOKEN = os.environ.get("KAPWING_ACCESS_TOKEN")


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


def get_download_url(video_url: str, video_metadata: dict) -> str | None:
    url = "https://www.kapwing.com/api/trpc/asset.createFromLink"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0",
        "Content-Type": "application/json",
        "Referer": "https://www.kapwing.com/",
        "X-Client-Version": KAPWING_VERSION,
        "X-Access-Token": KAPWING_ACCESS_TOKEN,
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

    return data["result"]["data"]["asset"]["url"]


def get_video_content(download_url: str) -> bytes:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0",
        "Referer": "https://www.kapwing.com/",
        "Origin": "https://www.kapwing.com"
    }
    response = requests.get(download_url, headers=headers)
    response.raise_for_status()
    return response.content