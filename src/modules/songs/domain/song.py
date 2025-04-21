from dataclasses import dataclass, field
from datetime import datetime
import logging
import os
import uuid

import numpy as np
from pydantic import BaseModel


from modules.songs.domain.features import AnalyzeSongFeatures

class SongJsonFeatures(BaseModel):
  name: str
  value: int

@dataclass()
class Song():
  id: uuid.UUID
  # features: AnalyzeSongFeatures | None = None
  genre: list[SongJsonFeatures] | None = None
  mood: list[SongJsonFeatures] | None = None
  aggressive: int | None = None
  happy: int | None = None
  sad: int | None = None
  relaxed: int | None = None
  engagement: int | None = None
  
  
@dataclass()
class SongData():
  id: uuid.UUID
  data: AnalyzeSongFeatures | None = None