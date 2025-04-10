
import os
import json
import argparse

from modules.common.infrastructure.redis_streaming import RedisStreaming
from modules.songs.application.commands.download_song_cmd import DownloadSongCommand, DownloadSongCommandHandler
from modules.songs.infrastructure.youtube_external_url import YoutubeExternalUrl
from modules.songs.infrastructure.youtube_song_downloader import YoutubeSongDownloader
from logging_config import setup_logging


youtube_downloader = YoutubeSongDownloader()
event_stream = RedisStreaming(redis_host=os.getenv('REDIS_HOST'), redis_port=os.getenv('REDIS_PORT'), redis_db=os.getenv('REDIS_DB'))
external_url = YoutubeExternalUrl()

stream_name = "song-added"
consumer_group_name = "song-added-grp"
consumer = "song-added-grp-consumer-filtering-app"

donwload_song_cmd = DownloadSongCommandHandler(download_api=youtube_downloader, stream=event_stream, external_song_url=external_url)

def main(processor):
  setup_logging()

  try:
    while True:
      msgs = event_stream.consume(stream_name, consumer_group_name, f"{consumer}-{processor}")
      print(msgs)
      for id, message in msgs:
        data = json.loads(message["data"])
        try:
          donwload_song_cmd.handle(DownloadSongCommand(id=data["song_id"], title=data["song_name"], artist=data["artist_name"], album=data["album_name"]))
          event_stream.ack(stream_name, consumer_group_name, id)
        except Exception as e:
          print(f"Error processing message {id}: {e}")
  except KeyboardInterrupt:
    print("Subscriber stopped.")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Process some inputs.")
  parser.add_argument("--process", type=int, help="process", required=True)
  
  args = parser.parse_args()

  main(args.process)
