# Deployment Guide - Spotify Lyric Search

## 🚨 Common Issues & Solutions

### 404 Error During Deployment

If you're seeing a **404: NOT_FOUND** error, it means the frontend cannot reach the backend API. Here's how to fix it:

## ✅ Pre-Deployment Checklist

### 1. **Start All Services**

You need **3 services running simultaneously**:

#### Terminal 1: ML Service (Python)
```bash
cd ml-service
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Train model (if not already done)
python train_model.py

# Start ML service
python app.py
```
**Should be running on:** http://localhost:8000

#### Terminal 2: Backend Server (Node.js)
```bash
cd server
npm install  # If not already done

# Create .env file with:
# PORT=3001
# MONGODB_URI=your_mongodb_connection_string
# ML_SERVICE_URL=http://localhost:8000

npm start
```
**Should be running on:** http://localhost:3001

#### Terminal 3: Frontend (React)
```bash
cd client
npm install  # If not already done
npm start
```
**Should be running on:** http://localhost:3000

### 2. **Verify Services Are Running**

Test each service:

**ML Service:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","model_loaded":true,...}
```

**Backend:**
```bash
curl http://localhost:3001/health
# Should return: {"status":"ok","service":"Spotify Lyric Search Backend",...}
```

**Frontend:**
- Open http://localhost:3000 in browser
- Should show the search page

### 3. **Check Environment Variables**

#### Backend (`server/.env`):
```env
PORT=3001
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/spotify_lyrics?retryWrites=true&w=majority
ML_SERVICE_URL=http://localhost:8000
```

#### Frontend (`client/.env` - Optional):
```env
REACT_APP_API_URL=http://localhost:3001
```

**Note:** In development, the frontend uses a proxy (configured in `package.json`), so you don't need to set `REACT_APP_API_URL` unless deploying to production.

## 🔧 Troubleshooting 404 Errors

### Issue 1: Backend Not Running
**Symptom:** 404 error when trying to search

**Solution:**
1. Check if backend is running: `curl http://localhost:3001/health`
2. If not running, start it: `cd server && npm start`
3. Check for errors in the backend terminal

### Issue 2: ML Service Not Running
**Symptom:** Backend returns 503 or "ML service unavailable"

**Solution:**
1. Check if ML service is running: `curl http://localhost:8000/health`
2. If not running, start it: `cd ml-service && python app.py`
3. Ensure model is trained: `python train_model.py`

### Issue 3: MongoDB Connection Failed
**Symptom:** Backend crashes or shows MongoDB connection error

**Solution:**
1. Verify `MONGODB_URI` in `server/.env` is correct
2. Check MongoDB Atlas network whitelist (add your IP or 0.0.0.0/0 for development)
3. Verify database user credentials

### Issue 4: CORS Errors
**Symptom:** Browser console shows CORS errors

**Solution:**
- Backend already has CORS enabled for all origins
- If issues persist, check `server/server.js` CORS configuration

### Issue 5: Model Not Found
**Symptom:** ML service returns "Model not loaded"

**Solution:**
```bash
cd ml-service
python train_model.py
# This creates models/tfidf_vectorizer.pkl and models/song_data.pkl
```

## 🌐 Production Deployment

### Frontend Build
```bash
cd client
npm run build
# Creates optimized build in client/build/
```

### Environment Variables for Production

**Frontend:**
```env
REACT_APP_API_URL=https://your-backend-domain.com
```

**Backend:**
```env
PORT=3001
MONGODB_URI=your_production_mongodb_uri
ML_SERVICE_URL=http://localhost:8000  # Or your ML service URL
```

### Deployment Options

1. **Vercel/Netlify** (Frontend)
   - Connect GitHub repo
   - Set `REACT_APP_API_URL` environment variable
   - Deploy

2. **Heroku/Railway** (Backend)
   - Connect GitHub repo
   - Set environment variables
   - Deploy

3. **Docker** (All Services)
   - Create Dockerfiles for each service
   - Use docker-compose for orchestration

## 📝 Quick Start Script

Create a `start-all.sh` (or `start-all.bat` for Windows) to start all services:

**Windows (`start-all.bat`):**
```batch
@echo off
start "ML Service" cmd /k "cd ml-service && venv\Scripts\activate && python app.py"
timeout /t 3
start "Backend" cmd /k "cd server && npm start"
timeout /t 3
start "Frontend" cmd /k "cd client && npm start"
```

**macOS/Linux (`start-all.sh`):**
```bash
#!/bin/bash
cd ml-service && source venv/bin/activate && python app.py &
sleep 3
cd ../server && npm start &
sleep 3
cd ../client && npm start
```

## ✅ Verification Steps

1. ✅ ML Service responds at http://localhost:8000/health
2. ✅ Backend responds at http://localhost:3001/health
3. ✅ Frontend loads at http://localhost:3000
4. ✅ Can search for songs without 404 errors
5. ✅ Results display correctly

## 🆘 Still Having Issues?

1. **Check all terminals** for error messages
2. **Verify ports** are not in use by other applications
3. **Check firewall** settings
4. **Review logs** in each service terminal
5. **Test API endpoints** directly with curl/Postman

## 📞 Support

If issues persist:
- Check the main README.md for detailed setup instructions
- Review error messages in browser console (F12)
- Check backend and ML service terminal outputs

