from sqlalchemy import select
from sqlalchemy.orm import Session
from modules.songs.infrastructure.sqlalchemy.song_orm import SongORM  # ORM model
from modules.songs.domain.song import Song
from modules.songs.domain.song_repo import SongRepo, SongsFilter  # Domain model
from sqlalchemy.exc import IntegrityError

class SQLAlchemySongRepository(SongRepo):
  def __init__(self, session: Session):
    self.session = session

  def save_analyze_features(self, song:Song):
    db_model = SongORM.from_domain(song=song)
    try:
      # Use merge to insert or update
      self.session.merge(db_model)
      self.session.commit()
    except IntegrityError:
      self.session.rollback()  # Rollback in case of errors
      raise

  def get_song_by_id(self, song_id: str) -> Song | None:
    try:
      # Query the database for a single song
      song = (
          self.session.query(SongORM)
          .filter(SongORM.song_id == song_id)
          .one_or_none()  # Returns None if no result found
      )

      # Convert ORM object to domain object if found
      return song.to_domain() if song else None  

    except Exception as e:
      self.session.rollback()  # Rollback in case of errors
      raise e  # Re-raise the exception for handling at a higher level
  
  def get_songs_by_ids(self, ids: list[str]) -> list[Song]:
    try:
      # Query database for songs matching the given IDs
      songs = (
        self.session.query(SongORM)
        .filter(SongORM.song_id.in_(ids))
        .all()
      )

      # Convert ORM objects to domain objects
      return [song.to_domain() for song in songs]
    
    except Exception as e:
      self.session.rollback()  # Rollback in case of errors
      raise e  # Re-raise the exception for handling at a higher level

  def get_all_songs(self) -> list[Song]:
    """Get all songs."""
    try:
      # Query database for songs matching the given IDs
      songs = (
        self.session.query(SongORM)
        .all()
      )

      # Convert ORM objects to domain objects
      return [song.to_domain() for song in songs]
    
    except Exception as e:
      self.session.rollback()  # Rollback in case of errors
      raise e  # Re-raise the exception for handling at a higher level

  def filter_songs(self, filters:list[SongsFilter], ids:list = []) -> list[Song]:
    try:
      stmt = select(SongORM)

      for filter in filters:
        if filter.feature == "mood":
          filter_value = [{"name": value} for value in filter.value.split(",")]

          if filter.operation == "in":
            stmt = stmt.where(SongORM.mood.contains(filter_value))
          elif filter.operation == "not_in":
            stmt = stmt.where(SongORM.mood.contains(filter_value))

        if filter.feature == "genre":
          filter_value = [{"name": value} for value in filter.value.split(",")]

          if filter.operation == "in":
            stmt = stmt.where(SongORM.genre.contains(filter_value))
          elif filter.operation == "not_in":
            stmt = stmt.where(SongORM.genre.contains(filter_value))

        feature_mapping = {
          "aggressive": SongORM.aggressive,
          "engagement": SongORM.engagement,
          "happy": SongORM.happy,
          "relaxed": SongORM.relaxed,
          "sad": SongORM.sad,
          "mood": SongORM.mood
        }

        if filter.feature in feature_mapping:
          column = feature_mapping[filter.feature]
          if filter.operation == "<":
            stmt = stmt.where(column < int(filter.value))
          elif filter.operation == ">":
            stmt = stmt.where(column > int(filter.value))
            
      songs = self.session.execute(stmt).scalars().all()

      # Convert ORM objects to domain objects
      return [song.to_domain() for song in songs]
    
    except Exception as e:
      self.session.rollback()  # Rollback in case of errors
      raise e  # Re-raise the exception for handling at a higher level

  def get_feature_all_songs(self, feature:str, ids:list = []) -> list[Song]:
    try:
      selected_columns = ['song_id']  # Default to selecting 'song_id' and 'features'

      if feature == 'mood':
        selected_columns.append("mood_features")

      if feature == 'relaxed':
        selected_columns.append("relaxed_features")

      columns = [getattr(SongORM, col) for col in selected_columns]

      query = self.session.query(*columns)

      if ids:
        query = query.filter(SongORM.song_id.in_(ids))

      results = (
        query
        .all()
      )

      songs = []
      for row in results:
        # Convert the row tuple to a dictionary so to_domain() works properly
        row_dict = {col: getattr(row, col) for col in selected_columns}  # Map columns to dictionary keys
        song = SongORM(**row_dict).to_domain()  # Create SongORM instance, then convert to Song
        songs.append(song)

      return songs
    except Exception as e:
      self.session.rollback()  # Rollback in case of errors
      raise e  # Re-raise the exception for handling at a higher level


  def save_predicition_features(self, song:Song):
    db_model = SongORM.from_domain(song=song)

    """Save the prediction features."""
    song = self.session.get(SongORM, db_model.song_id)

    if song:
      # if db_model.features is not None:
      #   song.features = db_model.features
      if db_model.genre is not None:
        song.genre = db_model.genre
      if db_model.aggressive is not None:
        song.aggressive = db_model.aggressive
      if db_model.engagement is not None:
        song.engagement = db_model.engagement
      if db_model.happy is not None:
        song.happy = db_model.happy
      if db_model.relaxed is not None:
        song.relaxed = db_model.relaxed
      if db_model.sad is not None:
        song.sad = db_model.sad
      if db_model.mood is not None:
        song.mood = db_model.mood

      self.session.commit()
