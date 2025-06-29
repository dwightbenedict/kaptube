from dataclasses import dataclass
import re

import requests

import kapwing


@dataclass
class YoutubeVideo:
    title: str
    url: str
    content: bytes | None = None

    @property
    def filename(self) -> str:
        sanitized_title = re.sub(r'[\\/:"*?<>|]+', "", self.title)
        return f"{sanitized_title}.mp4"


def download(yt_url: str, max_attempts: int) -> YoutubeVideo | None:
    video_metadata = kapwing.extract_video_metadata(yt_url)

    for _ in range(max_attempts):
        download_url = kapwing.get_download_url(yt_url, video_metadata)

        try:
            video_content = kapwing.get_video_content(download_url)
            return YoutubeVideo(
                title=video_metadata["title"],
                url=download_url,
                content=video_content
            )
        except requests.HTTPError:
            return YoutubeVideo(
                title=video_metadata["title"],
                url=download_url,
            )

    return None