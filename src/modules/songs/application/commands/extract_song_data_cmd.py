from dataclasses import dataclass
import logging
import os
import uuid

from modules.common.application.interfaces.event_streaming_interface import EventStreamingInterface
from modules.songs.application.interfaces.analyze_song_api import AnalyzeSongApi
from modules.songs.application.interfaces.download_song_api import DownloadSongApi
from modules.songs.domain.song import SongData
from modules.songs.domain.song_repo import SongRepo


@dataclass
class ExtractSongDataCommand():
  id: uuid.UUID

@dataclass
class ExtractSongDataCommandHandler():
  download_api:DownloadSongApi
  song_repo:SongRepo
  stream:EventStreamingInterface
  analy_song_api:AnalyzeSongApi

  def handle(self, cmd: ExtractSongDataCommand):
    try:

      # check first if audio is downloaded
      song_downloaded_path = self.download_api.getFullDownloadPath(cmd.id)
      
      if not os.path.exists(song_downloaded_path):
        raise Exception(f"Path does not exist: {song_downloaded_path}")

      data = self.analy_song_api.analyze(song_downloaded_path)

      songData = SongData(
        id=cmd.id,
        data=data)

      self.song_repo.save_song_data(songData)

      body = {
        "id": str(cmd.id),
        "success": "true",
      }

      self.stream.add(stream="data-extracted-songs", data=body)


    except Exception as e:
      logging.error(f"error ExtractSongDataCommandHandler {e}")
      body = {
        "id": str(cmd.id),
        "success": "false",
      }
      self.stream.add(stream="data-extracted-songs", data=body)

