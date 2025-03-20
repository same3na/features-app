from dataclasses import field
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modules.songs.application.queries.filter_songs_qry import ClassificationFilters, FilterSongsCmd, FilterSongsHandler, SongsFilter
from modules.songs.application.queries.get_song_features_qry import GetSongFeaturesCommand, GetSongFeaturesQueryHandler
from modules.songs.infrastructure.essentia_features.essentia_extract_features import EssentiaExtractFeatures
from modules.songs.infrastructure.sqlalchemy.song_repo import SQLAlchemySongRepository

app = FastAPI()

# Allowed origins (Frontend URLs)
origins = [
    "http://localhost:5173",  # React local dev server
    "http://localhost:8000",  # React local dev server

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
        headers={"Access-Control-Allow-Origin": "*"},  # Ensure CORS headers are applied
    )

DATABASE_URL = "postgresql://root:test@localhost:5434/test"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

song_repo = SQLAlchemySongRepository(session=session)
feature_api = EssentiaExtractFeatures()
song_features_query = GetSongFeaturesQueryHandler(extract_song_features=feature_api, song_repo=song_repo)
filter_songs_qry = FilterSongsHandler(song_repo=song_repo)

@app.get("/features/{item_id}")
def read_item(item_id: str, q: str = None):
  result = song_features_query.handle(GetSongFeaturesCommand(id=item_id))
  return result

class SongsFilterRequest(BaseModel):
    feature: str
    operation: str
    value: str

class ClassificationRequest(BaseModel):
    weight: int
    filters: list[SongsFilterRequest]

class FilterPostRequest(BaseModel):
    is_all: bool = False
    song_ids: list = field(default_factory=list)
    filters: list[ClassificationRequest] = field(default_factory=list)
    playlist_max_nb:int = 50

@app.post("/filter-songs-by-criterias")
def filter_item(item: FilterPostRequest):
  try:
    filters = [ClassificationFilters(weight=item.weight, filters=[SongsFilter(feature=filter_item.feature, operation=filter_item.operation, value=filter_item.value) for filter_item in item.filters]) for item in item.filters] 
    result = filter_songs_qry.handle(FilterSongsCmd(is_all=item.is_all, song_ids=item.song_ids, filters=filters, total_songs=item.playlist_max_nb))
    return result
  except Exception as e:
    print(str(e))
    raise HTTPException(status_code=400, detail=str(e))
