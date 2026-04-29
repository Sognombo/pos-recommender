import numpy as np
import pandas as pd

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # rayon Terre en km

    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    return R * c


def find_nearest(df, user_lat, user_lon, category=None, top_n=10):
    df_copy = df.copy()

    # filtrer par catégorie si besoin
    if category:
        df_copy = df_copy[df_copy["category"] == category]

    # calcul distance
    df_copy["distance_km"] = haversine_distance(
        user_lat,
        user_lon,
        df_copy["lat"].values,
        df_copy["lon"].values
    )

    # tri
    df_sorted = df_copy.sort_values("distance_km")

    return df_sorted.head(top_n)