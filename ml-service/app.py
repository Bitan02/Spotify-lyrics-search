"""
FastAPI ML Service
Exposes REST API for song identification using TF-IDF and cosine similarity.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
import pickle
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Initialize stopwords
stop_words = set(stopwords.words('english'))

# Global variables for model and data
vectorizer = None
song_data = None
tfidf_matrix = None


def preprocess_text(text):
    """
    Preprocess text: lowercase, remove punctuation/numbers, tokenize, remove stopwords.
    """
    if not text or text == '':
        return ''
    
    # Convert to lowercase
    text = str(text).lower()
    
    # Remove punctuation and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
    
    # Join back to string
    return ' '.join(tokens)


def load_model():
    """
    Load the trained TF-IDF vectorizer and song data.
    """
    global vectorizer, song_data, tfidf_matrix
    
    vectorizer_path = 'models/tfidf_vectorizer.pkl'
    data_path = 'models/song_data.pkl'
    
    if not os.path.exists(vectorizer_path) or not os.path.exists(data_path):
        raise FileNotFoundError(
            "Model files not found. Please run train_model.py first to train the model."
        )
    
    # Load vectorizer
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    
    # Load song data
    with open(data_path, 'rb') as f:
        song_data = pickle.load(f)
    
    # Pre-compute TF-IDF matrix for all songs
    lyrics_list = [song['processed_lyrics'] for song in song_data]
    tfidf_matrix = vectorizer.transform(lyrics_list)
    
    print(f"Model loaded successfully. {len(song_data)} songs available.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load model
    try:
        load_model()
    except Exception as e:
        print(f"Warning: Could not load model: {e}")
        print("Please run train_model.py first to train the model.")
    yield
    # Shutdown: Cleanup (if needed)
    pass


app = FastAPI(
    title="Spotify Lyric Search ML Service",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class LyricInput(BaseModel):
    lyrics: str


class PredictionResponse(BaseModel):
    song: str
    artist: str
    confidence: float


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "Spotify Lyric Search ML Service",
        "model_loaded": vectorizer is not None
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": vectorizer is not None,
        "songs_available": len(song_data) if song_data else 0
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(input_data: LyricInput):
    """
    Predict song and artist from lyrics snippet.
    
    Args:
        input_data: LyricInput containing lyrics text
        
    Returns:
        PredictionResponse with song, artist, and confidence score
    """
    if vectorizer is None or song_data is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please ensure the model has been trained."
        )
    
    if not input_data.lyrics or len(input_data.lyrics.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Lyrics input cannot be empty"
        )
    
    # Preprocess input lyrics
    processed_lyrics = preprocess_text(input_data.lyrics)
    
    if len(processed_lyrics.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="After preprocessing, lyrics are empty. Please provide meaningful text."
        )
    
    # Transform input to TF-IDF
    input_vector = vectorizer.transform([processed_lyrics])
    
    # Calculate cosine similarity with all songs
    similarities = cosine_similarity(input_vector, tfidf_matrix)[0]
    
    # Find the best match
    best_match_idx = np.argmax(similarities)
    confidence = float(similarities[best_match_idx])
    
    # Get song details
    best_match = song_data[best_match_idx]
    
    return PredictionResponse(
        song=best_match['song_name'],
        artist=best_match['artist'],
        confidence=round(confidence, 4)
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

