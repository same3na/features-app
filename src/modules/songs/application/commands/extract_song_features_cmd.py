from dataclasses import dataclass
import os
import pickle
import uuid
import logging

from modules.common.application.interfaces.event_streaming_interface import EventStreamingInterface
from modules.songs.application.interfaces.download_song_api import DownloadSongApi
from modules.songs.application.interfaces.extract_song_features_api import ExtractSongFeaturesApi
from modules.songs.domain.song import Song
from modules.songs.domain.song_repo import SongRepo


@dataclass
class ExtractSongFeaturesCommand():
  id: uuid.UUID
  url: str

@dataclass
class ExtractSongFeaturesCommandHandler():
  download_api:DownloadSongApi
  extract_song_features:ExtractSongFeaturesApi
  song_repo:SongRepo
  stream:EventStreamingInterface


  def handle(self, cmd:ExtractSongFeaturesCommand):
    # use to decode it pickle.loads(blob_data)

    try:

      # check first if audio is downloaded
      song_downloaded_path = self.download_api.getFullDownloadPath(cmd.id)
      
      # if not os.path.exists(song_downloaded_path):
      #   # download the song
      #   self.download_api.download_sample(cmd.id, cmd.url)

      if not os.path.exists(song_downloaded_path):
        raise Exception(f"Path does not exist: {song_downloaded_path}")

      self.extract_song_features.load_audio(song_downloaded_path)
      genre_predictions = self.extract_song_features.extract_genre()
      aggressive_pred = self.extract_song_features.extract_aggressive()
      engagement_pred = self.extract_song_features.extract_engagement()
      happy_pred = self.extract_song_features.extract_happy()
      relaxed_pred = self.extract_song_features.extract_relaxed()
      sad_pred = self.extract_song_features.extract_sad()
      mood_pred = self.extract_song_features.extract_mood()

      song = Song(
        id=cmd.id,
        genre=genre_predictions, 
        aggressive=aggressive_pred, 
        engagement=engagement_pred, 
        happy=happy_pred,
        relaxed=relaxed_pred,
        sad=sad_pred,
        mood=mood_pred)

      self.song_repo.save_predicition_features(song)

      body = {
        "id": str(cmd.id),
        "success": "true",
      }

      self.stream.add(stream="analyzed-songs", data=body)


      # delete the sample file
      # os.remove(song_downloaded_path)

    except Exception as e:
      # notify that the song has been analyzed successfully
      # transform the body to bytes
      body = {
        "id": str(cmd.id),
        "success": "false",
      }
      logging.error(f"Error ExtractSongFeaturesCommandHandler {e}")
      self.stream.add(stream="analyzed-songs", data=body)