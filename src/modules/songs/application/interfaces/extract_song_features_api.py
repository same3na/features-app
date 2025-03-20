from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np

from modules.songs.domain.song import SongJsonFeatures

@dataclass()
class ExtractSongFeaturesApi(ABC):

  @abstractmethod
  def load_audio(self, audio_path:str):
    """passing the audio"""

  @abstractmethod
  def extract_genre(self) -> list[SongJsonFeatures]:
    """Get the url of a song"""

  @abstractmethod
  def extract_mood(self) -> list[SongJsonFeatures]:
    """Return the Mood array"""

  @abstractmethod
  def extract_aggressive(self) -> int:
    """Return the aggressivity"""

  @abstractmethod
  def extract_engagement(self) -> int:
    """Music engagement predicts whether the music evokes active attention of the listener (high-engagement “lean forward” active listening vs. low-engagement “lean back” background listening)."""

  @abstractmethod
  def extract_happy(self) -> int:
    """Return the Happiness array"""

  @abstractmethod
  def extract_relaxed(self) -> int:
    """Return the Happiness array"""

  @abstractmethod
  def extract_sad(self) -> int:
    """Return the Sad array"""

