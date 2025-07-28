import { api } from './api';

class UserService {
  // Authentication methods
  async login(credentials) {
    try {
      const response = await api.post('/auth/login', credentials);
      if (response.token) {
        localStorage.setItem('authToken', response.token);
        api.setAuthToken(response.token);
      }
      return response;
    } catch (error) {
      console.error('Error during login:', error);
      throw error;
    }
  }

  async register(userData) {
    try {
      const response = await api.post('/auth/register', userData);
      if (response.token) {
        localStorage.setItem('authToken', response.token);
        api.setAuthToken(response.token);
      }
      return response;
    } catch (error) {
      console.error('Error during registration:', error);
      throw error;
    }
  }

  async logout() {
    try {
      await api.post('/auth/logout');
      localStorage.removeItem('authToken');
      api.setAuthToken(null);
      return true;
    } catch (error) {
      console.error('Error during logout:', error);
      // Still remove token locally even if server request fails
      localStorage.removeItem('authToken');
      api.setAuthToken(null);
      throw error;
    }
  }

  async refreshToken() {
    try {
      const response = await api.post('/auth/refresh');
      if (response.token) {
        localStorage.setItem('authToken', response.token);
        api.setAuthToken(response.token);
      }
      return response;
    } catch (error) {
      console.error('Error refreshing token:', error);
      throw error;
    }
  }

  async forgotPassword(email) {
    try {
      const response = await api.post('/auth/forgot-password', { email });
      return response;
    } catch (error) {
      console.error('Error sending password reset:', error);
      throw error;
    }
  }

  async resetPassword(token, newPassword) {
    try {
      const response = await api.post('/auth/reset-password', {
        token,
        password: newPassword
      });
      return response;
    } catch (error) {
      console.error('Error resetting password:', error);
      throw error;
    }
  }

  async verifyEmail(token) {
    try {
      const response = await api.post('/auth/verify-email', { token });
      return response;
    } catch (error) {
      console.error('Error verifying email:', error);
      throw error;
    }
  }

  async resendVerification(email) {
    try {
      const response = await api.post('/auth/resend-verification', { email });
      return response;
    } catch (error) {
      console.error('Error resending verification:', error);
      throw error;
    }
  }

  // Profile management
  async getProfile() {
    try {
      const response = await api.get('/user/profile');
      return response;
    } catch (error) {
      console.error('Error fetching profile:', error);
      throw error;
    }
  }

  async updateProfile(profileData) {
    try {
      const response = await api.put('/user/profile', profileData);
      return response;
    } catch (error) {
      console.error('Error updating profile:', error);
      throw error;
    }
  }

  async changePassword(currentPassword, newPassword) {
    try {
      const response = await api.put('/user/change-password', {
        current_password: currentPassword,
        new_password: newPassword
      });
      return response;
    } catch (error) {
      console.error('Error changing password:', error);
      throw error;
    }
  }

  async uploadAvatar(file) {
    try {
      const response = await api.uploadFile('/user/avatar', file);
      return response;
    } catch (error) {
      console.error('Error uploading avatar:', error);
      throw error;
    }
  }

  async deleteAvatar() {
    try {
      const response = await api.delete('/user/avatar');
      return response;
    } catch (error) {
      console.error('Error deleting avatar:', error);
      throw error;
    }
  }

  // Address management
  async getAddresses() {
    try {
      const response = await api.get('/user/addresses');
      return response;
    } catch (error) {
      console.error('Error fetching addresses:', error);
      throw error;
    }
  }

  async addAddress(addressData) {
    try {
      const response = await api.post('/user/addresses', addressData);
      return response;
    } catch (error) {
      console.error('Error adding address:', error);
      throw error;
    }
  }

  async updateAddress(addressId, addressData) {
    try {
      const response = await api.put(`/user/addresses/${addressId}`, addressData);
      return response;
    } catch (error) {
      console.error('Error updating address:', error);
      throw error;
    }
  }

