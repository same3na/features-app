
from dataclasses import dataclass
import json
import logging

from modules.common.application.interfaces.pub_sub_interface import PubSubInterface
from modules.songs.application.commands.analyze_song_cmd import AnalyzeSongCommand, AnalyzeSongCommandHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_song_added_message(data, cmd):
  logging.info(f"Processing message in Pool: {data}")
    
  try:
    command = AnalyzeSongCommand(
        id=data["song_id"], 
        title=data["song_name"], 
        artist=data["artist_name"]
    )
    cmd.Handle(command)
  except Exception as e:
    print(f"Error handling command: {e}")

@dataclass
class PubSubListener():
  pub_sub: PubSubInterface

  def __init__(self, pub_sub: PubSubInterface, analyze_song_cmd: AnalyzeSongCommandHandler):
    pub_sub.subscribe("SongAdded")
    self.pub_sub = pub_sub
    self.analyze_song_cmd = analyze_song_cmd

  def listenSongAdded(self, pool, analyze_song_cmd: AnalyzeSongCommandHandler):
    logging.info("Listening for messages on 'SongAdded'...")
    for message in self.pub_sub.listen("SongAdded"):
      if message['type'] == 'message':
        print(message)
        try:
          # Extract only serializable data before sending to `apply_async`
          raw_data = message['data'].decode('utf-8')
          parsed_data = json.loads(raw_data)['Data']

          pool.apply_async(process_song_added_message, args=(parsed_data, analyze_song_cmd))
          # process_song_added_message(parsed_data, analyze_song_cmd)

          
        except Exception as e:
          print(f"Error processing message: {e}")



