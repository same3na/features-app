from typing import Any, Callable, Dict
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

  def consume(self, stream_name:str, group_name:str, consumer_name:str) -> list:
    # First, process old (pending) messages
    # messages = self.redis_client.xreadgroup(group_name, consumer_name, {stream_name: "0"}, count=5, block=5000)
    
    # if not messages[0][1]:
    messages = self.redis_client.xreadgroup(group_name, consumer_name, {stream_name: ">"}, count=5, block=5000)

    print(messages)
    msgs = messages[0][1] if messages and messages[0][1] else []

    print(len(msgs))

    return [(id.decode("utf-8"), {key.decode("utf-8"): value.decode("utf-8") for key, value in msg.items()}) for id, msg in msgs]

  
  def ack(self, stream_name:str, group_name:str, message_id:str):
    """must be called in while consuming messages"""
    self.redis_client.xack(stream_name, group_name, message_id)