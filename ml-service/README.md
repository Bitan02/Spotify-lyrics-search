# ML Service - Spotify Lyric Search

Python FastAPI service for song identification using TF-IDF and cosine similarity.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Train the model:
```bash
python train_model.py
```

3. Run the service:
```bash
python app.py
# Or: uvicorn app:app --host 0.0.0.0 --port 8000
```

## Dataset

Place your Spotify dataset CSV at `data/spotify_songs.csv` with columns:
- `lyrics`: Song lyrics text
- `song_name`: Song title
- `artist`: Artist name

If no dataset is found, the training script will create a sample dataset.

## API Endpoints

- `POST /predict` - Predict song from lyrics
- `GET /health` - Health check
- `GET /` - Service info

