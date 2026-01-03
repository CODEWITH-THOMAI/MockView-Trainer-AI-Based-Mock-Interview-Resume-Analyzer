-- =============================================
-- MOCKVIEW TRAINER DATABASE SCHEMA
-- PostgreSQL Schema for Supabase
-- =============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================
-- USERS TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    skill_level VARCHAR(50) DEFAULT 'Beginner', -- Beginner, Intermediate, Advanced
    job_role VARCHAR(255) DEFAULT 'Software Engineer',
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================
-- INTERVIEW SESSIONS TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS interview_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    job_role VARCHAR(255) NOT NULL,
    skill_level VARCHAR(50) NOT NULL,
    interview_type VARCHAR(50) DEFAULT 'text', -- text, voice, chat
    questions JSONB NOT NULL, -- Array of question objects
    answers JSONB NOT NULL, -- Array of answer objects
    scores JSONB, -- Overall scores object
    feedback JSONB, -- Detailed feedback object
    overall_score INTEGER, -- 0-100
    status VARCHAR(50) DEFAULT 'in_progress', -- in_progress, completed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- =============================================
-- FLUENCY TESTS TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS fluency_tests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    transcript TEXT NOT NULL,
    audio_url TEXT, -- URL to stored audio file (optional)
    fluency_score INTEGER, -- 0-100
    pronunciation_score INTEGER, -- 0-100
    grammar_score INTEGER, -- 0-100
    wpm INTEGER, -- Words per minute
    pause_count INTEGER,
    filler_word_count INTEGER,
    grammar_errors JSONB, -- Array of grammar error objects
    feedback JSONB, -- Detailed feedback array
    overall_score INTEGER, -- 0-100
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================
-- RESUMES TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS resumes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    resume_type VARCHAR(50) DEFAULT 'uploaded', -- uploaded, built
    file_url TEXT, -- URL to uploaded resume (for uploaded type)
    content JSONB, -- Structured resume content
    parsed_text TEXT, -- Extracted text from PDF
    analysis JSONB, -- Analysis results
    ats_score INTEGER, -- 0-100
    grammar_score INTEGER,
    keyword_match_score INTEGER,
    overall_score INTEGER, -- 0-100
    suggestions JSONB, -- Array of improvement suggestions
    target_job_role VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================
-- CHAT HISTORY TABLE (AI Chatbox)
-- =============================================
CREATE TABLE IF NOT EXISTS chat_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_id UUID, -- Group messages by session
    message_type VARCHAR(50) NOT NULL, -- user, ai
    message TEXT NOT NULL,
    context JSONB, -- Additional context data
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================
-- INDEXES FOR PERFORMANCE
-- =============================================
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_interview_sessions_user_id ON interview_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_interview_sessions_created_at ON interview_sessions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_fluency_tests_user_id ON fluency_tests(user_id);
CREATE INDEX IF NOT EXISTS idx_fluency_tests_created_at ON fluency_tests(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_resumes_user_id ON resumes(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_user_id ON chat_history(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_session_id ON chat_history(session_id);

-- =============================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- =============================================

-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE interview_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE fluency_tests ENABLE ROW LEVEL SECURITY;
ALTER TABLE resumes ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;

-- Users can only read/update their own profile
CREATE POLICY users_select_own ON users FOR SELECT USING (auth.uid() = id);
CREATE POLICY users_update_own ON users FOR UPDATE USING (auth.uid() = id);

-- Users can only access their own interview sessions
CREATE POLICY interview_sessions_crud_own ON interview_sessions 
    FOR ALL USING (auth.uid() = user_id);

-- Users can only access their own fluency tests
CREATE POLICY fluency_tests_crud_own ON fluency_tests 
    FOR ALL USING (auth.uid() = user_id);

-- Users can only access their own resumes
CREATE POLICY resumes_crud_own ON resumes 
    FOR ALL USING (auth.uid() = user_id);

-- Users can only access their own chat history
CREATE POLICY chat_history_crud_own ON chat_history 
    FOR ALL USING (auth.uid() = user_id);

-- =============================================
-- FUNCTIONS & TRIGGERS
-- =============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_resumes_updated_at BEFORE UPDATE ON resumes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
