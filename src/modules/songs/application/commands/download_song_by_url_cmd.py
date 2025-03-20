from dataclasses import dataclass

from modules.songs.application.interfaces.download_song_api import DownloadSongApi


@dataclass
class DownloadSongByUrlCommand():
  id: str
  url: str

@dataclass
class DownloadSongByUrlCommandHandler():
  download_api:DownloadSongApi

  def handle(self, cmd:DownloadSongByUrlCommand):
    self.download_api.download_sample(cmd.id, cmd.url)