  async deleteAddress(addressId) {
    try {
      const response = await api.delete(`/user/addresses/${addressId}`);
      return response;
    } catch (error) {
      console.error('Error deleting address:', error);
      throw error;
    }
  }

  async setDefaultAddress(addressId) {
    try {
      const response = await api.put(`/user/addresses/${addressId}/set-default`);
      return response;
    } catch (error) {
      console.error('Error setting default address:', error);
      throw error;
    }
  }

  // Order history
  async getOrders(params = {}) {
    try {
      const response = await api.get('/user/orders', params);
      return response;
    } catch (error) {
      console.error('Error fetching orders:', error);
      throw error;
    }
  }

  async getOrderById(orderId) {
    try {
      const response = await api.get(`/user/orders/${orderId}`);
      return response;
    } catch (error) {
      console.error(`Error fetching order ${orderId}:`, error);
      throw error;
    }
  }

  async cancelOrder(orderId, reason = '') {
    try {
      const response = await api.post(`/user/orders/${orderId}/cancel`, { reason });
      return response;
    } catch (error) {
      console.error(`Error canceling order ${orderId}:`, error);
      throw error;
    }
  }

  async trackOrder(orderId) {
    try {
      const response = await api.get(`/user/orders/${orderId}/tracking`);
      return response;
    } catch (error) {
      console.error(`Error tracking order ${orderId}:`, error);
      throw error;
    }
  }

  // Wishlist management
  async getWishlist() {
    try {
      const response = await api.get('/user/wishlist');
      return response;
    } catch (error) {
      console.error('Error fetching wishlist:', error);
      throw error;
    }
  }

  async addToWishlist(productId) {
    try {
      const response = await api.post('/user/wishlist', { product_id: productId });
      return response;
    } catch (error) {
      console.error('Error adding to wishlist:', error);
      throw error;
    }
  }

  async removeFromWishlist(productId) {
    try {
      const response = await api.delete(`/user/wishlist/${productId}`);
      return response;
    } catch (error) {
      console.error('Error removing from wishlist:', error);
      throw error;
    }
  }

  // Preferences and settings
  async getPreferences() {
    try {
      const response = await api.get('/user/preferences');
      return response;
    } catch (error) {
      console.error('Error fetching preferences:', error);
      throw error;
    }
  }

  async updatePreferences(preferences) {
    try {
      const response = await api.put('/user/preferences', preferences);
      return response;
    } catch (error) {
      console.error('Error updating preferences:', error);
      throw error;
    }
  }

  async getNotificationSettings() {
    try {
      const response = await api.get('/user/notification-settings');
      return response;
    } catch (error) {
      console.error('Error fetching notification settings:', error);
      throw error;
    }
  }

  async updateNotificationSettings(settings) {
    try {
      const response = await api.put('/user/notification-settings', settings);
      return response;
    } catch (error) {
      console.error('Error updating notification settings:', error);
      throw error;
    }
  }

  // Account management
  async deleteAccount(password) {
    try {
      const response = await api.delete('/user/account', { password });
      localStorage.removeItem('authToken');
      api.setAuthToken(null);
      return response;
    } catch (error) {
      console.error('Error deleting account:', error);
      throw error;
    }
  }

  async exportData() {
    try {
      const response = await api.get('/user/export-data');
      return response;
    } catch (error) {
      console.error('Error exporting user data:', error);
      throw error;
    }
  }

  // Utility methods
  isAuthenticated() {
    return !!localStorage.getItem('authToken');
  }

  getAuthToken() {
    return localStorage.getItem('authToken');
  }

  // Initialize auth token on service creation
  initializeAuth() {
    const token = this.getAuthToken();
    if (token) {
      api.setAuthToken(token);
    }
  }
}

// Create and export a singleton instance
export const userService = new UserService();

// Initialize auth on import
userService.initializeAuth();

export default userService;