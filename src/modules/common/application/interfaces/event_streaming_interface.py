from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass()
class EventStreamingInterface(ABC):

  @abstractmethod
  def add(self, stream:str, data:dict):
    """Add message to the stream"""
