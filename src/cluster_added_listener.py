

import json

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from modules.common.infrastructure.redis_pub_sub import RedisPubSub
from modules.common.infrastructure.redis_streaming import RedisStreaming
from modules.songs.application.commands.apply_clustering_cmd import ApplyClustering, ApplyClusteringHandler
from modules.songs.infrastructure.sqlalchemy.song_repo import SQLAlchemySongRepository

DATABASE_URL = "postgresql://root:test@localhost:5434/test"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def main():
  # database connection
  repo = SQLAlchemySongRepository(session=session)

  # redis
  redis = RedisStreaming(redis_host="localhost", redis_port=6379, redis_db=0)

  redis_pub_sub = RedisPubSub(redis_host="localhost", redis_port=6379, redis_db=0)
  redis_pub_sub.subscribe("ClusterAdded")

  try:
    for message in redis_pub_sub.listen("ClusterAdded"):
      if message['type'] == 'message':
        # data = message['data']
        print(f"Received message: {message['data'].decode('utf-8')}")
        data = message['data'].decode('utf-8')

        data = json.loads(data)
        data = data['Data']
        
        # create the command and trigger it
        command = ApplyClusteringHandler(repo, redis)
        command.handle(ApplyClustering(cluster_id=data["cluster_id"], nb_of_clusters=data["clusters_nb"], ids=data["song_ids"]))


  except KeyboardInterrupt:
    print("Subscriber stopped.")


if __name__ == "__main__":
  main()