import streamlit as st
import pickle
import numpy as np
import pandas as pd
import requests
import os
import subprocess
from io import BytesIO

st.set_page_config(page_title="Movie Recommender", layout="wide")

FILE_ID = "1byW4HCXhgdXrMEtoYUd3FfW0VN4jkLYX"  # Replace with your file ID
SIMILARITY_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"  # Replace with your file ID
SIMILARITY_FILE = "similarity.pkl"

# Download file if not present
def download_similarity():
    if not os.path.exists(SIMILARITY_FILE):
        st.info("Downloading similarity.pkl from Google Drive...")
        response = requests.get(SIMILARITY_URL)
        with open(SIMILARITY_FILE, "wb") as f:
            f.write(response.content)
        st.success("similarity.pkl downloaded!")

download_similarity()

# Load similarity.pkl
@st.cache_data
def load_similarity():
    with open(SIMILARITY_FILE, "rb") as f:
        return pickle.load(f)

similarity = load_similarity()


# Load movies and similarity matrix
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

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




# import os
# import pickle
# import pandas as pd
# import numpy as np
# import requests
# from io import BytesIO
# import streamlit as st
# import subprocess

# st.set_page_config(page_title="Movie Recommender", layout="wide")

# # --- STEP 1: Set Kaggle credentials from Streamlit secrets ---
# os.environ["KAGGLE_USERNAME"] = st.secrets["KAGGLE_USERNAME"]
# os.environ["KAGGLE_KEY"] = st.secrets["KAGGLE_KEY"]

# # --- STEP 2: Download files from Kaggle if not present ---
# DATASET = "<username>/<dataset-name>"  # Replace with your Kaggle dataset

# def download_from_kaggle():
#     files_needed = [
#         "movies.pkl",
#         "movies_dict.pkl",
#         "similarity.pkl",
#         "tmdb_5000_movies.csv",
#         "tmdb_5000_credits.csv"
#     ]
#     missing_files = [f for f in files_needed if not os.path.exists(f)]
#     if missing_files:
#         st.info("Downloading dataset from Kaggle…")
#         subprocess.run([
#             "kaggle", "datasets", "download",
#             "-d", DATASET,
#             "--unzip"
#         ], check=True)
#         st.success("Dataset downloaded!")

# download_from_kaggle()

# # --- STEP 3: Load data ---
# @st.cache_data
# def load_pickle(filename):
#     with open(filename, "rb") as f:
#         return pickle.load(f)

# @st.cache_data
# def load_csv(filename):
#     return pd.read_csv(filename)

# movies_dict = load_pickle("movies_dict.pkl")
# similarity = load_pickle("similarity.pkl")
# movies = pd.DataFrame(movies_dict)
# tmdb = load_csv("tmdb_5000_movies.csv")

# # --- STEP 4: Movie recommender logic ---
# def fetch_poster(movie_id):
#     tmdb_api_key = "<your_tmdb_api_key>"  # Optional, only if fetching posters dynamically
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}&language=en-US"
#     data = requests.get(url).json()
#     return "https://image.tmdb.org/t/p/w500/" + data.get("poster_path", "")

# def recommend(movie):
#     if movie not in movies['title'].values:
#         st.warning("Movie not found!")
#         return [], []
#     idx = np.where(movies['title'] == movie)[0][0]
#     distances = similarity[idx]
#     movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
#     recommended = []
#     posters = []
#     for i in movies_list:
#         recommended.append(movies.iloc[i[0]].title)
#         try:
#             posters.append(fetch_poster(movies.iloc[i[0]].id))
#         except:
#             posters.append("")
#     return recommended, posters

# # --- STEP 5: Streamlit UI ---
# st.title("🎬 Movie Recommender System")
# selected_movie = st.selectbox("Select a movie", movies['title'].values)

# if st.button("Recommend"):
#     names, posters = recommend(selected_movie)
#     cols = st.columns(5)
#     for col, name, poster in zip(cols, names, posters):
#         col.text(name)
#         if poster:
#             col.image(poster)