
from abc import ABC, abstractmethod
from dataclasses import dataclass

from modules.songs.domain.song import Song

@dataclass()
class DownloadSongApi(ABC):
  SAMPLE_DURATION = -1
  audio_codec: str = "wav"
  download_path: str = "/tmp"


  @abstractmethod
  def download_sample(self, id: str, url: str): 
    """Download a one minute sample. and return the path"""
    
  def getSampleDuration(self):
    return self.SAMPLE_DURATION
  
  def getAudioCodec(self):
    return self.audio_codec
  
  def getDownloadPath(self):
    return self.download_path
  
  def getFullDownloadPath(self, id):
    return f'{self.download_path}/{id}.{self.audio_codec}'

