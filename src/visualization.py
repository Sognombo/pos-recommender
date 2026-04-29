import folium
import os

def plot_cluster_map(df, cluster_id, save_path="../data/maps/"):
    os.makedirs(save_path, exist_ok=True)

    df_cluster = df[df["cluster"] == cluster_id]

    if df_cluster.empty:
        print(f"Aucun point pour cluster {cluster_id}")
        return None

    lat0, lon0 = df_cluster["lat"].mean(), df_cluster["lon"].mean()
    m = folium.Map(location=[lat0, lon0], zoom_start=13)

    colors = {
        "school": "blue",
        "restaurant": "red",
        "hospital": "green",
        "hotel": "purple",
        "pharmacy": "orange",
        "atm": "black"
    }

    for _, row in df_cluster.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=4,
            color=colors.get(row["category"], "gray"),
            fill=True,
            fill_opacity=0.7,
            popup=f"{row['name']} ({row['category']})"
        ).add_to(m)

    file_name = f"{save_path}cluster_{cluster_id}.html"
    m.save(file_name)

    print(f"Carte cluster {cluster_id} sauvegardée : {file_name}")

    return m