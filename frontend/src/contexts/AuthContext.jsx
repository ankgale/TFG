/**
 * AuthContext - Manages authentication state across the app.
 * 
 * Provides:
 * - user: Current user data (null if not logged in)
 * - isAuthenticated: Boolean indicating login status
 * - login: Function to log in a user
 * - logout: Function to log out
 * - loading: Boolean indicating if auth state is being checked
 */

import { createContext, useContext, useState, useEffect } from 'react';
import { usersApi } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check for existing session on mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('userId');
    
    if (token && userId) {
      // Fetch user data
      fetchUser(userId);
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUser = async (userId) => {
    try {
      const userData = await usersApi.getUser(userId);
      setUser(userData);
    } catch (error) {
      // Token might be invalid, clear storage
      console.error('Failed to fetch user:', error);
      localStorage.removeItem('token');
      localStorage.removeItem('userId');
    } finally {
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    const response = await usersApi.login(username, password);
    
    // Store token and user ID
    localStorage.setItem('token', response.token);
    localStorage.setItem('userId', response.user_id);
    
    // Fetch full user data
    await fetchUser(response.user_id);
    
    return response;
  };

  const register = async (username, email, password, passwordConfirm) => {
    const response = await usersApi.register(username, email, password, passwordConfirm);
    return response;
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    setUser(null);
  };

  const value = {
    user,
    isAuthenticated: !!user,
    loading,
    login,
    register,
    logout,
    refreshUser: () => {
      const userId = localStorage.getItem('userId');
      if (userId) fetchUser(userId);
    },
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook to use auth context
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export default AuthContext;
