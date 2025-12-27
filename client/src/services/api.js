/**
 * API Service
 * Handles all API calls to the backend
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Search for a song by lyrics
 * @param {string} lyrics - The lyrics snippet to search
 * @returns {Promise} API response with song, artist, and confidence
 */
export const searchSong = async (lyrics) => {
  try {
    const response = await api.post('/api/search', { lyrics });
    return response.data;
  } catch (error) {
    if (error.response) {
      // Server responded with error status
      throw new Error(error.response.data.error || 'Search failed');
    } else if (error.request) {
      // Request made but no response
      throw new Error('Unable to connect to server. Please check if the backend is running.');
    } else {
      // Error setting up request
      throw new Error('An error occurred while making the request');
    }
  }
};

/**
 * Get search history
 * @param {number} page - Page number (default: 1)
 * @param {number} limit - Items per page (default: 20)
 * @returns {Promise} API response with history data
 */
export const getHistory = async (page = 1, limit = 20) => {
  try {
    const response = await api.get('/api/history', {
      params: { page, limit }
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.error || 'Failed to fetch history');
    } else if (error.request) {
      throw new Error('Unable to connect to server');
    } else {
      throw new Error('An error occurred while fetching history');
    }
  }
};

export default api;

