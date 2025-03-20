import json
import pickle
from sqlalchemy import UUID, Column, LargeBinary, Integer, Table, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
import uuid

from modules.songs.domain.song import Song

Base = declarative_base()

class SongORM(Base):

  __tablename__ = "song_features"

  song_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # Primary key
  # features = Column(JSONB, nullable=False)  # Store song features as JSONB
  genre = Column(JSONB, nullable=True)  # Store song features as JSONB
  mood = Column(JSONB, nullable=True)  # Store song features as JSONB
  aggressive = Column(Integer, nullable=True)
  happy = Column(Integer, nullable=True)
  sad = Column(Integer, nullable=True)
  relaxed = Column(Integer, nullable=True)
  engagement = Column(Integer, nullable=True)

  def to_domain(self) -> Song:
    return Song(
      id=self.song_id,
      # features=self.features,
      genre=self.genre,
      aggressive=self.aggressive,
      engagement=self.engagement,
      happy=self.happy,
      relaxed=self.relaxed,
      sad=self.sad,
      mood=self.mood,
    )

  @staticmethod
  def from_domain(song: Song) -> "SongORM":
    return SongORM(
      song_id=song.id,
      # features=song.features.model_dump() if song.features is not None else None,
      genre=[genre.model_dump() for genre in song.genre] if song.genre is not None else None,
      mood=[mood.model_dump() for mood in song.mood] if song.mood is not None else None,
      aggressive=song.aggressive,
      engagement=song.engagement,
      happy=song.happy,
      relaxed=song.relaxed,
      sad=song.sad,
    )
