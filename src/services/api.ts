/**
 * API Configuration and Axios Instance
 * Base configuration for all API calls
 */

import axios, { AxiosInstance, AxiosError } from 'axios';

// API base URL from environment or default to localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// Create Axios instance with default config
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    const token = localStorage.getItem('authToken');
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error: AxiosError) => {
    // Handle specific error cases
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      
      if (status === 401) {
        // Unauthorized - clear token and redirect to login
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        window.location.href = '/login';
      } else if (status === 403) {
        console.error('Forbidden: You do not have permission to access this resource');
      } else if (status === 404) {
        console.error('Resource not found');
      } else if (status === 500) {
        console.error('Server error: Please try again later');
      }
    } else if (error.request) {
      // Request made but no response received
      console.error('Network error: Unable to connect to server');
    }
    
    return Promise.reject(error);
  }
);

// API endpoints constants
export const API_ENDPOINTS = {
  // Authentication
  AUTH: {
    SIGNUP: '/auth/signup',
    LOGIN: '/auth/login',
    PROFILE: '/auth/profile',
    UPDATE_PROFILE: '/auth/profile',
  },
  // Interview
  INTERVIEW: {
    START: '/interview/start',
    QUESTIONS: '/interview/questions',
    SUBMIT_ANSWER: '/interview/submit-answer',
    VOICE_ANSWER: '/interview/voice-answer',
    FEEDBACK: (sessionId: string) => `/interview/feedback/${sessionId}`,
  },
  // Fluency
  FLUENCY: {
    TEST: '/fluency/test',
    ANALYZE: '/fluency/analyze',
    SCORE: (testId: string) => `/fluency/score/${testId}`,
  },
  // Resume
  RESUME: {
    BUILD: '/resume/build',
    ANALYZE: '/resume/analyze',
    TEMPLATES: '/resume/templates',
    EXPORT: '/resume/export',
    FEEDBACK: (resumeId: string) => `/resume/feedback/${resumeId}`,
  },
  // Dashboard
  DASHBOARD: {
    STATS: '/dashboard/stats',
    HISTORY: '/dashboard/history',
    TRENDS: '/dashboard/trends',
  },
};

export default apiClient;
