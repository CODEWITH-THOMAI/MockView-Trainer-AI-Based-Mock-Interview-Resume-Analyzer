/**
 * Dashboard Service
 * Handles analytics, statistics, and session history
 */

import apiClient, { API_ENDPOINTS } from './api';

/**
 * Get user statistics
 */
export const getStats = async (): Promise<any> => {
  try {
    const response = await apiClient.get(API_ENDPOINTS.DASHBOARD.STATS);
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to get statistics',
      error: error.message,
    };
  }
};

/**
 * Get session history
 */
export const getHistory = async (limit: number = 10): Promise<any> => {
  try {
    const response = await apiClient.get(API_ENDPOINTS.DASHBOARD.HISTORY, {
      params: { limit },
    });
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to get history',
      error: error.message,
    };
  }
};

/**
 * Get performance trends
 */
export const getTrends = async (days: number = 30): Promise<any> => {
  try {
    const response = await apiClient.get(API_ENDPOINTS.DASHBOARD.TRENDS, {
      params: { days },
    });
    return response.data;
  } catch (error: any) {
    return {
      success: false,
      message: error.response?.data?.message || 'Failed to get trends',
      error: error.message,
    };
  }
};
