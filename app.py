import streamlit as st
import pickle
import numpy as np
import pandas as pd
import requests
import os
import subprocess
from io import BytesIO

st.set_page_config(page_title="Movie Recommender", layout="wide")

# SIMILARITY_URL = "https://drive.google.com/uc?export=download&id=1byW4HCXhgdXrMEtoYUd3FfW0VN4jkLYX"
KAGGLE_DATASET = "manishhbajracharya/movie-recommender-similarity-matrix"  
SIMILARITY_FILE = "similarity.pkl"

# Set Kaggle credentials from Streamlit secrets
os.environ["KAGGLE_USERNAME"] = st.secrets["KAGGLE_USERNAME"]
os.environ["KAGGLE_KEY"] = st.secrets["KAGGLE_KEY"]


def download_similarity():
    if not os.path.exists(SIMILARITY_FILE):
        # st.info("Downloading similarity.pkl from Google Drive...")
        # response = requests.get(SIMILARITY_URL)
        # with open(SIMILARITY_FILE, "wb") as f:
        #     f.write(response.content)
        st.info("Downloading similarity.pkl from Kaggle...")
        subprocess.run([
            "kaggle", "datasets", "download",
            "-d", KAGGLE_DATASET,
            "--unzip"
        ], check=True)
        st.success("similarity.pkl downloaded!")

download_similarity()

# Load the pickle safely with caching
@st.cache_data
def load_similarity():
    with open(SIMILARITY_FILE, "rb") as f:
        return pickle.load(f)

similarity = load_similarity()


# Load movies and similarity matrix
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)


API_KEY = "07f2044c612900790e93e23856f3246e"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    data = requests.get(url).json()

    poster_path = data['poster_path']

    full_path = "https://image.tmdb.org/t/p/original/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), key=lambda x:x[1], reverse=True)[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        id = movies.iloc[i[0]].movie_id
        
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        poster = fetch_poster(id)
        recommended_posters.append(poster)

    return recommended_movies, recommended_posters

st.title("Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Choose a Movie:",
    movies['title'].values
)

if st.button("Recommend"):
    st.write(f"You selected: {selected_movie_name}")
    names, posters = recommend(selected_movie_name)
    st.write(f"Recommendations: ")
    # for movie in names:
    #     st.write(movie)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:          
        st.text(names[2])
        st.image(posters[2])
    with col4:          
        st.text(names[3])
        st.image(posters[3])
    with col5:          
        st.text(names[4])
        st.image(posters[4])



st.write("Developed by Manish Harsha Bajracharya")