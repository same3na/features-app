from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict

@dataclass()
class EventStreamingInterface(ABC):

  @abstractmethod
  def add(self, stream:str, data:dict):
    """Add message to the stream"""

  @abstractmethod
  def consume(self, stream_name:str, group_name:str, consumer_name:str) -> list:
    """consume from stream"""

  @abstractmethod
  def ack(self, stream_name:str, group_name:str, message_id:str):
    """must be called in while consuming messages"""