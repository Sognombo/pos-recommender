# ==============================
# 📍 APPLICATION STREAMLIT (VERSION PROPRE)
# ==============================

import streamlit as st
import pandas as pd
import numpy as np
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.clustering import perform_clustering
from src.profiles import build_cluster_profiles
from src.recommendation import get_user_vector, recommend_clusters
from src.nearest_neighbors import find_nearest

import folium
from streamlit_folium import st_folium

# ==============================
# CONFIG
# ==============================

st.set_page_config(page_title="Recommandation géographique", layout="wide")

# ==============================
# STYLE SOBRE
# ==============================

st.markdown("""
<style>
h1, h2, h3 {color: #1f4e79;}
.stButton>button {
    background-color: #1f4e79;
    color: white;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# DONNÉES
# ==============================

@st.cache_data
def load_data():
    

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(BASE_DIR, "data", "pos_cotonou.csv")

    df = pd.read_csv(data_path)
    df, _ = perform_clustering(df, n_clusters=7)
    return df

df = load_data()

# ==============================
# COULEURS PAR CATÉGORIE
# ==============================

category_colors = {
    "restaurant": "red",
    "school": "blue",
    "hospital": "green",
    "hotel": "purple",
    "pharmacy": "orange",
    "atm": "black"
}

# ==============================
# HEADER
# ==============================

st.title("Système de recommandation géographique")

st.write(
    "Identifiez les zones qui correspondent à vos besoins ou trouvez les services les plus proches."
)

# ==============================
# MENU
# ==============================

menu = st.sidebar.radio(
    "Navigation",
    ["Recommandation de zones", "Services à proximité"]
)

# ==============================
# SESSION
# ==============================

if "top_clusters" not in st.session_state:
    st.session_state.top_clusters = None

if "nearest_results" not in st.session_state:
    st.session_state.nearest_results = None

# ==============================
# RECOMMANDATION
# ==============================

if menu == "Recommandation de zones":

    st.header("Choisissez vos critères")

    col1, col2, col3 = st.columns(3)

    with col1:
        restaurant = st.slider("Restaurants", 0, 5, 1)
        school = st.slider("Écoles", 0, 5, 1)

    with col2:
        hospital = st.slider("Hôpitaux", 0, 5, 1)
        hotel = st.slider("Hôtels", 0, 5, 1)

    with col3:
        pharmacy = st.slider("Pharmacies", 0, 5, 0)
        atm = st.slider("ATM", 0, 5, 0)

    user_preferences = {
        "restaurant": restaurant,
        "school": school,
        "hospital": hospital,
        "hotel": hotel,
        "pharmacy": pharmacy,
        "atm": atm
    }

    if st.button("Lancer la recherche"):

        cluster_profiles, cluster_profiles_norm = build_cluster_profiles(df)
        user_vector = get_user_vector(user_preferences, cluster_profiles.columns)

        top_clusters, _ = recommend_clusters(
            user_vector,
            cluster_profiles_norm,
            top_n=4
        )

        st.session_state.top_clusters = top_clusters

    # ==============================
    # AFFICHAGE
    # ==============================

    if st.session_state.top_clusters is not None:

        st.subheader("Zones recommandées")

        # Légende
        st.write("Couleurs des services :")
        st.write(category_colors)

        for i, cluster_id in enumerate(st.session_state.top_clusters):

            st.markdown(f"### Zone {i+1}")

            df_cluster = df[df["cluster"] == cluster_id]

            summary = df_cluster["category"].value_counts()
            st.write(summary.head(5))

            lat0, lon0 = df_cluster["lat"].mean(), df_cluster["lon"].mean()

            m = folium.Map(location=[lat0, lon0], zoom_start=13)

            for _, row in df_cluster.iterrows():
                folium.CircleMarker(
                    [row["lat"], row["lon"]],
                    radius=4,
                    color=category_colors.get(row["category"], "gray"),
                    fill=True,
                    fill_opacity=0.7,
                    popup=f"{row['name']} ({row['category']})"
                ).add_to(m)

            st_folium(m, width=700)

# ==============================
# NEAREST
# ==============================

elif menu == "Services à proximité":

    st.header("Recherche par proximité")

    col1, col2 = st.columns(2)

    with col1:
        user_lat = st.number_input("Latitude", value=6.37)

    with col2:
        user_lon = st.number_input("Longitude", value=2.43)

    category = st.selectbox(
        "Type de service",
        sorted(df["category"].unique())
    )

    if st.button("Rechercher"):

        results = find_nearest(
            df,
            user_lat,
            user_lon,
            category=category,
            top_n=10
        )

        st.session_state.nearest_results = results

    if st.session_state.nearest_results is not None:

        results = st.session_state.nearest_results

        st.subheader("Résultats")

        st.dataframe(results[["name", "category", "distance_km"]])

        m = folium.Map(location=[user_lat, user_lon], zoom_start=14)

        folium.Marker(
            [user_lat, user_lon],
            popup="Position utilisateur",
            icon=folium.Icon(color="red")
        ).add_to(m)

        for _, row in results.iterrows():
            folium.Marker(
                [row["lat"], row["lon"]],
                popup=f"{row['name']} ({row['distance_km']:.2f} km)",
                icon=folium.Icon(color=category_colors.get(row["category"], "blue"))
            ).add_to(m)

        st_folium(m, width=700)

# ==============================
# FOOTER
# ==============================

st.markdown("---")
st.write("Application de recommandation basée sur le clustering et la géolocalisation")