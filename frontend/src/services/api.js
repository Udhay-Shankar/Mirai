/**
 * API service for backend communication
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (firebaseToken, provider) =>
    apiClient.post('/api/auth/register', { firebase_token: firebaseToken, provider }),
  
  getMe: () => apiClient.get('/api/auth/me'),
  
  logout: () => apiClient.post('/api/auth/logout'),
  
  verifyToken: (firebaseToken) =>
    apiClient.post('/api/auth/verify-token', { firebase_token: firebaseToken }),
};

// Analytics API
export const analyticsAPI = {
  search: (keyword, startDate, endDate, alertId) =>
    apiClient.post('/api/analytics/search', {
      keyword,
      start_date: startDate,
      end_date: endDate,
      alert_id: alertId,
    }),
  
  getInfluencers: (keyword, minFollowers = 1000, limit = 20) =>
    apiClient.get('/api/analytics/influencers', {
      params: { keyword, min_followers: minFollowers, limit },
    }),
  
  getTrending: (keyword, limit = 20) =>
    apiClient.get('/api/analytics/trending', {
      params: { keyword, limit },
    }),
  
  compareCompetitors: (primaryKeyword, competitors) =>
    apiClient.post('/api/analytics/competitors', null, {
      params: { primary_keyword: primaryKeyword, competitors },
    }),
  
  getSimilarCreators: (keyword, minCoOccurrence = 3) =>
    apiClient.get('/api/analytics/similar-creators', {
      params: { keyword, min_co_occurrence: minCoOccurrence },
    }),
  
  getDemographics: (keyword) =>
    apiClient.get('/api/analytics/demographics', {
      params: { keyword },
    }),
};

// Subscription API
export const subscriptionAPI = {
  getStatus: () => apiClient.get('/api/subscription/status'),
  
  upgrade: (tier, paymentToken) =>
    apiClient.post('/api/subscription/upgrade', {
      tier,
      payment_token: paymentToken,
    }),
  
  cancel: () => apiClient.post('/api/subscription/cancel'),
  
  getFeatures: () => apiClient.get('/api/subscription/features'),
};

export default apiClient;
