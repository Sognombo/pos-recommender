import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_user_vector(preferences, columns):
    return np.array([preferences.get(col, 0) for col in columns])


def recommend_clusters(user_vector, cluster_profiles_norm, top_n=4):
    similarities = cosine_similarity(
        [user_vector],
        cluster_profiles_norm
    )[0]

    top_clusters = similarities.argsort()[::-1][:top_n]
    
    return top_clusters, similarities