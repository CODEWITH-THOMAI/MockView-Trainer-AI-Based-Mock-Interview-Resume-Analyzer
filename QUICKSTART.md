# Quick Start Guide for MockView Trainer

## Step 1: Clone Repository
```bash
git clone https://github.com/CODEWITH-THOMAI/MockView-Trainer-AI-Based-Mock-Interview-Resume-Analyzer.git
cd MockView-Trainer-AI-Based-Mock-Interview-Resume-Analyzer
```

## Step 2: Frontend Setup (5 minutes)

```bash
# Install Node.js dependencies
npm install

# Create environment file
cp .env.example .env

# Edit .env if needed (default: http://localhost:5000/api)
```

## Step 3: Backend Setup (10 minutes)

```bash
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Download NLTK data (required for NLP)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('vader_lexicon'); nltk.download('averaged_perceptron_tagger')"

# Copy environment template
cp .env.example .env
```

## Step 4: Firebase Setup (15 minutes)

### 4.1 Create Firebase Project
1. Go to https://console.firebase.google.com/
2. Click "Add project"
3. Name it "MockView-Trainer" (or your choice)
4. Follow the setup wizard

### 4.2 Enable Services
1. **Firestore Database**:
   - Go to Firestore Database
   - Click "Create database"
   - Choose "Start in test mode"
   - Select location (closest to you)

2. **Authentication**:
   - Go to Authentication
   - Click "Get started"
   - Enable "Email/Password" provider

3. **Storage** (Optional for resume uploads):
   - Go to Storage
   - Click "Get started"

### 4.3 Get Service Account Key
1. Go to Project Settings (gear icon)
2. Click "Service accounts" tab
3. Click "Generate new private key"
4. Save the JSON file as `firebase-credentials.json` in `backend/` folder

### 4.4 Update Backend .env
```env
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
FIREBASE_DATABASE_URL=https://your-project-id.firebaseio.com
```

## Step 5: Start the Application

### Terminal 1 - Backend Server
```bash
cd backend
python app.py
```
**Backend running at:** http://localhost:5000

### Terminal 2 - Frontend Server
```bash
# In root directory
npm run dev
```
**Frontend running at:** http://localhost:5173

## Step 6: Test the Application

1. Open browser: http://localhost:5173
2. Click "Get Started" or "Login"
3. Create an account with email/password
4. Try features:
   - Dashboard → Mock Interview
   - Dashboard → Fluency Tester
   - Dashboard → Resume Builder

## Common Issues & Solutions

### Issue: "Module not found" (Python)
```bash
pip install -r backend/requirements.txt
```

### Issue: NLTK data not found
```bash
python -c "import nltk; nltk.download('all')"
```

### Issue: Firebase error "credentials not found"
- Ensure `firebase-credentials.json` is in `backend/` folder
- Check file permissions (should be readable)

### Issue: CORS error in browser
- Verify backend is running on port 5000
- Check `FRONTEND_URL` in `backend/.env` matches your frontend URL

### Issue: Port 5000 already in use
**Option 1**: Change backend port in `backend/.env`:
```env
PORT=5001
```

**Option 2**: Kill the process using port 5000:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

## Development Tips

### Run Backend in Debug Mode
```bash
cd backend
export FLASK_ENV=development  # Linux/macOS
set FLASK_ENV=development     # Windows CMD
python app.py
```

### Build Frontend for Production
```bash
npm run build
npm run preview
```

### Test API with curl
```bash
# Test signup
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","name":"Test User"}'

# Test health check
curl http://localhost:5000/health
```

## Environment Variables Reference

### Frontend (.env)
```env
VITE_API_URL=http://localhost:5000/api
```

### Backend (.env)
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
PORT=5000
FRONTEND_URL=http://localhost:5173
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
JWT_SECRET_KEY=your-jwt-secret
```

## Next Steps

1. Explore the codebase
2. Try all features (Interview, Fluency, Resume)
3. Review the comprehensive README.md
4. Customize for your needs
5. Deploy to production (see deployment guide)

## Getting Help

- Check README.md for detailed documentation
- Review troubleshooting section
- Check code comments for implementation details
- Create an issue on GitHub

## Success Checklist

- [ ] Node.js and Python installed
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] NLTK data downloaded
- [ ] Firebase project created
- [ ] Firebase credentials added to backend
- [ ] Backend server running (port 5000)
- [ ] Frontend server running (port 5173)
- [ ] Can access http://localhost:5173
- [ ] Can create account and login
- [ ] Features work (interview, fluency, resume)

🎉 **Congratulations! MockView Trainer is now running!**
