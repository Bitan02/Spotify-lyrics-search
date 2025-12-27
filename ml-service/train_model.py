"""
Model Training Script
Trains TF-IDF vectorizer on Spotify lyrics dataset and saves the model.
"""
import pandas as pd
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Initialize stopwords
stop_words = set(stopwords.words('english'))


def preprocess_text(text):
    """
    Preprocess text: lowercase, remove punctuation/numbers, tokenize, remove stopwords.
    """
    if pd.isna(text) or text == '':
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


def detect_column_mapping(df):
    """
    Automatically detect column names for lyrics, song_name, and artist.
    Returns a dictionary mapping standard names to actual column names.
    """
    column_mapping = {}
    available_cols = [col.lower() for col in df.columns]
    original_cols = {col.lower(): col for col in df.columns}
    
    # Common variations for lyrics
    lyrics_variations = ['lyrics', 'lyric', 'text', 'song_lyrics', 'lyrics_text']
    for var in lyrics_variations:
        if var in available_cols:
            column_mapping['lyrics'] = original_cols[var]
            break
    
    # Common variations for song name
    song_variations = ['song_name', 'track_name', 'name', 'title', 'song', 'track', 
                       'track_name', 'song_title']
    for var in song_variations:
        if var in available_cols:
            column_mapping['song_name'] = original_cols[var]
            break
    
    # Common variations for artist
    artist_variations = ['artist', 'artist_name', 'artists', 'artist_name(s)', 
                        'artist_names', 'artist(s)']
    for var in artist_variations:
        if var in available_cols:
            column_mapping['artist'] = original_cols[var]
            break
    
    return column_mapping


def load_and_prepare_data(csv_path='data/spotify_songs.csv'):
    """
    Load dataset and prepare it for training.
    Creates a sample dataset if file doesn't exist.
    """
    try:
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} songs from dataset")
        print(f"Available columns: {list(df.columns)}")
    except FileNotFoundError:
        print(f"Dataset not found at {csv_path}. Creating sample dataset...")
        df = create_sample_dataset()
        df.to_csv(csv_path, index=False)
        print(f"Created sample dataset with {len(df)} songs")
    
    # Auto-detect column mapping
    column_mapping = detect_column_mapping(df)
    
    # Check if all required columns were found
    required_cols = ['lyrics', 'song_name', 'artist']
    missing_cols = [col for col in required_cols if col not in column_mapping]
    
    if missing_cols:
        print(f"\n❌ Error: Could not detect the following required columns:")
        for col in missing_cols:
            print(f"   - {col}")
        print(f"\nAvailable columns in your dataset:")
        for col in df.columns:
            print(f"   - {col}")
        print(f"\nPlease ensure your dataset has columns for:")
        print(f"   - Lyrics (text): lyrics, lyric, text, song_lyrics")
        print(f"   - Song name: song_name, track_name, name, title, song, track")
        print(f"   - Artist: artist, artist_name, artists")
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Rename columns to standard names for easier processing
    df_processed = df.copy()
    df_processed['lyrics'] = df_processed[column_mapping['lyrics']]
    df_processed['song_name'] = df_processed[column_mapping['song_name']]
    df_processed['artist'] = df_processed[column_mapping['artist']]
    
    print(f"\n✅ Column mapping detected:")
    print(f"   Lyrics: '{column_mapping['lyrics']}'")
    print(f"   Song Name: '{column_mapping['song_name']}'")
    print(f"   Artist: '{column_mapping['artist']}'")
    
    # Preprocess lyrics
    print("\nPreprocessing lyrics...")
    df_processed['processed_lyrics'] = df_processed['lyrics'].apply(preprocess_text)
    
    # Remove rows with empty processed lyrics
    initial_count = len(df_processed)
    df_processed = df_processed[df_processed['processed_lyrics'].str.len() > 0]
    removed_count = initial_count - len(df_processed)
    
    if removed_count > 0:
        print(f"Removed {removed_count} rows with empty lyrics after preprocessing")
    
    print(f"Final dataset size: {len(df_processed)} songs")
    return df_processed


