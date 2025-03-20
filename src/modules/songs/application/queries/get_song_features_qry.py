from dataclasses import dataclass
import uuid

import numpy as np

from modules.songs.application.interfaces.extract_song_features_api import ExtractSongFeaturesApi
from modules.songs.domain.song_repo import SongRepo

@dataclass
class GetSongFeaturesCommand():
  id: uuid.UUID

@dataclass
class GetSongFeaturesQueryHandler():
  extract_song_features:ExtractSongFeaturesApi
  song_repo:SongRepo

  def handle(self, qry:GetSongFeaturesCommand):
    song = self.song_repo.get_song_by_id(qry.id)

    if song is None:
      raise Exception("No Song with the given id")
  

    return {"genres": song.genre, "aggressive": song.aggressive, "engagement": song.engagement, "happy": song.happy, "relaxed": song.relaxed, "sad": song.sad, "moods": song.mood}
