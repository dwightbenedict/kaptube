from dataclasses import dataclass

import kapwing


@dataclass
class YoutubeVideo:
    title: str
    link: str


def download(yt_url: str, max_attempts: int) -> YoutubeVideo | None:
    video_metadata = kapwing.extract_video_metadata(yt_url)

    for _ in range(max_attempts):
        asset_url = kapwing.get_asset_url(yt_url, video_metadata)

        if asset_url:
            return YoutubeVideo(
                title=video_metadata["title"],
                link=asset_url,
            )

    return None