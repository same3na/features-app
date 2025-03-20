
import essentia.standard as es
from dataclasses import dataclass

from modules.songs.application.interfaces.analyze_song_api import AnalyzeSongApi
from modules.songs.domain.features import AnalyzeSongFeatures


@dataclass()
class EssentiaAnalyzer(AnalyzeSongApi):

  def analyze(self, path: str) -> AnalyzeSongFeatures:
    # use the music extractor
    extractor = es.MusicExtractor(lowlevelStats=['mean', 'stdev'], 
                               rhythmStats=['mean', 'stdev'], 
                               tonalStats=['mean', 'stdev'])
    
    features, features_frames = extractor(path)

    return AnalyzeSongFeatures(
      average_loudness=features['lowlevel.average_loudness'],
      barkbands={
        'mean': features['lowlevel.barkbands.mean']
      },
      # barkbands_crest Evaluates how peaky or dynamic the energy distribution is in a frequency band
      barkbands_crest={
        'mean': features['lowlevel.barkbands_crest.mean']
      },
      # Evaluates whether the sound is tonal (harmonic) or noise-like in character
      barkbands_flatness_db={
        'mean': features['lowlevel.barkbands_flatness_db.mean']
      },
      barkbands_kurtosis={
        'mean': features['lowlevel.barkbands_kurtosis.mean']
      },
      barkbands_skewness={
        'mean': features['lowlevel.barkbands_skewness.mean']
      },
      barkbands_spread={
        'mean': features['lowlevel.barkbands_spread.mean']
      },
      dissonance={
        'mean': features['lowlevel.dissonance.mean']
      },
      dynamic_complexity=features['lowlevel.dynamic_complexity'],
      erbbands={
        'mean': features['lowlevel.erbbands.mean']
      },
      erbbands_crest={
        'mean': features['lowlevel.erbbands_crest.mean']
      },
      erbbands_flatness_db={
        'mean': features['lowlevel.erbbands_flatness_db.mean']
      },
      erbbands_kurtosis={
        'mean': features['lowlevel.erbbands_kurtosis.mean']
      },
      erbbands_skewness={
        'mean': features['lowlevel.erbbands_skewness.mean']
      },
      erbbands_spread={
        'mean': features['lowlevel.erbbands_spread.mean']
      },
      gfcc={
        'mean': features['lowlevel.gfcc.mean']
      },
      hfc={
        'mean': features['lowlevel.hfc.mean']
      },
      melbands={
        'mean': features['lowlevel.melbands.mean']
      },
      melbands_crest={
        'mean': features['lowlevel.melbands_crest.mean']
      },
      melbands_flatness_db={
        'mean': features['lowlevel.melbands_flatness_db.mean']
      },
      melbands_kurtosis={
        'mean': features['lowlevel.melbands_kurtosis.mean']
      },
      melbands_skewness={
        'mean': features['lowlevel.melbands_skewness.mean']
      },
      melbands_spread={
        'mean': features['lowlevel.melbands_spread.mean']
      },
      mfcc={
        'mean': features['lowlevel.mfcc.mean']
      },
      pitch_salience={
        'mean': features['lowlevel.pitch_salience.mean']
      },
      silence_rate_20dB={
        'mean': features['lowlevel.silence_rate_20dB.mean']
      },
      silence_rate_30dB={
        'mean': features['lowlevel.silence_rate_30dB.mean']
      },
      silence_rate_60dB={
        'mean': features['lowlevel.silence_rate_60dB.mean']
      },
      spectral_centroid={
        'mean': features['lowlevel.spectral_centroid.mean']
      },
      spectral_complexity={
        'mean': features['lowlevel.spectral_complexity.mean']
      },
      spectral_contrast_coeffs={
        'mean': features['lowlevel.spectral_contrast_coeffs.mean']
      },
      spectral_contrast_valleys={
        'mean': features['lowlevel.spectral_contrast_valleys.mean']
      },
      spectral_decrease={
        'mean': features['lowlevel.spectral_decrease.mean']
      },
      spectral_energy={
        'mean': features['lowlevel.spectral_energy.mean']
      },
      spectral_energyband_high={
        'mean': features['lowlevel.spectral_energyband_high.mean']
      },
      spectral_energyband_low={
        'mean': features['lowlevel.spectral_energyband_low.mean']
      },
      spectral_energyband_middle_high={
        'mean': features['lowlevel.spectral_energyband_middle_high.mean']
      },
      spectral_energyband_middle_low={
        'mean': features['lowlevel.spectral_energyband_middle_low.mean']
      },
      spectral_entropy={
        'mean': features['lowlevel.spectral_entropy.mean']
      },
      spectral_flux={
        'mean': features['lowlevel.spectral_flux.mean']
      },
      spectral_kurtosis={
        'mean': features['lowlevel.spectral_kurtosis.mean']
      },
      spectral_rms={
        'mean': features['lowlevel.spectral_rms.mean']
      },
      spectral_rolloff={
        'mean': features['lowlevel.spectral_rolloff.mean']
      },
      spectral_skewness={
        'mean': features['lowlevel.spectral_skewness.mean']
      },
      spectral_spread={
        'mean': features['lowlevel.spectral_spread.mean']
      },
      spectral_strongpeak={
        'mean': features['lowlevel.spectral_strongpeak.mean']
      },
      zerocrossingrate={
        'mean': features['lowlevel.zerocrossingrate.mean']
      },
      genre='find out how to get it',
      beats_count=features['rhythm.beats_count'],
      beats_loudness={
        'mean': features['rhythm.beats_loudness.mean']
      },
      beats_loudness_band_ratio={
        'mean': features['rhythm.beats_loudness_band_ratio.mean']
      },
      bpm=features['rhythm.bpm'],
      bpm_histogram_first_peak_bpm={
        'mean': features['rhythm.bpm_histogram_first_peak_bpm']
      },
      # check why it does not have
      # bpm_histogram_first_peak_spread={
      #   'mean': features['']
      # },
      bpm_histogram_first_peak_weight={
        'mean': features['rhythm.bpm_histogram_first_peak_weight']
      },
      bpm_histogram_second_peak_bpm={
        'mean': features['rhythm.bpm_histogram_second_peak_bpm']
      },
      bpm_histogram_second_peak_spread={
        'mean': features['rhythm.bpm_histogram_second_peak_spread']
      },
      bpm_histogram_second_peak_weight={
        'mean': features['rhythm.bpm_histogram_second_peak_weight']
      },
      danceability=features['rhythm.danceability'],
      onset_rate=features['rhythm.onset_rate'],
      chords_changes_rate=features['tonal.chords_changes_rate'],
      chords_key=features['tonal.chords_key'],
      chords_number_rate=features['tonal.chords_number_rate'],
      chords_scale=features['tonal.chords_scale'],
      chords_strength={
        'mean': features['tonal.chords_strength.mean']
      },
      hpcp={
        'mean': features['tonal.hpcp.mean']
      },
      hpcp_entropy={
        'mean': features['tonal.hpcp_entropy.mean']
      },
      tuning_diatonic_strength=features['tonal.tuning_diatonic_strength'],
      tuning_equal_tempered_deviation=features['tonal.tuning_equal_tempered_deviation'],
      tuning_frequency=features['tonal.tuning_frequency'],
      tuning_nontempered_energy_ratio=features['tonal.tuning_nontempered_energy_ratio'],
    )
  
