# preprocess.py
import pandas as pd
import re
import nltk
import joblib
import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("preprocess.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("🚀 Starting preprocessing...")

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Text cleaning
stop_words = set(stopwords.words('english'))

# Load and sample dataset
try:
    df = pd.read_csv("movies.csv")
    logging.info("✅ Dataset loaded successfully. Total rows: %d", len(df))
except Exception as e:
    logging.error("❌ Failed to load dataset: %s", str(e))
    raise e

def preprocess_text(text):
    text = re.sub(r"[^a-zA-Z\s]", "", str(text))
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)


# filter the required columns for recommendation
required_columns = ["genres", "keywords", "overview", "title"]

df = df[required_columns]

df = df.dropna().reset_index(drop=True)

df['combined'] = df['genres'] + ' ' + df['keywords'] + ' ' + df['overview']

logging.info("🧹 Cleaning text...")
df['cleaned_text'] = df['combined'].apply(preprocess_text)
logging.info("✅ Text cleaned.")


# Vectorization
logging.info("🔠 Vectorizing using TF-IDF...")
tfidf = TfidfVectorizer(max_features=5000)
tfidf_matrix = tfidf.fit_transform(df['cleaned_text'])
logging.info("✅ TF-IDF matrix shape: %s", tfidf_matrix.shape)

# Cosine similarity
logging.info("📐 Calculating cosine similarity...")
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
logging.info("✅ Cosine similarity matrix generated.")

# Save everything
joblib.dump(df, 'df_cleaned.pkl')
joblib.dump(tfidf_matrix, 'tfidf_matrix.pkl')
joblib.dump(cosine_sim, 'cosine_sim.pkl')
logging.info("💾 Data saved to disk.")

logging.info("✅ Preprocessing complete.")


def recommend_movies(title, top_n=5):
    """
    Recommend movies similar to the given title.
    """
    # Find the index of the movie that matches the title
    indices = df[df['title'].str.lower() == title.lower()].index
    if len(indices) == 0:
        return f"No movie found with title '{title}'"
    idx = indices[0]

    # Get the pairwise similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]  # Exclude the movie itself

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top_n most similar movies
    return df['title'].iloc[movie_indices].tolist()

__all__ = ['df', 'recommend_movies']