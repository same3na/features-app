from dataclasses import dataclass
import logging
import os
import uuid

from modules.common.application.interfaces.event_streaming_interface import EventStreamingInterface
from modules.common.application.interfaces.pub_sub_interface import PubSubInterface
from modules.songs.application.interfaces.analyze_song_api import AnalyzeSongApi
from modules.songs.application.interfaces.download_song_api import DownloadSongApi
from modules.songs.application.interfaces.external_song_url import ExternalSongUrl
from modules.songs.domain.song import Song
from modules.songs.domain.song_repo import SongRepo

@dataclass
class DownloadSongCommand():
  id: str
  title: str
  album: str
  artist: str

@dataclass
class DownloadSongCommandHandler():
  download_api:DownloadSongApi
  external_song_url:ExternalSongUrl
  stream:EventStreamingInterface


  def handle(self, cmd: DownloadSongCommand):
    try:
      # get song url
      url = self.external_song_url.get_url(title=cmd.title, artist=cmd.artist, album=cmd.album)

      # download the sample
      if not url:
        raise Exception(f"song url is not set: {url}")

      # download the song
      self.download_api.download_sample(cmd.id, url)

      song_downloaded_path = self.download_api.getFullDownloadPath(cmd.id)

      if not os.path.exists(song_downloaded_path):
        raise Exception(f"Path does not exist: {song_downloaded_path}")
            
      # notify that the song has been analyzed successfully
      # transform the body to bytes
      body = {
        "id": cmd.id,
        "url": url
      }
      logging.debug(f"Message sent to the stream {body}")
      self.stream.add(stream="song-external-url", data=body)
      self.stream.add(stream="get-song-features", data=body)

    except Exception as e:
      # notify that the song has been analyzed successfully
      # transform the body to bytes
      body = {
        "id": cmd.id,
        "success": "false",
        "url": ""
      }
      logging.debug(f"Message sent to the stream {body}")
      self.stream.add(stream="analyzed-songs", data=body)
