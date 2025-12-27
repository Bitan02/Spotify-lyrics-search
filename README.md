# 🎵 Spotify Lyric Search – Song & Artist Identification System

A complete full-stack web application that identifies songs and artists from lyric snippets using Machine Learning (TF-IDF and Cosine Similarity).

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [How It Works](#how-it-works)
- [Accuracy & Performance](#accuracy--performance)

## ✨ Features

- **Lyric Search**: Enter a snippet of lyrics to find the song and artist
- **ML-Powered**: Uses TF-IDF vectorization and cosine similarity for matching
- **Search History**: All searches are saved to MongoDB for future reference
- **Confidence Scores**: Get confidence percentages for match quality
- **Modern UI**: Beautiful, responsive design with Tailwind CSS
- **RESTful APIs**: Clean API architecture with proper error handling

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI framework
- **React Router** - Navigation
- **Tailwind CSS** - Styling
- **Axios** - HTTP client

### Backend
- **Node.js** - Runtime
- **Express** - Web framework
- **MongoDB** - Database (MongoDB Atlas)
- **Mongoose** - ODM

### ML Service
- **Python 3.8+** - Language
- **FastAPI** - API framework
- **scikit-learn** - Machine learning
- **NLTK** - Natural language processing
- **TF-IDF** - Feature extraction
- **Cosine Similarity** - Similarity matching

## 📁 Project Structure

```
spotify-lyrics-search/
├── client/                 # React frontend
│   ├── public/
│   ├── src/
│   │   ├── pages/         # Page components
│   │   ├── services/       # API service
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
│
├── server/                 # Node.js backend
│   ├── models/            # MongoDB schemas
│   ├── routes/            # API routes
│   ├── server.js          # Main server file
│   └── package.json
│
├── ml-service/            # Python ML service
│   ├── models/           # Saved models (generated)
│   ├── data/             # Dataset (optional)
│   ├── app.py            # FastAPI application
│   ├── train_model.py    # Model training script
│   └── requirements.txt
│
└── README.md
```

## 🚀 Setup Instructions

### Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **MongoDB Atlas** account (free tier works)
- **npm** or **yarn**

### Step 1: Clone and Navigate

```bash
cd spotify-lyrics-search
```

### Step 2: Setup ML Service

```bash
cd ml-service

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train the model (this will create sample data if dataset not found)
python train_model.py

# The model files will be saved in ml-service/models/
```

**Note**: If you have a Spotify dataset CSV file, place it at `ml-service/data/spotify_songs.csv` with columns: `lyrics`, `song_name`, `artist`. Otherwise, the script will create a sample dataset.

### Step 3: Setup Backend Server

```bash
cd ../server

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Edit .env and add your MongoDB Atlas connection string:
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/spotify_lyrics?retryWrites=true&w=majority
# PORT=3001
# ML_SERVICE_URL=http://localhost:8000
```

**Getting MongoDB Atlas URI:**
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create a database user
4. Whitelist your IP (or use 0.0.0.0/0 for development)
5. Get connection string and replace `<password>` with your password

### Step 4: Setup Frontend

```bash
cd ../client

# Install dependencies
npm install

# Create .env file (optional, defaults to http://localhost:3001)
# REACT_APP_API_URL=http://localhost:3001
```

### Step 5: Run the Application

You need to run all three services:

#### Terminal 1: ML Service
```bash
cd ml-service
python app.py
# Or: uvicorn app:app --host 0.0.0.0 --port 8000
```
ML Service runs on: **http://localhost:8000**

#### Terminal 2: Backend Server
```bash
cd server
npm start
# Or for development: npm run dev
```
Backend runs on: **http://localhost:3001**

#### Terminal 3: Frontend
```bash
cd client
npm start
```
Frontend runs on: **http://localhost:3000**

### Step 6: Access the Application

Open your browser and navigate to: **http://localhost:3000**

## 📡 API Documentation

### Backend APIs

#### POST `/api/search`
Search for a song by lyrics.

**Request:**
```json
{
  "lyrics": "I been tryna call I been on my own"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "song": "Blinding Lights",
    "artist": "The Weeknd",
    "confidence": 0.8542,
    "id": "507f1f77bcf86cd799439011"
  }
}
```

#### GET `/api/history`
Get search history with pagination.

**Query Parameters:**
- `page` (optional, default: 1) - Page number
- `limit` (optional, default: 20) - Items per page (max: 100)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "lyrics": "I been tryna call",
      "song": "Blinding Lights",
      "artist": "The Weeknd",
      "confidence": 0.8542,
      "createdAt": "2024-01-15T10:30:00.000Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "pages": 3
  }
}
```

### ML Service APIs

#### POST `/predict`
Predict song from lyrics (called by backend).

**Request:**
```json
{
  "lyrics": "I been tryna call I been on my own"
}
```

**Response:**
```json
{
  "song": "Blinding Lights",
  "artist": "The Weeknd",
  "confidence": 0.8542
}
```

#### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "songs_available": 50
}
```

