from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass()
class PubSubInterface(ABC):

  @abstractmethod
  def subscribe(self, channel:str):
    """Subscribe for a channel"""

  @abstractmethod
  def listen(self, channel:str):
    """Listen for new messages in a channel"""

  @abstractmethod
  def publish(self, channel:str, msg:any):
    """Publish message to channel"""