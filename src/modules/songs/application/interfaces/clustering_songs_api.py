from abc import ABC, abstractmethod
from dataclasses import dataclass
import pandas as pd

@dataclass()
class ClusteringSongsApi(ABC):

  @abstractmethod
  def cluster_songs(self, features_df: pd.DataFrame) -> list[str]:
    """Cluster songs based on their features and return the cluster ids."""