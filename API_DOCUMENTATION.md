# MockView Trainer API Documentation

Base URL: `http://localhost:5000/api`

## Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### Response Format

All API responses follow this standard format:

```json
{
  "success": true/false,
  "message": "Description of the result",
  "data": { ... },
  "error": "Error details if any"
}
```

---

## Authentication Endpoints

### POST /api/auth/signup

Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "name": "John Doe",
  "skill_level": "Beginner",  // Optional: Beginner, Intermediate, Advanced
  "job_role": "Software Engineer"  // Optional
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "User created successfully",
  "data": {
    "user": {
      "uid": "firebase-uid",
      "email": "user@example.com",
      "name": "John Doe",
      "skill_level": "Beginner",
      "job_role": "Software Engineer"
    },
    "token": "jwt-token-string"
  }
}
```

**Error Response (400):**
```json
{
  "success": false,
  "message": "Email already exists"
}
```

---

### POST /api/auth/login

Authenticate a user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": { ... },
    "token": "jwt-token-string"
  }
}
```

---

### GET /api/auth/profile

Get current user profile. **Requires authentication.**

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "uid": "...",
    "email": "user@example.com",
    "name": "John Doe",
    "skill_level": "Beginner",
    "job_role": "Software Engineer"
  }
}
```

---

### PUT /api/auth/profile

Update user profile. **Requires authentication.**

**Request Body:**
```json
{
  "name": "John Updated",
  "skill_level": "Intermediate",
  "job_role": "Full Stack Developer"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": { ... }
}
```

---

## Interview Endpoints

### POST /api/interview/start

Start a new interview session. **Requires authentication.**

**Request Body:**
```json
{
  "job_role": "Software Engineer",
  "skill_level": "Intermediate",
  "num_questions": 5  // Optional, default: 5, max: 10
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "Interview session started",
  "data": {
    "session_id": "uuid",
    "job_role": "Software Engineer",
    "skill_level": "Intermediate",
    "questions": [
      {
        "id": "q_1",
        "question": "Explain the SOLID principles...",
        "job_role": "Software Engineer",
        "skill_level": "Intermediate",
        "order": 1
      }
    ],
    "total_questions": 5
  }
}
```

---

### GET /api/interview/questions

Get interview questions without creating a session. **Requires authentication.**

**Query Parameters:**
- `job_role` - Job role (default: "Software Engineer")
- `skill_level` - Skill level (default: "Beginner")
- `count` - Number of questions (default: 5)

**Example:** `/api/interview/questions?job_role=Data%20Scientist&skill_level=Advanced&count=3`

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "questions": [ ... ],
    "job_role": "Data Scientist",
    "skill_level": "Advanced"
  }
}
```

---

### POST /api/interview/submit-answer

Submit an answer for AI evaluation. **Requires authentication.**

**Request Body:**
```json
{
  "session_id": "session-uuid",
  "question_id": "q_1",
  "question": "Explain the SOLID principles...",
  "answer": "SOLID principles are five design principles: Single Responsibility..."
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Answer submitted and evaluated",
  "data": {
    "evaluation": {
      "overall_score": 85.5,
      "relevance": {
        "score": 88.0,
        "matched_keywords": ["SOLID", "principles", "design"]
      },
      "grammar": {
        "score": 90.0,
        "error_count": 1
      },
      "completeness": {
        "score": 82.0,
        "word_count": 45
      },
      "sentiment_score": 75.0,
      "feedback": [
        "Excellent answer! You demonstrated strong understanding.",
        "Good use of relevant keywords..."
      ]
    }
  }
}
```

---

### POST /api/interview/voice-answer

Submit a voice-based answer. **Requires authentication.**

**Request Body:**
```json
{
  "session_id": "session-uuid",
  "question_id": "q_1",
  "question": "Explain...",
  "transcript": "Text from speech-to-text...",
  "audio_duration": 45.5  // Optional, in seconds
}
```

**Success Response:** Same as `/submit-answer`

---

### GET /api/interview/feedback/:sessionId

Get complete feedback for an interview session. **Requires authentication.**

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "session_id": "uuid",
    "job_role": "Software Engineer",
    "skill_level": "Intermediate",
    "overall_score": 82.5,
    "scores": {
      "q_1": {
        "score": 85.5,
        "relevance": 88.0,
        "grammar": 90.0
      }
    },
    "answers": [ ... ],
    "questions": [ ... ]
  }
}
```

---

## Fluency Test Endpoints

### POST /api/fluency/test

Start a new fluency test. **Requires authentication.**

**Success Response (201):**
```json
{
  "success": true,
  "message": "Fluency test started",
  "data": {
    "test_id": "test-uuid"
  }
}
```

---

### POST /api/fluency/analyze

Analyze speech fluency. **Requires authentication.**

**Request Body:**
```json
{
  "test_id": "test-uuid",
  "transcript": "This is my speech transcript. I am speaking clearly...",
  "audio_duration": 60.0  // Optional, in seconds
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Fluency analyzed successfully",
  "data": {
    "test_id": "test-uuid",
    "overall_score": 78.5,
    "fluency_score": 75.0,
    "pronunciation_score": 85.0,
    "grammar_score": 80.0,
    "wpm": 125.5,
    "word_count": 125,
    "filler_word_count": 3,
    "pause_count": 2,
    "feedback": [
      "Good fluency with room for minor improvements.",
      "Perfect speaking pace (125 WPM)!",
      "You used 3 filler words..."
    ]
  }
}
```

---

### GET /api/fluency/score/:testId

Get fluency test results. **Requires authentication.**

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "test_id": "test-uuid",
    "overall_score": 78.5,
    "fluency_score": 75.0,
    "pronunciation_score": 85.0,
    "grammar_score": 80.0,
    "wpm": 125.5,
    "feedback": [ ... ]
  }
}
```

