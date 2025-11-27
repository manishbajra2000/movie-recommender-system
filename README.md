# 🎬 Movie Recommender System

A **content-based movie recommendation system** built with Python and Streamlit. The app suggests similar movies based on a precomputed similarity matrix. Movie posters are fetched dynamically from **The Movie Database (TMDb) API**.

🔗 **Live Demo:**  
https://movie-recommender-manish.streamlit.app

---

## 🛠 Features

* Recommends **5 similar movies** for any selected movie.
* Fetches **posters dynamically** from TMDb.
* Uses a **precomputed similarity matrix** stored on Kaggle.
* Clean and scalable with **Streamlit caching**.
* Easy deployment on **Streamlit Cloud**.

---

## 🧩 Usage

1. Select a movie from the dropdown.
2. Click **Recommend**.
3. View **5 recommended movies** with their posters.

---

## 📂 Files

* `app.py` – Main Streamlit application.
* `movies_dict.pkl` – Movie metadata (included in repo, small file).
* `similarity.pkl` – Movie similarity matrix (downloaded from Kaggle at runtime).
* `requirements.txt` – Python dependencies.

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/manishbajra2000/movie-recommender-system.git
cd movie-recommender-system
```

### 2. Create a virtual environment and activate it

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Kaggle API credentials (for similarity matrix)

1. Go to [Kaggle → Account → API](https://www.kaggle.com/account).
2. Click **“Create New API Token”** and download `kaggle.json`.
3. In **Streamlit Cloud → Settings → Secrets**, add:

```
KAGGLE_USERNAME = "your_kaggle_username"
KAGGLE_KEY = "your_kaggle_api_key"
```

> Locally, you can also set them as environment variables:

```bash
export KAGGLE_USERNAME=your_kaggle_username
export KAGGLE_KEY=your_kaggle_api_key
```

---

### 5. Run the app

```bash
streamlit run app.py
```

* The app will automatically **download `similarity.pkl` from Kaggle** if it’s missing.
* Movie posters will be fetched from TMDb.

---

## ⚡ Notes

* Ensure **`movies_dict.pkl`** is present locally; it’s small and included in the repo.
* `similarity.pkl` is large, so it is **downloaded from Kaggle** instead of being included in the repo.
* The TMDb API key is included in the code (`API_KEY`), but you can replace it with your own for higher rate limits.

---

## 📜 License

MIT License – free to use and modify.
