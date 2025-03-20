
import argparse

from modules.songs.application.commands.download_song_by_url_cmd import DownloadSongByUrlCommand, DownloadSongByUrlCommandHandler
from modules.songs.infrastructure.youtube_song_downloader import YoutubeSongDownloader


def main(url:str, name:str):
  download_api = YoutubeSongDownloader()
  cmd = DownloadSongByUrlCommandHandler(download_api=download_api)
  cmd.handle(DownloadSongByUrlCommand(id=name, url=url))

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Process some inputs.")
  parser.add_argument("--name", type=str, help="name", required=True)
  parser.add_argument("--url", type=str, help="url", required=True)

  args = parser.parse_args()
  main(args.url, args.name)
