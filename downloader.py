from dataclasses import dataclass

import kapwing


@dataclass
class YoutubeVideo:
    title: str
    content: bytes


def download(yt_url: str, max_attempts: int) -> YoutubeVideo | None:
    video_metadata = kapwing.extract_video_metadata(yt_url)

    for _ in range(max_attempts):
        video_content = kapwing.get_video_content(yt_url, video_metadata)

        if video_content:
            return YoutubeVideo(
                title=video_metadata["title"],
                content=video_content,
            )

    return None