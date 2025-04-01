
from dataclasses import dataclass
import yt_dlp

from modules.songs.application.interfaces.download_song_api import DownloadSongApi
from modules.songs.domain.song import Song


@dataclass()
class YoutubeSongDownloader(DownloadSongApi):

  def download_sample(self, id: str, url: str):
    ydl_opts = {
      'format': 'bestaudio/best',
      'postprocessors': [{
        'cookiefile': 'src/cookies.txt', 
        'key': 'FFmpegExtractAudio',
        'preferredcodec': self.getAudioCodec(),
      }],
      # 'outtmpl': self.getDownloadPath(song, '%(ext)s'),
      'outtmpl': f'{ self.getDownloadPath() }/{id}.%(ext)s',
      'postprocessor_args': [
        '-ac', '2',
        # '-t', str(self.getSampleDuration()),
      ],
      'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

        