def create_sample_dataset():
    """
    Creates a sample dataset with popular songs for testing.
    """
    sample_data = [
        {
            'song_name': 'Blinding Lights',
            'artist': 'The Weeknd',
            'lyrics': 'I been tryna call I been on my own for long enough Maybe you can show me how to love maybe'
        },
        {
            'song_name': 'Shape of You',
            'artist': 'Ed Sheeran',
            'lyrics': 'The club isnt the best place to find a lover So the bar is where I go Me and my friends at the table doing shots'
        },
        {
            'song_name': 'Someone Like You',
            'artist': 'Adele',
            'lyrics': 'I heard that you settled down That you found a girl and youre married now I heard that your dreams came true'
        },
        {
            'song_name': 'Bohemian Rhapsody',
            'artist': 'Queen',
            'lyrics': 'Is this the real life Is this just fantasy Caught in a landslide No escape from reality'
        },
        {
            'song_name': 'Hotel California',
            'artist': 'Eagles',
            'lyrics': 'On a dark desert highway cool wind in my hair Warm smell of colitas rising up through the air'
        },
        {
            'song_name': 'Stairway to Heaven',
            'artist': 'Led Zeppelin',
            'lyrics': 'Theres a lady whos sure all that glitters is gold And shes buying a stairway to heaven'
        },
        {
            'song_name': 'Billie Jean',
            'artist': 'Michael Jackson',
            'lyrics': 'She was more like a beauty queen from a movie scene I said dont mind but what do you mean I am the one'
        },
        {
            'song_name': 'Sweet Child O Mine',
            'artist': "Guns N' Roses",
            'lyrics': 'She has a smile that it seems to me Reminds me of childhood memories Where everything was as fresh as the bright blue sky'
        },
        {
            'song_name': 'Imagine',
            'artist': 'John Lennon',
            'lyrics': 'Imagine theres no heaven Its easy if you try No hell below us Above us only sky'
        },
        {
            'song_name': 'Like a Rolling Stone',
            'artist': 'Bob Dylan',
            'lyrics': 'Once upon a time you dressed so fine You threw the bums a dime in your prime didnt you'
        }
    ]
    
    # Expand to 50+ entries by creating variations
    expanded_data = []
    for i in range(5):  # Create 5 variations of each
        for song in sample_data:
            expanded_data.append(song.copy())
    
    return pd.DataFrame(expanded_data)


def train_model(df):
    """
    Train TF-IDF vectorizer on the dataset.
    """
    print("Training TF-IDF vectorizer...")
    
    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),  # Unigrams and bigrams
        min_df=2,
        max_df=0.95
    )
    
    # Fit and transform
    tfidf_matrix = vectorizer.fit_transform(df['processed_lyrics'])
    
    print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")
    
    return vectorizer, tfidf_matrix, df


def save_model(vectorizer, df, vectorizer_path='models/tfidf_vectorizer.pkl', 
               data_path='models/song_data.pkl'):
    """
    Save the trained model and song data.
    """
    import os
    os.makedirs('models', exist_ok=True)
    
    # Save vectorizer
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    print(f"Saved vectorizer to {vectorizer_path}")
    
    # Save song data (for lookup)
    song_data = df[['song_name', 'artist', 'processed_lyrics']].to_dict('records')
    with open(data_path, 'wb') as f:
        pickle.dump(song_data, f)
    print(f"Saved song data to {data_path}")


if __name__ == '__main__':
    print("=" * 50)
    print("Spotify Lyric Search - Model Training")
    print("=" * 50)
    
    # Load and prepare data
    df = load_and_prepare_data()
    
    # Train model
    vectorizer, tfidf_matrix, df = train_model(df)
    
    # Save model
    save_model(vectorizer, df)
    
    print("\n" + "=" * 50)
    print("Model training completed successfully!")
    print("=" * 50)

