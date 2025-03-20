import redis
from dataclasses import dataclass

from modules.common.application.interfaces.event_streaming_interface import EventStreamingInterface


@dataclass()
class RedisStreaming(EventStreamingInterface):
  redis_client:redis.Redis = None

  def __init__(self, redis_host:str, redis_port:int, redis_db:int):
    self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

  def add(self, stream:str, data:dict):
    """Adding the message to the stream"""
    self.redis_client.xadd(stream, data)