## 🧠 How It Works

### Machine Learning Pipeline

1. **Text Preprocessing**:
   - Convert to lowercase
   - Remove punctuation and numbers
   - Tokenize words
   - Remove stopwords (common words like "the", "is", etc.)

2. **Feature Extraction**:
   - **TF-IDF (Term Frequency-Inverse Document Frequency)**: Converts text into numerical vectors
   - Captures word importance relative to the entire dataset
   - Uses unigrams and bigrams (single words and word pairs)

3. **Similarity Matching**:
   - **Cosine Similarity**: Measures the angle between two vectors
   - Higher similarity = better match
   - Returns the song with the highest similarity score

### System Flow

```
User Input (Lyrics)
    ↓
Frontend (React)
    ↓
Backend API (Express)
    ↓
ML Service (FastAPI)
    ↓
TF-IDF Vectorization
    ↓
Cosine Similarity Search
    ↓
Return: Song, Artist, Confidence
    ↓
Save to MongoDB
    ↓
Return to Frontend
```

## 📊 Accuracy & Performance

### Accuracy Factors

1. **Dataset Size**: Larger datasets improve accuracy
2. **Lyric Length**: Longer snippets (10+ words) yield better results
3. **Unique Phrases**: Distinctive lyrics match better than common phrases
4. **Preprocessing Quality**: Stopword removal and normalization help

### Performance

- **Model Training**: ~30 seconds for 50 songs, scales linearly
- **Prediction Time**: <100ms per search
- **API Response**: <200ms end-to-end (including database save)

### Improving Accuracy

1. **Use a larger dataset**: The more songs, the better
2. **Fine-tune TF-IDF parameters**: Adjust `max_features`, `ngram_range`
3. **Add more preprocessing**: Stemming, lemmatization
4. **Try different models**: Word2Vec, BERT embeddings for better semantic understanding

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```env
PORT=3001
MONGODB_URI=mongodb+srv://...
ML_SERVICE_URL=http://localhost:8000
```

**Frontend (.env):**
```env
REACT_APP_API_URL=http://localhost:3001
```

**ML Service (.env):**
```env
PORT=8000
```

## 🐛 Troubleshooting

### ML Service Issues

- **Model not found**: Run `python train_model.py` first
- **NLTK data missing**: The script auto-downloads, but you can manually run:
  ```python
  import nltk
  nltk.download('punkt')
  nltk.download('stopwords')
  ```

### Backend Issues

- **MongoDB connection failed**: Check your `MONGODB_URI` and network whitelist
- **ML service unreachable**: Ensure ML service is running on port 8000

### Frontend Issues

- **API calls failing**: Check `REACT_APP_API_URL` matches backend port
- **CORS errors**: Backend CORS is configured for all origins (adjust for production)

## 📝 Sample API Requests

### Using cURL

**Search:**
```bash
curl -X POST http://localhost:3001/api/search \
  -H "Content-Type: application/json" \
  -d '{"lyrics": "I been tryna call I been on my own"}'
```

**History:**
```bash
curl http://localhost:3001/api/history?page=1&limit=10
```

### Using Postman

1. Import the endpoints
2. Set headers: `Content-Type: application/json`
3. For POST requests, use JSON body

## 🚢 Production Deployment

### Recommendations

1. **Environment Variables**: Use secure secret management
2. **CORS**: Restrict origins in production
3. **Error Handling**: Add logging (Winston, Pino)
4. **Rate Limiting**: Add rate limits to APIs
5. **HTTPS**: Use SSL/TLS certificates
6. **Database Indexing**: Already implemented for common queries
7. **Model Optimization**: Consider model compression for faster loading

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue on the repository.

---

**Built with ❤️ using React, Node.js, Python, and Machine Learning**

