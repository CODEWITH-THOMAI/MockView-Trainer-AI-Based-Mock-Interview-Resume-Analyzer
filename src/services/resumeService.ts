/**
 * Resume Service
 * Handles resume building, analysis, and export
 */

import apiClient, { API_ENDPOINTS } from './api';

export interface ResumeContent {
  personal_info?: any;
  education?: any[];
  experience?: any[];
  skills?: string[];
  certifications?: any[];
  projects?: any[];
}

export interface BuildResumeData extends ResumeContent {}

export interface AnalyzeResumeData {
  resume_text: string;
  job_role?: string;
}

/**
 * Build a resume from form data
 */
export const buildResume = async (data: BuildResumeData): Promise<any> => {
  try {
    const response = await apiClient.post(API_ENDPOINTS.RESUME.BUILD, data);
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to build resume',
      error: error.message,
    };
  }
};

/**
 * Analyze a resume
 */
export const analyzeResume = async (data: AnalyzeResumeData): Promise<any> => {
  try {
    const response = await apiClient.post(API_ENDPOINTS.RESUME.ANALYZE, data);
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to analyze resume',
      error: error.message,
    };
  }
};

/**
 * Get available resume templates
 */
export const getTemplates = async (): Promise<any> => {
  try {
    const response = await apiClient.get(API_ENDPOINTS.RESUME.TEMPLATES);
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to get templates',
      error: error.message,
    };
  }
};

/**
 * Export resume as PDF
 */
export const exportResume = async (resumeId: string, template: string = 'modern'): Promise<any> => {
  try {
    const response = await apiClient.post(API_ENDPOINTS.RESUME.EXPORT, {
      resume_id: resumeId,
      template,
    });
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to export resume',
      error: error.message,
    };
  }
};

/**
 * Get resume feedback
 */
export const getResumeFeedback = async (resumeId: string): Promise<any> => {
  try {
    const response = await apiClient.get(API_ENDPOINTS.RESUME.FEEDBACK(resumeId));
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to get resume feedback',
      error: error.message,
    };
  }
};
