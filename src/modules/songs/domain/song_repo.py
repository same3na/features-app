from abc import ABC, abstractmethod
from dataclasses import dataclass
import uuid

from modules.songs.domain.song import Song, SongData

@dataclass
class SongsFilter():
  feature: str
  operation: str
  value: str

@dataclass()
class SongRepo(ABC):

  @abstractmethod
  def save_analyze_features(self, song:Song):
    """Save the song features."""
  
  @abstractmethod
  def save_predicition_features(self, song:Song):
    """Save the prediction features."""

  @abstractmethod
  def save_song_data(self, songData:SongData):
    """Save the song analyzed data"""

  @abstractmethod
  def get_songs_by_ids(self, ids:list[str]) -> list[Song]:
    """Get songs by list of ids."""

  @abstractmethod
  def get_song_by_id(self, song_id: str) -> Song | None:
    """Get song by id."""

  @abstractmethod
  def get_all_songs(self) -> list[Song]:
    """Get all songs."""

  @abstractmethod
  def filter_songs(self, filters:list[SongsFilter], ids:list = []) -> list[Song]:
    """Filter Songs."""