---

## Resume Endpoints

### POST /api/resume/build

Build a resume from form data. **Requires authentication.**

**Request Body:**
```json
{
  "personal_info": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890"
  },
  "education": [
    {
      "degree": "Bachelor of Science",
      "major": "Computer Science",
      "university": "MIT",
      "year": "2023"
    }
  ],
  "experience": [ ... ],
  "skills": ["Python", "React", "Node.js"],
  "certifications": [ ... ],
  "projects": [ ... ]
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "Resume created successfully",
  "data": {
    "resume_id": "resume-uuid",
    "content": { ... }
  }
}
```

---

### POST /api/resume/analyze

Analyze a resume. **Requires authentication.**

**Request Body:**
```json
{
  "resume_text": "John Doe\nSoftware Engineer\n\nExperience:\n...",
  "job_role": "Software Engineer"  // Optional
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Resume analyzed successfully",
  "data": {
    "resume_id": "resume-uuid",
    "overall_score": 75.0,
    "analysis": {
      "grammar_score": 85.0,
      "structure_score": 75.0,
      "ats_score": 80.0,
      "keyword_score": 65.0,
      "word_count": 250
    },
    "suggestions": [
      "Review grammar and spelling...",
      "Add more Software Engineer-specific keywords..."
    ]
  }
}
```

---

### GET /api/resume/templates

Get available resume templates. **Requires authentication.**

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "templates": [
      {
        "id": "modern",
        "name": "Modern Professional",
        "description": "Clean and modern design..."
      }
    ]
  }
}
```

---

### POST /api/resume/export

Export resume as PDF. **Requires authentication.**

**Request Body:**
```json
{
  "resume_id": "resume-uuid",
  "template": "modern"  // Optional, default: "modern"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Resume export initiated",
  "data": {
    "resume_id": "resume-uuid",
    "download_url": "/downloads/resume_uuid.pdf"
  }
}
```

---

### GET /api/resume/feedback/:resumeId

Get resume feedback. **Requires authentication.**

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "resume_id": "resume-uuid",
    "score": 75.0,
    "analysis": { ... },
    "suggestions": [ ... ]
  }
}
```

---

## Dashboard Endpoints

### GET /api/dashboard/stats

Get user statistics. **Requires authentication.**

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "interviews": {
      "total_count": 10,
      "average_score": 82.5,
      "latest_score": 85.0
    },
    "fluency_tests": {
      "total_count": 5,
      "average_score": 78.0,
      "latest_score": 80.0
    },
    "resumes": {
      "total_count": 3,
      "latest_score": 75.0
    },
    "overall": {
      "total_activities": 18,
      "overall_performance": 78.5
    }
  }
}
```

---

### GET /api/dashboard/history

Get session history. **Requires authentication.**

**Query Parameters:**
- `limit` - Number of results (default: 10)

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "history": [
      {
        "id": "session-uuid",
        "type": "interview",
        "title": "Software Engineer Interview - Intermediate",
        "score": 85.0,
        "status": "completed",
        "timestamp": "2024-01-15T10:30:00Z"
      }
    ],
    "total": 10
  }
}
```

---

### GET /api/dashboard/trends

Get performance trends. **Requires authentication.**

**Query Parameters:**
- `days` - Number of days (default: 30)

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "date_range": {
      "start": "2024-01-01T00:00:00Z",
      "end": "2024-01-31T23:59:59Z",
      "days": 30
    },
    "trends": {
      "interviews": [
        { "date": "2024-01-15", "score": 85.0 }
      ],
      "fluency": [
        { "date": "2024-01-20", "score": 80.0 }
      ]
    }
  }
}
```

---

## Error Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (missing or invalid token)
- `403` - Forbidden (no permission)
- `404` - Not Found
- `500` - Internal Server Error
- `503` - Service Unavailable (database error)

---

## Rate Limiting

Currently, no rate limiting is enforced. In production, consider implementing rate limiting to prevent abuse.

---

## Testing with curl

```bash
# Sign up
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","name":"Test"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# Get profile (with token)
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

For more information, see the main README.md file.
