
import json

from multiprocessing import Pool
from modules.common.infrastructure.redis_pub_sub import RedisPubSub
from modules.common.infrastructure.redis_streaming import RedisStreaming
from modules.songs.application.commands.analyze_song_cmd import AnalyzeSongCommand, AnalyzeSongCommandHandler
from modules.songs.infrastructure.essentia_analyzer import EssentiaAnalyzer
from modules.songs.infrastructure.sqlalchemy.song_repo import SQLAlchemySongRepository
from modules.songs.infrastructure.youtube_external_url import YoutubeExternalUrl
from modules.songs.infrastructure.youtube_song_downloader import YoutubeSongDownloader
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://root:test@localhost:5434/test"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

youtube_downloader = YoutubeSongDownloader()
essentia_analyzer = EssentiaAnalyzer()
song_repo = SQLAlchemySongRepository(session=session)
event_stream = RedisStreaming(redis_host="localhost", redis_port=6379, redis_db=0)
external_url = YoutubeExternalUrl()

redis_pub_sub = RedisPubSub(redis_host="localhost", redis_port=6379, redis_db=0)

analyze_song_cmd = AnalyzeSongCommandHandler(download_api=youtube_downloader, analyze_song_api=essentia_analyzer, song_repo=song_repo, stream=event_stream, external_song_url=external_url, pub_sub=redis_pub_sub)


def process_message(message):
  # data = message['data']
  print(f"Received message: {message['data'].decode('utf-8')}")

  data = message['data'].decode('utf-8')
  data = json.loads(data)
  data = data['Data']

  # execute the command
  analyze_song_cmd.handle(AnalyzeSongCommand(id=data["song_id"], title=data["song_name"], artist=data["artist_name"], album=data["album_name"]))


def main():
  # multiprocessing.set_start_method("spawn")

  redis_pub_sub = RedisPubSub(redis_host="localhost", redis_port=6379, redis_db=0)
  redis_pub_sub.subscribe("SongAdded")
  pool = Pool(processes=3)  # Limit to 3 simultaneous processes

  try:
    for message in redis_pub_sub.listen("SongAdded"):
      if message['type'] == 'message':
        pool.apply_async(process_message, args=(message,))   

  except KeyboardInterrupt:
    print("Subscriber stopped.")

if __name__ == "__main__":
  main()
