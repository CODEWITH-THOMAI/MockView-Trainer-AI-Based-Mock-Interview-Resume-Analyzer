/**
 * Interview Service
 * Handles mock interview sessions and answer evaluations
 */

import apiClient, { API_ENDPOINTS } from './api';

export interface StartInterviewData {
  job_role: string;
  skill_level: string;
  num_questions?: number;
}

export interface SubmitAnswerData {
  session_id: string;
  question_id: string;
  question: string;
  answer: string;
}

export interface VoiceAnswerData extends SubmitAnswerData {
  transcript: string;
  audio_duration?: number;
}

/**
 * Start a new interview session
 */
export const startInterview = async (data: StartInterviewData): Promise<any> => {
  try {
    const response = await apiClient.post(API_ENDPOINTS.INTERVIEW.START, data);
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to start interview',
      error: error.message,
    };
  }
};

/**
 * Get interview questions
 */
export const getQuestions = async (
  jobRole: string,
  skillLevel: string,
  count: number = 5
): Promise<any> => {
  try {
    const response = await apiClient.get(API_ENDPOINTS.INTERVIEW.QUESTIONS, {
      params: { job_role: jobRole, skill_level: skillLevel, count },
    });
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to get questions',
      error: error.message,
    };
  }
};

/**
 * Submit an answer for evaluation
 */
export const submitAnswer = async (data: SubmitAnswerData): Promise<any> => {
  try {
    const response = await apiClient.post(API_ENDPOINTS.INTERVIEW.SUBMIT_ANSWER, data);
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to submit answer',
      error: error.message,
    };
  }
};

/**
 * Submit a voice answer for evaluation
 */
export const submitVoiceAnswer = async (data: VoiceAnswerData): Promise<any> => {
  try {
    const response = await apiClient.post(API_ENDPOINTS.INTERVIEW.VOICE_ANSWER, data);
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to submit voice answer',
      error: error.message,
    };
  }
};

/**
 * Get feedback for an interview session
 */
export const getFeedback = async (sessionId: string): Promise<any> => {
  try {
    const response = await apiClient.get(API_ENDPOINTS.INTERVIEW.FEEDBACK(sessionId));
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to get feedback',
      error: error.message,
    };
  }
};
