from dataclasses import field, dataclass

import numpy as np
import pandas as pd
import random

from modules.songs.domain.song_repo import SongRepo, SongsFilter

@dataclass
class ClassificationFilters():
  weight: int
  filters: list[SongsFilter]

@dataclass
class FilterSongsCmd():
  is_all: bool = False
  song_ids: list[str] = field(default_factory=list)
  filters: list[ClassificationFilters] = field(default_factory=list)
  total_songs: int = 50

@dataclass
class FilterSongsHandler():
  song_repo: SongRepo

  def handle(self, cmd:FilterSongsCmd) -> list[str]:
    # songs = self.song_repo.get_all_songs() if cmd.is_all else self.song_repo.get_songs_by_ids(cmd.song_ids)

    # df = pd.DataFrame([song.__dict__ for song in songs])

    classification_id_list_with_weight = []
    
    for classification_filter in cmd.filters:

      songs = self.song_repo.filter_songs(classification_filter.filters)
      song_ids = [song.id for song in songs]

      classification_id_list_with_weight.append({"filter": classification_filter, "ids": song_ids})


    return get_ids_per_weight(classification_id_list_with_weight, cmd.total_songs)
    # perform filtering on the df depending on the filters
    # df_mood = df[]
    # print(len(songs))
    
    
def get_ids_per_weight(classification_list:list, total_songs):
  sum_of_weights = sum(item['filter'].weight for item in classification_list)

  all_songs = []
  for classification in classification_list:
    nb_of_songs = (classification['filter'].weight / sum_of_weights) * total_songs

    if len(classification['ids']) < nb_of_songs:
      raise(Exception(f"{classification['filter']} result has only {len(classification['ids'])} songs"))
    # randomly get nb_of_songs from the list of ids
    random_songs = random.sample(classification['ids'], int(nb_of_songs))
    all_songs.extend(random_songs)

  return all_songs
