from pydantic import BaseModel, PositiveInt
from typing_extensions import Dict, List, TypedDict


class AnalyzeSongFeaturesStatesList(BaseModel):
  mean: List[float]

class AnalyzeSongFeaturesStatesListOfList(BaseModel):
  mean: List[List[float]]

class AnalyzeSongFeaturesStates(BaseModel):
  mean: float

class AnalyzeSongFeatures(BaseModel):
  average_loudness: float
  barkbands: AnalyzeSongFeaturesStatesList
  barkbands_crest: AnalyzeSongFeaturesStates
  barkbands_flatness_db: AnalyzeSongFeaturesStates
  barkbands_kurtosis: AnalyzeSongFeaturesStates
  barkbands_skewness: AnalyzeSongFeaturesStates
  barkbands_spread: AnalyzeSongFeaturesStates
  dissonance: AnalyzeSongFeaturesStates
  dynamic_complexity: float
  erbbands: AnalyzeSongFeaturesStatesList
  erbbands_crest: AnalyzeSongFeaturesStates
  erbbands_flatness_db: AnalyzeSongFeaturesStates
  erbbands_kurtosis: AnalyzeSongFeaturesStates
  erbbands_skewness: AnalyzeSongFeaturesStates
  erbbands_spread: AnalyzeSongFeaturesStates
  gfcc: AnalyzeSongFeaturesStatesList
  hfc: AnalyzeSongFeaturesStates
  melbands: AnalyzeSongFeaturesStatesList
  melbands_crest: AnalyzeSongFeaturesStates
  melbands_flatness_db: AnalyzeSongFeaturesStates
  melbands_kurtosis: AnalyzeSongFeaturesStates
  melbands_skewness: AnalyzeSongFeaturesStates
  melbands_spread: AnalyzeSongFeaturesStates
  mfcc: AnalyzeSongFeaturesStatesList
  pitch_salience: AnalyzeSongFeaturesStates
  silence_rate_20dB: AnalyzeSongFeaturesStates
  silence_rate_30dB: AnalyzeSongFeaturesStates
  silence_rate_60dB: AnalyzeSongFeaturesStates
  spectral_centroid: AnalyzeSongFeaturesStates
  spectral_complexity: AnalyzeSongFeaturesStates
  spectral_contrast_coeffs: AnalyzeSongFeaturesStatesList
  spectral_contrast_valleys: AnalyzeSongFeaturesStatesList
  spectral_decrease: AnalyzeSongFeaturesStates
  spectral_energy: AnalyzeSongFeaturesStates
  spectral_energyband_high: AnalyzeSongFeaturesStates
  spectral_energyband_low: AnalyzeSongFeaturesStates
  spectral_energyband_middle_high: AnalyzeSongFeaturesStates
  spectral_energyband_middle_low: AnalyzeSongFeaturesStates
  spectral_entropy: AnalyzeSongFeaturesStates
  spectral_flux: AnalyzeSongFeaturesStates
  spectral_kurtosis: AnalyzeSongFeaturesStates
  spectral_rms: AnalyzeSongFeaturesStates
  spectral_rolloff: AnalyzeSongFeaturesStates
  spectral_skewness: AnalyzeSongFeaturesStates
  spectral_spread: AnalyzeSongFeaturesStates
  spectral_strongpeak: AnalyzeSongFeaturesStates
  zerocrossingrate: AnalyzeSongFeaturesStates
  genre: str
  beats_count: float
  beats_loudness: AnalyzeSongFeaturesStates
  beats_loudness_band_ratio: AnalyzeSongFeaturesStatesList
  bpm: float
  bpm_histogram_first_peak_bpm: AnalyzeSongFeaturesStates
  # bpm_histogram_first_peak_spread: AnalyzeSongFeaturesStates
  bpm_histogram_first_peak_weight: AnalyzeSongFeaturesStates
  bpm_histogram_second_peak_bpm: AnalyzeSongFeaturesStates
  bpm_histogram_second_peak_spread: AnalyzeSongFeaturesStates
  bpm_histogram_second_peak_weight: AnalyzeSongFeaturesStates
  danceability: float
  onset_rate: float
  chords_changes_rate: float
  chords_key: str
  chords_number_rate: float
  chords_scale: str
  chords_strength: AnalyzeSongFeaturesStates
  hpcp: AnalyzeSongFeaturesStatesList
  hpcp_entropy: AnalyzeSongFeaturesStates
  tuning_diatonic_strength: float
  tuning_equal_tempered_deviation: float
  tuning_frequency: float
  tuning_nontempered_energy_ratio: float
