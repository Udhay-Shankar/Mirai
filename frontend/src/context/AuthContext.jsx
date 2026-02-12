/**
 * Auth Context for managing JWT authentication state
 * Supports: Email/Password, Google, Facebook, Twitter/X, Instagram OAuth
 */
import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Configure axios defaults
axios.defaults.baseURL = API_URL;

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const [refreshToken, setRefreshToken] = useState(null);

  // Initialize auth state from localStorage
  useEffect(() => {
    const initAuth = async () => {
      const storedAccessToken = localStorage.getItem('accessToken');
      const storedRefreshToken = localStorage.getItem('refreshToken');
      const storedUser = localStorage.getItem('user');

      if (storedAccessToken && storedUser) {
        setAccessToken(storedAccessToken);
        setRefreshToken(storedRefreshToken);
        setUser(JSON.parse(storedUser));
        
        // Set axios default header
        axios.defaults.headers.common['Authorization'] = `Bearer ${storedAccessToken}`;
        
        // Verify token is still valid
        try {
          const response = await axios.get('/api/auth/me');
          setUser(response.data);
          localStorage.setItem('user', JSON.stringify(response.data));
        } catch (err) {
          // Token might be expired, try to refresh
          if (storedRefreshToken) {
            try {
              await refreshAccessToken(storedRefreshToken);
            } catch (refreshErr) {
              // Refresh failed, logout user
              handleLogout();
            }
          } else {
            handleLogout();
          }
        }
      }
      
      setLoading(false);
    };

    initAuth();
  }, []);

  // Handle OAuth callback (called from redirect)
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const accessTokenParam = urlParams.get('access_token');
    const refreshTokenParam = urlParams.get('refresh_token');
    const provider = urlParams.get('provider');
    const errorParam = urlParams.get('error');

    if (errorParam) {
      setError(`Authentication failed with ${provider}`);
      // Clean up URL
      window.history.replaceState({}, document.title, window.location.pathname);
    } else if (accessTokenParam && refreshTokenParam) {
      // Store tokens
      storeTokens(accessTokenParam, refreshTokenParam);
      
      // Fetch user info
      axios.defaults.headers.common['Authorization'] = `Bearer ${accessTokenParam}`;
      axios.get('/api/auth/me')
        .then(response => {
          setUser(response.data);
          localStorage.setItem('user', JSON.stringify(response.data));
          // Clean up URL
          window.history.replaceState({}, document.title, '/dashboard');
        })
        .catch(err => {
          console.error('Error fetching user after OAuth:', err);
          setError('Failed to fetch user information');
        });
    }
  }, []);

  // Store tokens in state and localStorage
  const storeTokens = (access, refresh) => {
    setAccessToken(access);
    setRefreshToken(refresh);
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
  };

  // Refresh access token using refresh token
  const refreshAccessToken = async (refreshTok) => {
    try {
      const response = await axios.post('/api/auth/refresh', {
        refresh_token: refreshTok || refreshToken
      });
      
      const { access_token, refresh_token, user: userData } = response.data;
      storeTokens(access_token, refresh_token);
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      
      return access_token;
    } catch (err) {
      console.error('Token refresh failed:', err);
      throw err;
    }
  };

  // Setup axios interceptor to handle token refresh on 401
  useEffect(() => {
    const interceptor = axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;
        
        // If 401 and we haven't retried yet
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          
          try {
            const newAccessToken = await refreshAccessToken();
            originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
            return axios(originalRequest);
          } catch (refreshError) {
            handleLogout();
            return Promise.reject(refreshError);
          }
        }
        
        return Promise.reject(error);
      }
    );

    return () => {
      axios.interceptors.response.eject(interceptor);
    };
  }, [refreshToken]);

  // Email/Password Registration
  const signUpWithEmail = async (email, password, displayName = null) => {
    try {
      setError(null);
      const response = await axios.post('/api/auth/signup', {
        email,
        password,
        displayName: displayName || email.split('@')[0]
      });
      
      const { token, user: userData } = response.data;
      storeTokens(token, null); // No refresh token yet
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      
      return userData;
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Registration failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  };

  // Email/Password Login
  const signInWithEmail = async (email, password) => {
    try {
      setError(null);
      const response = await axios.post('/api/auth/login', {
        email,
        password
      });
      
      const { token, user: userData } = response.data;
      storeTokens(token, null); // No refresh token yet
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      
      return userData;
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Login failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  };

  // OAuth Sign In (Google, Facebook, Twitter, Instagram)
  const signInWithOAuth = (provider) => {
    if (!['google', 'facebook', 'twitter', 'instagram'].includes(provider)) {
      throw new Error(`Unsupported provider: ${provider}`);
    }
    
    // Redirect to backend OAuth endpoint
    window.location.href = `${API_URL}/api/auth/oauth/${provider}`;
  };

  // Google Sign In
  const signInWithGoogle = () => {
    return signInWithOAuth('google');
  };

  // Facebook Sign In
  const signInWithFacebook = () => {
    return signInWithOAuth('facebook');
  };

  // Twitter/X Sign In
  const signInWithTwitter = () => {
    return signInWithOAuth('twitter');
  };

  // Instagram Sign In
  const signInWithInstagram = () => {
    return signInWithOAuth('instagram');
  };

  // Logout
  const logout = async () => {
    try {
      await axios.post('/api/auth/logout');
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      handleLogout();
    }
  };

  // Clear local auth state
  const handleLogout = () => {
    setUser(null);
    setAccessToken(null);
    setRefreshToken(null);
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    delete axios.defaults.headers.common['Authorization'];
  };

  // Check if user is authenticated
  const isAuthenticated = () => {
    return !!user && !!accessToken;
  };

  // Check if user has premium subscription
  const isPremium = () => {
    return user?.subscription_tier === 'premium' || user?.subscription_tier === 'enterprise';
  };

  const value = {
    user,
    loading,
    error,
    accessToken,
    isAuthenticated,
    isPremium,
    signUpWithEmail,
    signInWithEmail,
    signInWithGoogle,
    signInWithFacebook,
    signInWithTwitter,
    signInWithInstagram,
    logout,
    refreshAccessToken,
    setError
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
