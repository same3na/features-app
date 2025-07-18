
import argparse
import json
import os
import uuid
import logging

from logging_config import setup_logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.common.infrastructure.redis_pub_sub import RedisPubSub
from modules.common.infrastructure.redis_streaming import RedisStreaming
from modules.songs.application.commands.extract_song_features_cmd import ExtractSongFeaturesCommand, ExtractSongFeaturesCommandHandler
from modules.songs.infrastructure.essentia_features.essentia_extract_features import EssentiaExtractFeatures
from modules.songs.infrastructure.sqlalchemy.song_repo import SQLAlchemySongRepository
from modules.songs.infrastructure.youtube_song_downloader import YoutubeSongDownloader

DATABASE_URL = f"postgresql://{os.getenv('DBUSER')}:{os.getenv('DBPASS')}@{os.getenv('DBHOST')}:{os.getenv('DBPORT')}/{os.getenv('DBNAME')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

song_repo = SQLAlchemySongRepository(session=session)
feature_api = EssentiaExtractFeatures()

youtube_downloader = YoutubeSongDownloader()

event_stream = RedisStreaming(redis_host=os.getenv('REDIS_HOST'), redis_port=os.getenv('REDIS_PORT'), redis_db=os.getenv('REDIS_DB'))

stream_name = "get-song-features"
consumer_group_name = "get-song-features-grp"
consumer = "get-song-features-grp-consumer-filtering-app"

def main(processor):
  setup_logging()

  cmd = ExtractSongFeaturesCommandHandler(extract_song_features=feature_api, song_repo=song_repo, download_api=youtube_downloader, stream=event_stream)

  try:
    while True:
      msgs = event_stream.consume(stream_name=stream_name, group_name=consumer_group_name, consumer_name=f"{consumer}-{processor}")
      for event_id, data in msgs:
        try:
          cmd.handle(ExtractSongFeaturesCommand(id=uuid.UUID(data["id"]), url=data["url"]))
          event_stream.ack(stream_name, consumer_group_name, event_id)

        except Exception as e:
          event_stream.ack(stream_name, consumer_group_name, event_id)
          logging.error(f"Error extract_song_features {e}")
  except KeyboardInterrupt:
    print("Subscriber stopped.")


if __name__ == "__main__":
  # parser = argparse.ArgumentParser(description="Process some inputs.")
  parser = argparse.ArgumentParser(description="Process some inputs.")
  parser.add_argument("--process", type=int, help="process", required=True)
  
  args = parser.parse_args()

  main(args.process)
