
from dataclasses import dataclass
import os

import numpy as np

from essentia.standard import MonoLoader, TensorflowPredictEffnetDiscogs, TensorflowPredict2D
from modules.songs.application.interfaces.extract_song_features_api import ExtractSongFeaturesApi
from modules.songs.domain.song import SongJsonFeatures


@dataclass()
class EssentiaExtractFeatures(ExtractSongFeaturesApi):
  audio:any = None
  discogs_effnet_embeddings: any = None
  genre_labels = ["60s","70s","80s","90s","acidjazz","alternative","alternativerock","ambient","atmospheric","blues","bluesrock","bossanova","breakbeat","celtic","chanson","chillout","choir","classical","classicrock","club","contemporary","country","dance","darkambient","darkwave","deephouse","disco","downtempo","drumnbass","dub","dubstep","easylistening","edm","electronic","electronica","electropop","ethno","eurodance","experimental","folk","funk","fusion","groove","grunge","hard","hardrock","hiphop","house","idm","improvisation","indie","industrial","instrumentalpop","instrumentalrock","jazz","jazzfusion","latin","lounge","medieval","metal","minimal","newage","newwave","orchestral","pop","popfolk","poprock","postrock","progressive","psychedelic","punkrock","rap","reggae","rnb","rock","rocknroll","singersongwriter","soul","soundtrack","swing","symphonic","synthpop","techno","trance","triphop","world","worldfusion"]
  mood_labels = ["action","adventure","advertising","background","ballad","calm","children","christmas","commercial","cool","corporate","dark","deep","documentary","drama","dramatic","dream","emotional","energetic","epic","fast","film","fun","funny","game","groovy","happy","heavy","holiday","hopeful","inspiring","love","meditative","melancholic","melodic","motivational","movie","nature","party","positive","powerful","relaxing","retro","romantic","sad","sexy","slow","soft","soundscape","space","sport","summer","trailer","travel","upbeat","uplifting"]
  
  def load_audio(self, audio_path:str):
    if not os.path.exists(audio_path):
      raise Exception(f"Path does not exist: {audio_path}")

    self.audio = MonoLoader(filename=audio_path, sampleRate=16000, resampleQuality=4)()

    embedding_model = TensorflowPredictEffnetDiscogs(graphFilename="src/modules/songs/infrastructure/essentia_features/models/discogs-effnet-bs64-1.pb", output="PartitionedCall:1")
    self.discogs_effnet_embeddings = embedding_model(self.audio)

  def extract_genre(self) -> list[SongJsonFeatures]:
    if self.discogs_effnet_embeddings is None:
      raise ValueError("discogs_effnet_embeddings is not initialized. Call load_audio() first.")
    
    model = TensorflowPredict2D(graphFilename="src/modules/songs/infrastructure/essentia_features/models/mtg_jamendo_genre-discogs-effnet-1.pb")
    predictions = model(self.discogs_effnet_embeddings)

    avg_predictions = np.mean(predictions, axis=0)
    
    # Get the top 5 genre indices
    top5_indices = np.argsort(avg_predictions)[-5:][::-1]
    top5_genres = [SongJsonFeatures(name=self.genre_labels[i], value=round(avg_predictions[i] * 100)) for i in top5_indices]

    return top5_genres
  
  def extract_mood(self) -> list[SongJsonFeatures]:
    """Return the Mood array"""

    if self.discogs_effnet_embeddings is None:
      raise ValueError("discogs_effnet_embeddings is not initialized. Call load_audio() first.")

    model = TensorflowPredict2D(graphFilename="src/modules/songs/infrastructure/essentia_features/models/mtg_jamendo_moodtheme-discogs-effnet-1.pb")
    predictions = model(self.discogs_effnet_embeddings)

    avg_predictions = np.mean(predictions, axis=0)
    
    # Get the top 5 genre indices
    top5_indices = np.argsort(avg_predictions)[-5:][::-1]
    top5_genres = [SongJsonFeatures(name=self.mood_labels[i], value=round(avg_predictions[i] * 100)) for i in top5_indices]

    return top5_genres

  def extract_aggressive(self) -> int:
    """Return the aggressivity array"""
    
    if self.discogs_effnet_embeddings is None:
      raise ValueError("discogs_effnet_embeddings is not initialized. Call load_audio() first.")

    model = TensorflowPredict2D(graphFilename="src/modules/songs/infrastructure/essentia_features/models/mood_aggressive-discogs-effnet-1.pb", output="model/Softmax")
    predictions = model(self.discogs_effnet_embeddings)

    return averaging_probabilities(predictions[:, 0])

  def extract_engagement(self) -> int:
    """Music engagement predicts whether the music evokes active attention of the listener (high-engagement “lean forward” active listening vs. low-engagement “lean back” background listening)."""
    
    if self.discogs_effnet_embeddings is None:
      raise ValueError("discogs_effnet_embeddings is not initialized. Call load_audio() first.")

    model = TensorflowPredict2D(graphFilename="src/modules/songs/infrastructure/essentia_features/models/engagement_regression-discogs-effnet-1.pb", output="model/Identity")
    predictions = model(self.discogs_effnet_embeddings)

    return averaging_probabilities(predictions[:, 0])
  
  def extract_happy(self) -> int:
    """Return the Happiness array"""

    if self.discogs_effnet_embeddings is None:
      raise ValueError("discogs_effnet_embeddings is not initialized. Call load_audio() first.")

    model = TensorflowPredict2D(graphFilename="src/modules/songs/infrastructure/essentia_features/models/mood_happy-discogs-effnet-1.pb", output="model/Softmax")
    predictions = model(self.discogs_effnet_embeddings)

    return averaging_probabilities(predictions[:, 0])

  def extract_relaxed(self) -> int:
    """Return the Party array"""

    if self.discogs_effnet_embeddings is None:
      raise ValueError("discogs_effnet_embeddings is not initialized. Call load_audio() first.")

    model = TensorflowPredict2D(graphFilename="src/modules/songs/infrastructure/essentia_features/models/mood_relaxed-discogs-effnet-1.pb", output="model/Softmax")
    predictions = model(self.discogs_effnet_embeddings)

    return averaging_probabilities(predictions[:, 1])

  def extract_sad(self) -> int:
    """Return the Sad array"""

    if self.discogs_effnet_embeddings is None:
      raise ValueError("discogs_effnet_embeddings is not initialized. Call load_audio() first.")

    model = TensorflowPredict2D(graphFilename="src/modules/songs/infrastructure/essentia_features/models/mood_sad-discogs-effnet-1.pb", output="model/Softmax")
    predictions = model(self.discogs_effnet_embeddings)

    return averaging_probabilities(predictions[:, 1])


def averaging_probabilities(predictions):
  # num_elements = len(predictions[0])  # Detect how many elements are in each sublist
  # if num_elements == 2:
  #     # Extract probabilities for danceable and not danceable
  #     first_probs = [first_prob for first_prob, second_prob in predictions]
  #     second_probs = [second_prob for first_prob, second_prob in predictions]
      
  #     # Compute the mean probabilities
  #     mean_first = sum(first_probs) / len(first_probs)
  #     mean_second = sum(second_probs) / len(second_probs)
  
  #     return f"{mean_first:.2f}", f"{mean_second:.2f}"
      
  # if num_elements == 1:
  #     probs = [first_prob for first_prob in predictions]

  #     mean_first = sum(probs) / len(probs)
  #     return f"{mean_first[0]:.2f}"

  mean = sum(predictions) / len(predictions)
  return round(mean * 100)
