from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.cluster import KMeans



@dataclass
class FeatureClusteringCmd:
  features_df: pd.DataFrame

class FeatureClusteringCmdHandler:
  
  def handle(self, command: FeatureClusteringCmd) -> tuple[list[int], pd.DataFrame]:

    df_init = command.features_df.copy()

    if command.features_df.empty:
      raise ValueError("Input DataFrame is empty.")
        
    genre_labels = [
      "60s","70s","80s","90s","acidjazz","alternative","alternativerock","ambient","atmospheric",
      "blues","bluesrock","bossanova","breakbeat","celtic","chanson","chillout","choir","classical",
      "classicrock","club","contemporary","country","dance","darkambient","darkwave","deephouse",
      "disco","downtempo","drumnbass","dub","dubstep","easylistening","edm","electronic",
      "electronica","electropop","ethno","eurodance","experimental","folk","funk","fusion",
      "groove","grunge","hard","hardrock","hiphop","house","idm","improvisation","indie",
      "industrial","instrumentalpop","instrumentalrock","jazz","jazzfusion","latin","lounge",
      "medieval","metal","minimal","newage","newwave","orchestral","pop","popfolk","poprock",
      "postrock","progressive","psychedelic","punkrock","rap","reggae","rnb","rock","rocknroll",
      "singersongwriter","soul","soundtrack","swing","symphonic","synthpop","techno","trance",
      "triphop","world","worldfusion"
    ]

    mood_labels = [
      "action","adventure","advertising","background","ballad","calm","children","christmas",
      "commercial","cool","corporate","dark","deep","documentary","drama","dramatic","dream",
      "emotional","energetic","epic","fast","film","fun","funny","game","groovy","happy","heavy",
      "holiday","hopeful","inspiring","love","meditative","melancholic","melodic","motivational",
      "movie","nature","party","positive","powerful","relaxing","retro","romantic","sad","sexy",
      "slow","soft","soundscape","space","sport","summer","trailer","travel","upbeat","uplifting"
    ]
  
    def expand_json_column(data, all_labels):
      result = dict.fromkeys(all_labels, 0)  # Default 0 for all
      for item in data:
        name = item["name"]
        val = item["value"]
        if name in result:
          result[name] = val

      return pd.Series(result)

    genre_df = df_init["genre"].apply(lambda x: expand_json_column(x, genre_labels))
    mood_df = df_init["mood"].apply(lambda x: expand_json_column(x, mood_labels))


    # Normalize genre values per song
    # genre_df_normalized = genre_df.div(genre_df.sum(axis=1), axis=0)
    genre_df_normalized = genre_df.div(100)

    # Normalize mood values per song
    # mood_df_normalized = mood_df.div(mood_df.sum(axis=1), axis=0)
    mood_df_normalized = mood_df.div(100)

    feature_cols = ['aggressive', 'happy', 'sad', 'relaxed', 'engagement']
    scaler = StandardScaler()
    df_init[feature_cols] = scaler.fit_transform(df_init[feature_cols])

    df_final = pd.concat([df_init.drop(columns=["genre", "mood"]), genre_df_normalized, mood_df_normalized], axis=1)

    #################
    # Remove low-variance features
    selector = VarianceThreshold(threshold=0.01)  # Remove low-variance features
    data_variance = selector.fit_transform(df_final)

    # Get mask of selected features
    mask = selector.get_support()
    # Get removed features
    removed_features = df_final.columns[~mask]
    ok_features = df_final.columns[mask]

    selected_features = np.array(ok_features)
    data_variance_df = pd.DataFrame(data_variance, columns=selected_features)


    # clustering
    k = 3  # for now static
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data_variance_df)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_  # shape: (n_clusters, n_features)
    centers_df = pd.DataFrame(centers, columns=data_variance_df.columns)  # exclude 'cluster' col

    cluster_tag = []
    for idx, row in centers_df.iterrows():
        # Get top 3 features by value for this cluster center
        top_features = row.nlargest(3).index.tolist()
        # Join them into a string
        cluster_tag.append(", ".join(top_features))

    return labels, centers_df, cluster_tag