import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { storage } from '../utils/storage';

const AppContext = createContext();

const appReducer = (state, action) => {
  switch (action.type) {
    case 'SET_THEME':
      return {
        ...state,
        theme: action.payload
      };
    case 'SET_SIDEBAR_OPEN':
      return {
        ...state,
        sidebarOpen: action.payload
      };
    case 'SET_MODAL_OPEN':
      return {
        ...state,
        modalOpen: action.payload,
        modalContent: action.payload ? state.modalContent : null
      };
    case 'SET_MODAL_CONTENT':
      return {
        ...state,
        modalContent: action.payload
      };
    case 'SET_NOTIFICATION':
      return {
        ...state,
        notification: action.payload
      };
    case 'CLEAR_NOTIFICATION':
      return {
        ...state,
        notification: null
      };
    case 'SET_LOADING':
      return {
        ...state,
        globalLoading: action.payload
      };
    case 'SET_ONLINE_STATUS':
      return {
        ...state,
        isOnline: action.payload
      };
    case 'SET_VIEWPORT':
      return {
        ...state,
        viewport: action.payload
      };
    case 'SET_USER':
      return {
        ...state,
        user: action.payload,
        isAuthenticated: !!action.payload
      };
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        isAuthenticated: false
      };
    default:
      return state;
  }
};

const initialState = {
  theme: 'light',
  sidebarOpen: false,
  modalOpen: false,
  modalContent: null,
  notification: null,
  globalLoading: false,
  isOnline: navigator.onLine,
  user: null,
  isAuthenticated: false,
  viewport: {
    width: window.innerWidth,
    height: window.innerHeight,
    isMobile: window.innerWidth < 768,
    isTablet: window.innerWidth >= 768 && window.innerWidth < 1024,
    isDesktop: window.innerWidth >= 1024
  }
};

export const AppProvider = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  // Load theme from localStorage on mount
  useEffect(() => {
    const savedTheme = storage.getTheme();
    if (savedTheme) {
      dispatch({ type: 'SET_THEME', payload: savedTheme });
    }
  }, []);

  // Restore authentication state from localStorage on mount
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    const userData = localStorage.getItem('userData');
    
    if (token && userData) {
      try {
        const user = JSON.parse(userData);
        dispatch({ type: 'SET_USER', payload: user });
      } catch (error) {
        console.error('Error parsing stored user data:', error);
        // Clear invalid data
        localStorage.removeItem('authToken');
        localStorage.removeItem('userData');
      }
    }
  }, []);

  // Save theme to localStorage when it changes
  useEffect(() => {
    storage.saveTheme(state.theme);
    document.documentElement.setAttribute('data-theme', state.theme);
  }, [state.theme]);

  // Handle online/offline status
  useEffect(() => {
    const handleOnline = () => dispatch({ type: 'SET_ONLINE_STATUS', payload: true });
    const handleOffline = () => dispatch({ type: 'SET_ONLINE_STATUS', payload: false });

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Handle viewport changes
  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      const height = window.innerHeight;
      
      dispatch({ 
        type: 'SET_VIEWPORT', 
        payload: {
          width,
          height,
          isMobile: width < 768,
          isTablet: width >= 768 && width < 1024,
          isDesktop: width >= 1024
        }
      });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Auto-clear notifications
  useEffect(() => {
    if (state.notification && state.notification.autoClose !== false) {
      const timer = setTimeout(() => {
        dispatch({ type: 'CLEAR_NOTIFICATION' });
      }, state.notification.duration || 5000);

      return () => clearTimeout(timer);
    }
  }, [state.notification]);

  const toggleTheme = () => {
    const newTheme = state.theme === 'light' ? 'dark' : 'light';
    dispatch({ type: 'SET_THEME', payload: newTheme });
  };

  const toggleSidebar = () => {
    dispatch({ type: 'SET_SIDEBAR_OPEN', payload: !state.sidebarOpen });
  };

  const openSidebar = () => {
    dispatch({ type: 'SET_SIDEBAR_OPEN', payload: true });
  };

  const closeSidebar = () => {
    dispatch({ type: 'SET_SIDEBAR_OPEN', payload: false });
  };

  const openModal = (content) => {
    dispatch({ type: 'SET_MODAL_CONTENT', payload: content });
    dispatch({ type: 'SET_MODAL_OPEN', payload: true });
  };

  const closeModal = () => {
    dispatch({ type: 'SET_MODAL_OPEN', payload: false });
  };

  const showNotification = (message, type = 'info', options = {}) => {
    dispatch({ 
      type: 'SET_NOTIFICATION', 
      payload: {
        message,
        type,
        ...options
      }
    });
  };

  const clearNotification = () => {
    dispatch({ type: 'CLEAR_NOTIFICATION' });
  };

  const setGlobalLoading = (loading) => {
    dispatch({ type: 'SET_LOADING', payload: loading });
  };

  const login = async (userData, token) => {
    try {
      // Store token in localStorage
      if (token) {
        localStorage.setItem('authToken', token);
      }
      
      // Store user data in localStorage
      localStorage.setItem('userData', JSON.stringify(userData));
      
      // Update context state
      dispatch({ type: 'SET_USER', payload: userData });
      
      showNotification('Login successful!', 'success');
      return userData;
    } catch (error) {
      showNotification('Login failed. Please try again.', 'error');
      throw error;
    }
  };

  const logout = () => {
    try {
      // Clear localStorage
      localStorage.removeItem('authToken');
      localStorage.removeItem('userData');
      
      // Update context state
      dispatch({ type: 'LOGOUT' });
      
      showNotification('Logged out successfully', 'info');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const value = {
    ...state,
    toggleTheme,
    toggleSidebar,
    openSidebar,
    closeSidebar,
    openModal,
    closeModal,
    showNotification,
    clearNotification,
    setGlobalLoading,
    login,
    logout
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};

export default AppContext;