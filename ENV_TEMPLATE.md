# Environment Variables Template

Copy these templates to create your `.env` files in each service directory.

## Backend (server/.env)

```env
PORT=3001
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/spotify_lyrics?retryWrites=true&w=majority
ML_SERVICE_URL=http://localhost:8000
```

**Getting MongoDB URI:**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free cluster
3. Create database user
4. Whitelist IP (0.0.0.0/0 for development)
5. Get connection string from "Connect" > "Connect your application"
6. Replace `<password>` with your actual password

## Frontend (client/.env)

```env
REACT_APP_API_URL=http://localhost:3001
```

**Note:** This is optional. If not set, defaults to `http://localhost:3001`

## ML Service (ml-service/.env)

```env
PORT=8000
```

**Note:** This is optional. If not set, defaults to port 8000

