
from dataclasses import dataclass
import json

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import StandardScaler

from modules.common.application.interfaces.event_streaming_interface import EventStreamingInterface
from modules.songs.domain.song_repo import SongRepo

@dataclass
class ApplyClustering():
  cluster_id: str
  nb_of_clusters: int
  ids: list

@dataclass
class ApplyClusteringHandler():
  song_repo: SongRepo
  event_stream: EventStreamingInterface
  df: pd.DataFrame = None

  def handle(self, command:ApplyClustering):
    # get data
    songs = self.song_repo.get_songs_by_ids(ids=command.ids)
    self.df = pd.DataFrame([song.__dict__ for song in songs])
    clusters = self.perform_clustering(command.nb_of_clusters, 32)
    # save results in database
    clusters['id'] = clusters['id'].apply(lambda x: str(x))
    self.event_stream.add("song-clustering", data = {
      "cluster_id": command.cluster_id,
      "records": json.dumps(clusters.to_dict(orient="records")).encode('utf-8')
    })
    
  def perform_clustering(self, nb_clusters, random_state):
  
    if self.df.empty:
      raise ValueError("Input data is empty.")

    self.df = pd.concat([self.df['id'], pd.json_normalize(self.df['features'])], axis=1)

    # make sure to remove rows with null values
    self.df = self.df[~self.df.isna().any(axis=1)]
    self.df.reset_index(drop=True, inplace=True)

    # store ids for later
    result_df = self.df

    self.df = self.df.drop(columns=['id'])

    # barkbands
    self._handling_barkbands()

    # gfcc
    self._handling_gfcc()

    # HPCP
    self._handling_hpcp()

    # mfcc
    self._handling_mfcc()

    # erbands
    self._handling_erbands()

    # melbands
    self._handling_melbands()

    # genre
    self._handling_genre()

    # handling_chords_key
    self._handling_chords_key() 

    # spectral_contrast_coeffs
    self._handle_spectral_contrast_coeffs()

    # beats_loudness_band_ratio
    self._handle_beats_loudness_band_ratio()

    # spectral_contrast_valleys
    self._handle_spectral_contrast_valleys()

    # map_chords_scale
    self._map_chords_scale()

    # Step 1: Standardize the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(self.df)

    # Step 2: Apply PCA to retain 95% of the variance
    pca = PCA(n_components=0.90)  # Retain 95% variance
    pca_components = pca.fit_transform(scaled_data)

    kmeans = KMeans(init="k-means++",n_clusters=nb_clusters,random_state=random_state)
    clusters = kmeans.fit_predict(pca_components)

    result_df['cluster'] = clusters
    return result_df[['id', 'cluster']]

  def _handling_barkbands(self):
    # Aggregate the bands
    def aggregate_method(bands, column_name):
      low_freq = sum(bands[:9]) / 9
      mid_freq = sum(bands[9:18]) / 9
      high_freq = sum(bands[18:]) / 9
      return pd.Series([low_freq, mid_freq, high_freq], index=[f"{column_name}_low_freq", f"{column_name}_mid_freq", f"{column_name}_high_freq"])

    barkbands_mean = self.df["barkbands.mean"].apply(aggregate_method, column_name="barkbands_mean")
    self.df = self.df.drop(columns=["barkbands.mean"]).join(barkbands_mean)

  def _handling_gfcc(self):
    gfcc_expanded = pd.DataFrame(
      self.df["gfcc.mean"].tolist(), 
      columns=[f"gfcc.mean_{i+1}" for i in range(len(self.df["gfcc.mean"][0]))]
    )
    self.df = self.df.drop(columns=['gfcc.mean']).join(gfcc_expanded)

  def _handling_hpcp(self):
    def map_to_chroma(hpcp):
      chroma = [0] * 12  # Initialize 12 chroma bins
      for i, value in enumerate(hpcp):
          chroma[i % 12] += value
      return chroma
    
    # Apply mapping to create chroma bins
    self.df[["hpcp.mean_C", "hpcp.mean_C#", "hpcp.mean_D", "hpcp.mean_D#", "hpcp.mean_E", "hpcp.mean_F",
        "hpcp.mean_F#", "hpcp.mean_G", "hpcp.mean_G#", "hpcp.mean_A", "hpcp.mean_A#", "hpcp.mean_B"]] = pd.DataFrame(
        self.df["hpcp.mean"].apply(map_to_chroma).tolist()
    )
    self.df = self.df.drop(columns=['hpcp.mean'])

  def _handling_mfcc(self):
    # mfcc
    mfcc_expanded = pd.DataFrame(
        self.df["mfcc.mean"].tolist(), 
        columns=[f"mfcc.mean_{i+1}" for i in range(len(self.df["mfcc.mean"][0]))]
    )
    self.df = self.df.drop(columns=['mfcc.mean']).join(mfcc_expanded)

  def _handling_erbands(self):
    erbbands_expanded = pd.DataFrame(
      self.df["erbbands.mean"].tolist(), 
      columns=[f"erbbands.mean_{i+1}" for i in range(len(self.df["erbbands.mean"][0]))]
    )
    self.df = self.df.drop(columns=['erbbands.mean']).join(erbbands_expanded)
  
  def _handling_melbands(self):
    self.df = self.df.drop(columns=['melbands.mean'])
  
  def _handling_genre(self):
    self.df = self.df.drop(columns=['genre'])

  def _handling_chords_key(self):
    # map the chord keys
    chord_to_int = {
      "C": 0,
      "Cb": 1,
      "C#": 2,
      "D": 3,
      "Db": 4,
      "D#": 5,
      "E": 6,
      "Eb": 7,
      "E#": 8,
      "F": 9,
      "Fb": 10,
      "F#":11,
      "G": 12,
      "Gb": 13,
      "G#": 14,
      "A": 15,
      "Ab": 16,
      "A#": 17,
      "B": 18,
      "B#": 19,
      "Bb": 20
    }
    self.df['chords_key_encoded'] = self.df['chords_key'].map(chord_to_int)
    self.df = self.df.drop(columns=['chords_key'])

  def _handle_spectral_contrast_coeffs(self):
    spectral_contrast_coeffs_expanded = pd.DataFrame(
      self.df["spectral_contrast_coeffs.mean"].tolist(), 
      columns=[f"spectral_contrast_coeffs.mean_{i+1}" for i in range(len(self.df["spectral_contrast_coeffs.mean"][0]))]
    )
    self.df = self.df.drop(columns=['spectral_contrast_coeffs.mean']).join(spectral_contrast_coeffs_expanded)

  def _handle_beats_loudness_band_ratio(self):
    beats_loudness_band_ratio_expanded = pd.DataFrame(
      self.df["beats_loudness_band_ratio.mean"].tolist(), 
      columns=[f"beats_loudness_band_ratio.mean_{i+1}" for i in range(len(self.df["beats_loudness_band_ratio.mean"][0]))]
    )
    self.df = self.df.drop(columns=['beats_loudness_band_ratio.mean']).join(beats_loudness_band_ratio_expanded)
  
  def _handle_spectral_contrast_valleys(self):
    spectral_contrast_valleys_expanded = pd.DataFrame(
      self.df["spectral_contrast_valleys.mean"].tolist(), 
      columns=[f"spectral_contrast_valleys.mean_{i+1}" for i in range(len(self.df["spectral_contrast_valleys.mean"][0]))]
    )
    self.df = self.df.drop(columns=['spectral_contrast_valleys.mean']).join(spectral_contrast_valleys_expanded)

  def _map_chords_scale(self):
    # map the chords scale
    chord_scale_to_int = {
      "minor": 0,
      "major": 1,
    }
    self.df['chords_scale_encoded'] = self.df['chords_scale'].map(chord_scale_to_int)
    self.df = self.df.drop(columns=['chords_scale'])
