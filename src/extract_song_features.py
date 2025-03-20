
import argparse
import json
import uuid
import logging


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.common.infrastructure.redis_pub_sub import RedisPubSub
from modules.common.infrastructure.redis_streaming import RedisStreaming
from modules.songs.application.commands.extract_song_features_cmd import ExtractSongFeaturesCommand, ExtractSongFeaturesCommandHandler
from modules.songs.infrastructure.essentia_features.essentia_extract_features import EssentiaExtractFeatures
from modules.songs.infrastructure.sqlalchemy.song_repo import SQLAlchemySongRepository
from modules.songs.infrastructure.youtube_song_downloader import YoutubeSongDownloader

DATABASE_URL = "postgresql://root:test@localhost:5434/test"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

song_repo = SQLAlchemySongRepository(session=session)
feature_api = EssentiaExtractFeatures()

youtube_downloader = YoutubeSongDownloader()

redis_pub_sub = RedisPubSub(redis_host="localhost", redis_port=6379, redis_db=0)
redis_pub_sub.subscribe("ExtractSongFeatures")
event_stream = RedisStreaming(redis_host="localhost", redis_port=6379, redis_db=0)

def main():
  cmd = ExtractSongFeaturesCommandHandler(extract_song_features=feature_api, song_repo=song_repo, download_api=youtube_downloader, stream=event_stream)

  try:
    for message in redis_pub_sub.listen("ExtractSongFeatures"):
      if message['type'] == 'message':
        # data = message['data']
        print(f"Received message: {message['data'].decode('utf-8')}")
        data = message['data'].decode('utf-8')

        data = json.loads(data)
        data = data['Data']
        logging.debug(f"song id {data['song_id']}")
        
        cmd.handle(ExtractSongFeaturesCommand(id=uuid.UUID(data["song_id"]), url=data["song_url"]))

  except KeyboardInterrupt:
    print("Subscriber stopped.")


if __name__ == "__main__":
  # parser = argparse.ArgumentParser(description="Process some inputs.")
  # parser.add_argument("--id", type=str, help="id", required=True)
  # parser.add_argument("--path", type=str, help="path", required=True)

  # args = parser.parse_args()
  # main(args.path, args.id)

  main()
