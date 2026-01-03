/**
 * Authentication Service
 * Handles user authentication, registration, and profile management
 * Updated to work with Supabase backend
 */

import apiClient, { API_ENDPOINTS } from './api';

export interface SignupData {
  email: string;
  password: string;
  name: string;
  skill_level?: string;
  job_role?: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface User {
  id: string;
  email: string;
  name: string;
  skill_level: string;
  job_role: string;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  data?: {
    user: User;
    session?: any;
    access_token?: string;
  };
  error?: string;
}

/**
 * Sign up a new user
 */
export const signup = async (data: SignupData): Promise<AuthResponse> => {
  try {
    const response = await apiClient.post(API_ENDPOINTS.AUTH.SIGNUP, data);
    
    if (response.data.success && response.data.data) {
      // Store token and user data
      if (response.data.data.access_token) {
        localStorage.setItem('authToken', response.data.data.access_token);
      }
      localStorage.setItem('user', JSON.stringify(response.data.data.user));
    }
    
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Signup failed',
      error: error.message,
    };
  }
};

/**
 * Login user
 */
export const login = async (data: LoginData): Promise<AuthResponse> => {
  try {
    const response = await apiClient.post(API_ENDPOINTS.AUTH.LOGIN, data);
    
    if (response.data.success && response.data.data) {
      // Store token and user data
      if (response.data.data.access_token) {
        localStorage.setItem('authToken', response.data.data.access_token);
      }
      localStorage.setItem('user', JSON.stringify(response.data.data.user));
    }
    
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Login failed',
      error: error.message,
    };
  }
};

/**
 * Logout user
 */
export const logout = async (): Promise<void> => {
  try {
    // Call backend logout endpoint
    await apiClient.post(API_ENDPOINTS.AUTH.LOGOUT);
  } catch (error) {
    console.error('Logout error:', error);
  } finally {
    // Clear local storage regardless of API call result
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  }
};

/**
 * Get current user profile
 */
export const getProfile = async (): Promise<any> => {
  try {
    const response = await apiClient.get(API_ENDPOINTS.AUTH.PROFILE);
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to get profile',
      error: error.message,
    };
  }
};

/**
 * Update user profile
 */
export const updateProfile = async (data: Partial<User>): Promise<any> => {
  try {
    const response = await apiClient.put(API_ENDPOINTS.AUTH.UPDATE_PROFILE, data);
    
    if (response.data.success && response.data.data) {
      // Update stored user data
      localStorage.setItem('user', JSON.stringify(response.data.data));
    }
    
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to update profile',
      error: error.message,
    };
  }
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = (): boolean => {
  const token = localStorage.getItem('authToken');
  return !!token;
};

/**
 * Get stored user data
 */
export const getCurrentUser = (): User | null => {
  const userStr = localStorage.getItem('user');
  if (userStr) {
    try {
      return JSON.parse(userStr);
    } catch {
      return null;
    }
  }
  return null;
};

/**
 * Get auth token
 */
export const getAuthToken = (): string | null => {
  return localStorage.getItem('authToken');
};
