from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modules.songs.application.queries.get_song_features_qry import GetSongFeaturesCommand, GetSongFeaturesQueryHandler
from modules.songs.infrastructure.essentia_features.essentia_extract_features import EssentiaExtractFeatures
from modules.songs.infrastructure.sqlalchemy.song_repo import SQLAlchemySongRepository


DATABASE_URL = "postgresql://root:test@localhost:5434/test"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

song_repo = SQLAlchemySongRepository(session=session)
feature_api = EssentiaExtractFeatures()
query = GetSongFeaturesQueryHandler(extract_song_features=feature_api, song_repo=song_repo)

def main():

  result = query.handle(GetSongFeaturesCommand(id="9f384aa4-4c00-4bc6-bec1-260232e57ed4"))
  print(result)
  # records = song_repo.get_songs_by_ids(["9f384aa4-4c00-4bc6-bec1-260232e57ed4"])

  # for song in records:
  #   print(song.genre_features)

if __name__ == "__main__":

  main()
