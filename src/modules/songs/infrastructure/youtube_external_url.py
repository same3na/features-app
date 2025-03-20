
from dataclasses import dataclass
import logging
import re
import yt_dlp

from modules.songs.application.interfaces.external_song_url import ExternalSongUrl


@dataclass()
class YoutubeExternalUrl(ExternalSongUrl):

  def get_url(self, title:str, artist: str, album: str) -> str:
    search_query = f"ytsearch:{artist} {album} {title}"  # Search on YouTube
    print(search_query)
    ydl_opts = {
      "quiet": True,  # Suppress unnecessary output
      "extract_flat": True,  # Extract metadata without downloading
      "default_search": "ytsearch",  # Search on YouTube
      "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(search_query, download=False)  # Search and extract
      if "entries" in info and len(info["entries"]) > 0:
        url = info["entries"][0]["url"]  # Return the first result URL
        return url
      return None  # Return None if no results        
    