/**
 * API service for communicating with the Django backend.
 */

const API_BASE_URL = '/api';

/**
 * Generic fetch wrapper with error handling.
 * Automatically includes auth token if available.
 */
async function fetchApi(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  // Get auth token from localStorage
  const token = localStorage.getItem('token');
  
  const defaultHeaders = {
    'Content-Type': 'application/json',
  };
  
  // Add auth token if available
  if (token) {
    defaultHeaders['Authorization'] = `Token ${token}`;
  }
  
  const mergedOptions = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };
  
  const response = await fetch(url, mergedOptions);
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || error.error || `HTTP error ${response.status}`);
  }
  
  return response.json();
}

// ============ Lessons API ============

export const lessonsApi = {
  /**
   * Get all modules.
   */
  getModules: () => fetchApi('/lessons/modules/'),
  
  /**
   * Get a single module by ID.
   */
  getModule: (id) => fetchApi(`/lessons/modules/${id}/`),
  
  /**
   * Get all lessons.
   */
  getLessons: (moduleId = null) => {
    const params = moduleId ? `?module_id=${moduleId}` : '';
    return fetchApi(`/lessons/lessons/${params}`);
  },
  
  /**
   * Get a single lesson by ID.
   */
  getLesson: (id) => fetchApi(`/lessons/lessons/${id}/`),
  
  /**
   * Get quizzes for a lesson.
   */
  getLessonQuizzes: (lessonId) => fetchApi(`/lessons/lessons/${lessonId}/quizzes/`),
  
  /**
   * Submit quiz answer.
   */
  submitAnswer: (quizId, optionId) => fetchApi(`/lessons/quizzes/${quizId}/answer/`, {
    method: 'POST',
    body: JSON.stringify({ option_id: optionId }),
  }),
  
  /**
   * Start a lesson.
   */
  startLesson: (lessonId, userId = null) => fetchApi(`/lessons/lessons/${lessonId}/start/`, {
    method: 'POST',
    body: JSON.stringify({ user_id: userId }),
  }),
  
  /**
   * Complete a lesson.
   */
  completeLesson: (lessonId, userId = null, score = 100) => fetchApi(`/lessons/lessons/${lessonId}/complete/`, {
    method: 'POST',
    body: JSON.stringify({ user_id: userId, score }),
  }),
  
  /**
   * Get progress summary.
   */
  getProgressSummary: (userId = null) => {
    const params = userId ? `?user_id=${userId}` : '';
    return fetchApi(`/lessons/progress/summary/${params}`);
  },
};

// ============ Stocks API ============

export const stocksApi = {
  /**
   * Get all stocks.
   */
  getStocks: () => fetchApi('/stocks/stocks/'),
  
  /**
   * Get a single stock by ID.
   */
  getStock: (id) => fetchApi(`/stocks/stocks/${id}/`),
  
  /**
   * Get stock price history.
   */
  getStockHistory: (id, period = '1mo') => fetchApi(`/stocks/stocks/${id}/history/?period=${period}`),
  
  /**
   * Get real-time quote for a stock.
   */
  getStockQuote: (id) => fetchApi(`/stocks/stocks/${id}/quote/`),
  
  /**
   * Initialize stocks from config.
   */
  initializeStocks: () => fetchApi('/stocks/stocks/initialize/', { method: 'POST' }),
  
  /**
   * Refresh stock prices.
   */
  refreshPrices: () => fetchApi('/stocks/stocks/refresh/', { method: 'POST' }),
  
  /**
   * Get user's portfolio.
   */
  getPortfolio: (userId = null) => {
    const params = userId ? `?user_id=${userId}` : '';
    return fetchApi(`/stocks/portfolio/${params}`);
  },
  
  /**
   * Get portfolio summary.
   */
  getPortfolioSummary: (userId = null) => {
    const params = userId ? `?user_id=${userId}` : '';
    return fetchApi(`/stocks/portfolio/summary/${params}`);
  },
  
  /**
   * Execute a trade.
   */
  executeTrade: (stockId, shares, transactionType, userId = null) => fetchApi('/stocks/trade/', {
    method: 'POST',
    body: JSON.stringify({
      stock_id: stockId,
      shares,
      transaction_type: transactionType,
      user_id: userId,
    }),
  }),
  
  /**
   * Get transaction history.
   */
  getTransactions: (userId = null) => {
    const params = userId ? `?user_id=${userId}` : '';
    return fetchApi(`/stocks/transactions/${params}`);
  },
  
  /**
   * Get user's watchlist.
   */
  getWatchlist: (userId = null) => {
    const params = userId ? `?user_id=${userId}` : '';
    return fetchApi(`/stocks/watchlist/${params}`);
  },
  
  /**
   * Add stock to watchlist.
   */
  addToWatchlist: (stockId, userId = null) => fetchApi('/stocks/watchlist/', {
    method: 'POST',
    body: JSON.stringify({ stock_id: stockId, user_id: userId }),
  }),
  
  /**
   * Remove from watchlist.
   */
  removeFromWatchlist: (watchlistId) => fetchApi(`/stocks/watchlist/${watchlistId}/`, {
    method: 'DELETE',
  }),
};

// ============ Users API ============

export const usersApi = {
  /**
   * Get all users.
   */
  getUsers: () => fetchApi('/users/'),
  
  /**
   * Get a single user by ID.
   */
  getUser: (id) => fetchApi(`/users/${id}/`),
  
  /**
   * Get user progress.
   */
  getUserProgress: (id) => fetchApi(`/users/${id}/progress/`),
  
  /**
   * Add XP to user.
   */
  addXp: (userId, amount) => fetchApi(`/users/${userId}/add_xp/`, {
    method: 'POST',
    body: JSON.stringify({ amount }),
  }),
  
  /**
   * Get achievements.
   */
  getAchievements: () => fetchApi('/users/achievements/'),
  
  /**
   * Get user achievements.
   */
  getUserAchievements: (userId) => fetchApi(`/users/user-achievements/?user_id=${userId}`),

  /**
   * Login user.
   */
  login: (username, password) => fetchApi('/users/login/', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  }),
  
  /**
   * Register user.
   */
  register: (username, email, password, password_confirm) => fetchApi('/users/register/', {
    method: 'POST',
    body: JSON.stringify({ username, email, password, password_confirm }),
  }),
};

export default {
  lessons: lessonsApi,
  stocks: stocksApi,
  users: usersApi,
};
