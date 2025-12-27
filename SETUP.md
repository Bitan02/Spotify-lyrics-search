# Quick Setup Guide

## Prerequisites Checklist

- [ ] Node.js (v16+) installed
- [ ] Python (v3.8+) installed
- [ ] MongoDB Atlas account created
- [ ] npm or yarn installed

## Step-by-Step Setup

### 1. ML Service Setup

```bash
cd ml-service
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python train_model.py
```

### 2. Backend Setup

```bash
cd ../server
npm install

# Create .env file with:
# PORT=3001
# MONGODB_URI=your_mongodb_connection_string
# ML_SERVICE_URL=http://localhost:8000
```

### 3. Frontend Setup

```bash
cd ../client
npm install
```

### 4. Run All Services

**Terminal 1 (ML Service):**
```bash
cd ml-service
python app.py
```

**Terminal 2 (Backend):**
```bash
cd server
npm start
```

**Terminal 3 (Frontend):**
```bash
cd client
npm start
```

### 5. Access Application

Open http://localhost:3000 in your browser.

## MongoDB Atlas Setup

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for free account
3. Create a new cluster (free tier)
4. Create database user (Database Access)
5. Whitelist IP (Network Access) - use 0.0.0.0/0 for development
6. Get connection string (Connect > Connect your application)
7. Replace `<password>` with your password
8. Add to server/.env as MONGODB_URI

## Troubleshooting

- **ML Service won't start**: Run `python train_model.py` first
- **Backend connection error**: Check MongoDB URI and network whitelist
- **Frontend can't connect**: Ensure backend is running on port 3001

