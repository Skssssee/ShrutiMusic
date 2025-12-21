import asyncio
import os
import re
from typing import Union
import yt_dlp
from py_yt import VideosSearch
from ShrutiMusic.utils.formatters import time_to_seconds
import aiohttp
# from ShrutiMusic import LOGGER # Commented out to avoid import error if not present

# --- CONFIGURATION ---
MY_API_URL = "https://civic-robby-uhhy5-a19ca05d.koyeb.app" 
# ---------------------

async def download_song(link: str) -> str:
    video_id = link.split('v=')[-1].split('&')[0] if 'v=' in link else link

    if not video_id or len(video_id) < 3:
        return None

    DOWNLOAD_DIR = "downloads"
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp3")

    if os.path.exists(file_path):
        return file_path

    # Use our specific API URL
    api_url = MY_API_URL
    
    try:
        async with aiohttp.ClientSession() as session:
            # Our API uses /audio for direct streaming/downloading of audio
            # params: url={link}
            stream_url = f"{api_url}/audio?url=https://www.youtube.com/watch?v={video_id}"
            
            async with session.get(stream_url) as response:
                if response.status == 200:
                    with open(file_path, "wb") as f:
                        async for chunk in response.content.iter_chunked(16384):
                            f.write(chunk)
                    
                    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                        return file_path
    except Exception as e:
        print(f"Error downloading: {e}")
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
    
    return None

async def download_video(link: str) -> str:
    video_id = link.split('v=')[-1].split('&')[0] if 'v=' in link else link

    if not video_id or len(video_id) < 3:
        return None

    DOWNLOAD_DIR = "downloads"
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")

    if os.path.exists(file_path):
        return file_path

    api_url = MY_API_URL
    
    try:
        async with aiohttp.ClientSession() as session:
            # Our API uses /download for video
            # params: url={link}
            stream_url = f"{api_url}/download?url=https://www.youtube.com/watch?v={video_id}"
            
            async with session.get(stream_url) as response:
                if response.status == 200:
                    with open(file_path, "wb") as f:
                        async for chunk in response.content.iter_chunked(16384):
                            f.write(chunk)
                    
                    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                        return file_path
    except Exception as e:
        print(f"Error downloading video: {e}")
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
    
    return None

# ... (Original YouTubeAPI class logic can remain mostly same, 
#      but the 'download' method just calls our new functions)

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"

    async def download(
        self,
        link: str,
        mystic=None,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        if videoid:
            link = self.base + link

        try:
            if video:
                downloaded_file = await download_video(link)
            else:
                downloaded_file = await download_song(link)
            
            if downloaded_file:
                return downloaded_file, True
            else:
                return None, False
        except Exception:
            return None, False

# Test run if executed manually
if __name__ == "__main__":
    async def main():
        print("Testing download...")
        path = await download_song("dQw4w9WgXcQ")
        print(f"Downloaded to: {path}")

    # asyncio.run(main())

