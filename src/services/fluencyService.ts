/**
 * Fluency Service
 * Handles fluency tests and speech analysis
 */

import apiClient, { API_ENDPOINTS } from './api';

export interface FluencyTestData {
  test_id: string;
  transcript: string;
  audio_duration?: number;
}

/**
 * Start a new fluency test
 */
export const startFluencyTest = async (): Promise<any> => {
  try {
    const response = await apiClient.post(API_ENDPOINTS.FLUENCY.TEST);
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to start fluency test',
      error: error.message,
    };
  }
};

/**
 * Submit transcript for fluency analysis
 */
export const submitTranscript = async (data: FluencyTestData): Promise<any> => {
  try {
    const response = await apiClient.post(API_ENDPOINTS.FLUENCY.ANALYZE, data);
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to analyze fluency',
      error: error.message,
    };
  }
};

/**
 * Get fluency test score
 */
export const getFluencyScore = async (testId: string): Promise<any> => {
  try {
    const response = await apiClient.get(API_ENDPOINTS.FLUENCY.SCORE(testId));
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to get fluency score',
      error: error.message,
    };
  }
};
