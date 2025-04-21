import argparse
import logging
import os
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from logging_config import setup_logging
from modules.common.infrastructure.redis_streaming import RedisStreaming
from modules.songs.application.commands.extract_song_data_cmd import ExtractSongDataCommand, ExtractSongDataCommandHandler
from modules.songs.infrastructure.essentia_analyzer import EssentiaAnalyzer
from modules.songs.infrastructure.sqlalchemy.song_repo import SQLAlchemySongRepository
from modules.songs.infrastructure.youtube_song_downloader import YoutubeSongDownloader


DATABASE_URL = f"postgresql://{os.getenv('DBUSER')}:{os.getenv('DBPASS')}@{os.getenv('DBHOST')}:{os.getenv('DBPORT')}/{os.getenv('DBNAME')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

song_repo = SQLAlchemySongRepository(session=session)
essentia_analyzer = EssentiaAnalyzer()
youtube_downloader = YoutubeSongDownloader()

event_stream = RedisStreaming(redis_host=os.getenv('REDIS_HOST'), redis_port=os.getenv('REDIS_PORT'), redis_db=os.getenv('REDIS_DB'))

stream_name = "get-song-data"
consumer_group_name = "get-song-data-grp"
consumer = "get-song-data-grp-consumer-filtering-app"


def main(processor):
  setup_logging()

  cmd = ExtractSongDataCommandHandler(analy_song_api=essentia_analyzer, song_repo=song_repo, download_api=youtube_downloader, stream=event_stream)

  try:
    while True:
      msgs = event_stream.consume(stream_name=stream_name, group_name=consumer_group_name, consumer_name=f"{consumer}-{processor}")
      for event_id, data in msgs:
        try:
          print(f"Received message: {data}")
          cmd.handle(ExtractSongDataCommand(id=uuid.UUID(data["id"])))
          event_stream.ack(stream_name, consumer_group_name, event_id)

        except Exception as e:
          event_stream.ack(stream_name, consumer_group_name, event_id)
          logging.error(f"Error occurred: {e}")  # Print the error message    
  except KeyboardInterrupt:
    print("Subscriber stopped.")


if __name__ == "__main__":
  # parser = argparse.ArgumentParser(description="Process some inputs.")
  parser = argparse.ArgumentParser(description="Process some inputs.")
  parser.add_argument("--process", type=int, help="process", required=True)
  
  args = parser.parse_args()

  main(args.process)
