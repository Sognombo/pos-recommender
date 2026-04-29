import pandas as pd
from sklearn.preprocessing import normalize

def build_cluster_profiles(df):
    cluster_profiles = pd.crosstab(df["cluster"], df["category"])
    
    cluster_profiles_norm = pd.DataFrame(
        normalize(cluster_profiles, norm='l2'),
        index=cluster_profiles.index,
        columns=cluster_profiles.columns
    )
    
    return cluster_profiles, cluster_profiles_norm