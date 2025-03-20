
from dataclasses import dataclass, field
import json

import redis

from modules.common.application.interfaces.pub_sub_interface import PubSubInterface


@dataclass()
class RedisPubSub(PubSubInterface):
  redis_client:redis.Redis = None
  subscribers:dict = field(default_factory=dict)

  def __init__(self, redis_host:str, redis_port:int, redis_db:int):
    self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    self.subscribers = {}

  def subscribe(self, channel:str):
    pubsub = self.redis_client.pubsub()

    # Subscribe to the channel
    pubsub.subscribe(channel)
    self.subscribers[channel] = pubsub

  def listen(self, channel:str):
    if channel not in self.subscribers:
      raise Exception(f"Need to subscribe first to channel {channel}")
    
    return self.subscribers[channel].listen()

  def publish(self, channel:str, msg:any):
    """Publish message to channel"""
    self.redis_client.publish(channel, json.dumps({"Data": msg}).encode('utf-8'))