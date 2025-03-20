from abc import ABC, abstractmethod
from dataclasses import dataclass
import os


@dataclass()
class ExternalSongUrl(ABC):

  @abstractmethod
  def get_url(self, title:str, artist: str, album: str) -> str:
    """Get the url of a song"""
