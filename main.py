# app.py
import json
import streamlit as st
from recommend import df, recommend_movies
from omdb_utils import get_movie_details

config = json.load(open("config.json"))

# OMDB api key
OMDB_API_KEY = config["OMDB_API_KEY"]



st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie Recommender")

# Dropdown for movie selection
movie_list = sorted(df['title'].dropna().unique())
selected_movie = st.selectbox("🎬 Select a movie:", movie_list)

if st.button("🚀 Recommend Similar Movies"):
    with st.spinner("Finding similar movies..."):
        recommendations = recommend_movies(selected_movie)
        if not recommendations or isinstance(recommendations, str):
            st.warning("Sorry, no recommendations found.")
        else:
            st.success("Top similar movies:")
            for movie_title in recommendations:
                plot, poster = get_movie_details(movie_title, OMDB_API_KEY)

                # Truncate plot to 250 characters if too long
                max_len = 250
                if plot != "N/A":
                    plot = plot.strip()
                    if len(plot) > max_len:
                        plot = plot[:max_len].rsplit(" ", 1)[0] + "..."
                else:
                    plot = "_Plot not available_"

                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if poster != "N/A":
                            st.image(poster, width=100)
                        else:
                            st.write("❌ No Poster Found")
                    with col2:
                        st.markdown(f"### {movie_title}")
                        st.markdown(f"*{plot}*")