import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modules.songs.application.queries.get_song_features_qry import GetSongFeaturesCommand, GetSongFeaturesQueryHandler
from modules.songs.infrastructure.essentia_features.essentia_extract_features import EssentiaExtractFeatures
from modules.songs.infrastructure.sqlalchemy.song_repo import SQLAlchemySongRepository
from modules.songs.application.commands.download_song_cmd import DownloadSongCommand, DownloadSongCommandHandler
from modules.songs.infrastructure.youtube_external_url import YoutubeExternalUrl

from modules.songs.infrastructure.youtube_song_downloader import YoutubeSongDownloader
from modules.common.infrastructure.redis_streaming import RedisStreaming



DATABASE_URL = "postgresql://root:test@localhost:5434/test"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

song_repo = SQLAlchemySongRepository(session=session)
feature_api = EssentiaExtractFeatures()
query = GetSongFeaturesQueryHandler(extract_song_features=feature_api, song_repo=song_repo)

external_url = YoutubeExternalUrl()
youtube_downloader = YoutubeSongDownloader()
event_stream = RedisStreaming(redis_host=os.getenv('REDIS_HOST'), redis_port=os.getenv('REDIS_PORT'), redis_db=os.getenv('REDIS_DB'))

donwload_song_cmd = DownloadSongCommandHandler(download_api=youtube_downloader, stream=event_stream, external_song_url=external_url)


def main():

  donwload_song_cmd.handle(DownloadSongCommand(id="b0f85239-0f00-4a08-8eed-9e504e9696bc", title="codex", artist="radiohead", album="The King of Limbs"))


  # result = query.handle(GetSongFeaturesCommand(id="9f384aa4-4c00-4bc6-bec1-260232e57ed4"))
  # print(result)
  # records = song_repo.get_songs_by_ids(["9f384aa4-4c00-4bc6-bec1-260232e57ed4"])

  # for song in records:
  #   print(song.genre_features)

if __name__ == "__main__":

  main()
