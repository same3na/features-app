
from abc import ABC, abstractmethod
from dataclasses import dataclass

from modules.songs.domain.features import AnalyzeSongFeatures


@dataclass()
class AnalyzeSongApi(ABC):

  @abstractmethod
  def analyze(self, path: str) -> AnalyzeSongFeatures:
    """Analyze the song."""
  