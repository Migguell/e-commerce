// Local storage utility functions

export const storage = {
  // Get item from localStorage
  getItem: (key) => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : null;
    } catch (error) {
      console.error(`Error getting item from localStorage:`, error);
      return null;
    }
  },

  // Set item in localStorage
  setItem: (key, value) => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (error) {
      console.error(`Error setting item in localStorage:`, error);
      return false;
    }
  },

  // Remove item from localStorage
  removeItem: (key) => {
    try {
      localStorage.removeItem(key);
      return true;
    } catch (error) {
      console.error(`Error removing item from localStorage:`, error);
      return false;
    }
  },

  // Clear all localStorage
  clear: () => {
    try {
      localStorage.clear();
      return true;
    } catch (error) {
      console.error(`Error clearing localStorage:`, error);
      return false;
    }
  },

  // Check if key exists in localStorage
  hasItem: (key) => {
    return localStorage.getItem(key) !== null;
  },

  // Theme-specific methods
  getTheme: () => {
    try {
      return localStorage.getItem('theme');
    } catch (error) {
      console.error('Error getting theme from localStorage:', error);
      return null;
    }
  },

  saveTheme: (theme) => {
    try {
      localStorage.setItem('theme', theme);
      return true;
    } catch (error) {
      console.error('Error saving theme to localStorage:', error);
      return false;
    }
  },

  // Cart-specific methods
  getCart: () => {
    try {
      const cart = localStorage.getItem('cart');
      return cart ? JSON.parse(cart) : [];
    } catch (error) {
      console.error('Error getting cart from localStorage:', error);
      return [];
    }
  },

  saveCart: (cartItems) => {
    try {
      localStorage.setItem('cart', JSON.stringify(cartItems));
      return true;
    } catch (error) {
      console.error('Error saving cart to localStorage:', error);
      return false;
    }
  }
};

export default storage;