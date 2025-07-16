from dataclasses import dataclass

from modules.songs.application.commands.feature_clustering_cmd import FeatureClusteringCmdHandler, FeatureClusteringCmd
from modules.songs.domain.song_repo import SongRepo
import pandas as pd


@dataclass
class SongService:
  song_repo: SongRepo

  def feature_clustering(self, ids: list[str]):
    songs = self.song_repo.get_songs_by_ids(ids)
    df_init = pd.DataFrame([song.__dict__ for song in songs])
    ids = df_init['id'].astype(str)
    df_init = df_init.drop(columns=["id"])
    external_url = FeatureClusteringCmdHandler()

    labels, clusters_df, cluster_tag = external_url.handle(FeatureClusteringCmd(
      features_df=df_init
    ))

    print(cluster_tag)

    # return list of dictionaries specififying the cluster with it's name, then the ids of the songs in that cluster

    # create a df of the ids and the labels
    df_labels = pd.DataFrame({
      "id": ids,
      "label": labels
    })

    # construct a dictionary for each cluster
    # getting the index of each cluster from the clusters_df index
    # knowing that clusters_df[label] is a tag of the cluster
    clusters = []
    for idx, cluster_id in enumerate(clusters_df.index):
      cluster_songs = df_labels[df_labels['label'] == cluster_id]['id'].tolist()
      clusters.append({
        "cluster_id": str(cluster_id),
        "songs": cluster_songs,
        "features": clusters_df.loc[cluster_id].to_dict(),
        "label": cluster_tag[idx]
      })

    return clusters
  # end of feature_clustering
# end of SongService
# This service provides methods to handle song-related operations, such as clustering songs based on their features.
# It uses the SongRepo to interact with the song data and applies clustering algorithms to group songs based on their features.
