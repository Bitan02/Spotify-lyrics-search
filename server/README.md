# Backend Server - Spotify Lyric Search

Node.js Express backend for the Spotify Lyric Search application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file:
```env
PORT=3001
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/spotify_lyrics?retryWrites=true&w=majority
ML_SERVICE_URL=http://localhost:8000
```

3. Start the server:
```bash
npm start
# Or for development: npm run dev
```

## API Endpoints

- `POST /api/search` - Search for song by lyrics
- `GET /api/history` - Get search history
- `GET /health` - Health check

