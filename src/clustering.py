from sklearn.cluster import KMeans

def perform_clustering(df, n_clusters=7):
    X = df[["lat", "lon"]]
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = kmeans.fit_predict(X)
    
    return df, kmeans