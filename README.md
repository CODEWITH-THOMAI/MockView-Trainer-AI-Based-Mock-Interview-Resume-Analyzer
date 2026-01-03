# MockView Trainer - AI-Based Mock Interview & Resume Analyzer

🎯 **Full-Stack AI-Powered Interview Preparation Platform**

MockView Trainer is a comprehensive university final year project that leverages AI/ML/NLP technologies to help job seekers prepare for interviews through mock interviews, fluency testing, and resume analysis.

## 🌟 Features

### 1. AI Mock Interview
- **Dynamic Question Generation**: Questions tailored to job role and skill level
- **Real-time Answer Evaluation**: NLP-powered analysis of responses
- **Text & Voice Input**: Support for both typed and spoken answers
- **Comprehensive Feedback**: Detailed scoring on relevance, grammar, completeness, and confidence
- **Multiple Job Roles**: Software Engineer, Data Scientist, Product Manager, Frontend/Backend Developer, and more

### 2. English Fluency Tester
- **Speech Analysis**: Analyze speaking fluency using speech-to-text
- **Detailed Metrics**: Words per minute (WPM), pause frequency, filler words
- **Grammar Checking**: Identify grammar errors in speech
- **Actionable Feedback**: Specific suggestions for improvement
- **Progress Tracking**: Monitor fluency improvement over time

### 3. Resume Builder
- **Multi-Step Form**: Easy-to-use interface for resume creation
- **Professional Templates**: 3+ ATS-friendly templates
- **Live Preview**: See resume as you build it
- **PDF Export**: Download resume in PDF format

### 4. Resume Analyzer
- **AI-Powered Analysis**: NLP-based resume evaluation
- **ATS Compatibility Check**: Ensure resume passes Applicant Tracking Systems
- **Keyword Matching**: Job-specific keyword analysis
- **Grammar & Spell Check**: Identify errors in resume content
- **Improvement Suggestions**: Detailed recommendations

### 5. Dashboard & Analytics
- **Performance Statistics**: Track interview scores, fluency scores, and resume scores
- **Session History**: View all past interviews, tests, and analyses
- **Trend Analysis**: Visualize improvement over time

## 🏗️ Technology Stack

### Frontend
- React 19 + TypeScript
- Tailwind CSS + Radix UI
- Vite
- Axios

### Backend
- Flask (Python)
- Firebase (Authentication, Firestore, Storage)
- JWT Authentication

### AI/ML/NLP
- NLTK (Natural Language Toolkit)
- SpaCy
- Scikit-learn
- TF-IDF & Cosine Similarity
- VADER Sentiment Analysis

## 📋 Prerequisites

- Node.js (v18+)
- Python (v3.9+)
- Firebase Account
- npm/yarn
- pip

## 🚀 Quick Start

### Frontend Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('vader_lexicon')"

# Configure Firebase
# 1. Add firebase-credentials.json to backend/
# 2. Copy .env.example to .env and configure

# Start server
python app.py
```

## 📁 Project Structure

```
├── backend/
│   ├── app.py                    # Flask application
│   ├── config.py                 # Configuration
│   ├── routes/                   # API endpoints
│   ├── models/                   # Data models
│   ├── services/                 # Business logic
│   ├── ml_models/                # ML/NLP modules
│   ├── database/                 # Firebase config
│   └── data/                     # Question banks & keywords
├── src/
│   ├── components/               # React components
│   └── services/                 # API services
└── README.md
```

## 🔑 Key API Endpoints

### Authentication
- `POST /api/auth/signup` - Register user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get profile
- `PUT /api/auth/profile` - Update profile

### Interview
- `POST /api/interview/start` - Start interview
- `POST /api/interview/submit-answer` - Submit answer
- `GET /api/interview/feedback/:id` - Get feedback

### Fluency
- `POST /api/fluency/test` - Start fluency test
- `POST /api/fluency/analyze` - Analyze speech
- `GET /api/fluency/score/:id` - Get results

### Resume
- `POST /api/resume/build` - Build resume
- `POST /api/resume/analyze` - Analyze resume
- `GET /api/resume/templates` - Get templates

### Dashboard
- `GET /api/dashboard/stats` - Get statistics
- `GET /api/dashboard/history` - Get history

## 🛠️ Firebase Setup

1. Create Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Firestore, Authentication, and Storage
3. Generate service account key (Project Settings → Service Accounts)
4. Save as `backend/firebase-credentials.json`
5. Update `backend/.env` with Firebase URL

## 🧪 Testing

Frontend runs on: `http://localhost:5173`
Backend runs on: `http://localhost:5000`

Test API with Postman, curl, or Thunder Client.

## 🛠️ Troubleshooting

**NLTK data not found:**
```bash
python -c "import nltk; nltk.download('all')"
```

**Firebase errors:**
- Verify `firebase-credentials.json` exists
- Check Firebase project configuration
- Ensure Firestore and Auth are enabled

**CORS issues:**
- Check `FRONTEND_URL` in `backend/.env`
- Verify Flask-CORS configuration

## 📝 Environment Variables

### Backend (.env)
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
PORT=5000
FRONTEND_URL=http://localhost:5173
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:5000/api
```

## 🎓 Academic Project

This is a university final year project demonstrating:
- Full-stack development skills
- AI/ML/NLP integration
- RESTful API design
- Database management
- Clean code practices
- Professional documentation

## 📚 Documentation

Full API documentation and detailed setup instructions are available in this README. For additional help:
- Check troubleshooting section
- Review code comments
- Create an issue on GitHub

## 👥 Author

**CODEWITH-THOMAI**

## 📧 Contact

- GitHub: [CODEWITH-THOMAI](https://github.com/CODEWITH-THOMAI)
- Issues: [Create an issue](https://github.com/CODEWITH-THOMAI/MockView-Trainer-AI-Based-Mock-Interview-Resume-Analyzer/issues)

## 📄 License

ISC License

---

**Note**: This project is designed for educational purposes and showcases real-world application of AI technologies in the HR tech domain.
