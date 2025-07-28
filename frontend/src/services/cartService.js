import { api } from './api';

class CartService {
  // Get current user's cart
  async getCart() {
    try {
      const response = await api.get('/cart');
      return response;
    } catch (error) {
      console.error('Error fetching cart:', error);
      throw error;
    }
  }

  // Add item to cart
  async addItem(productId, quantity = 1, options = {}) {
    try {
      const response = await api.post('/cart/items', {
        product_id: productId,
        quantity,
        ...options
      });
      return response;
    } catch (error) {
      console.error('Error adding item to cart:', error);
      throw error;
    }
  }

  // Update cart item quantity
  async updateItem(itemId, quantity) {
    try {
      const response = await api.put(`/cart/items/${itemId}`, {
        quantity
      });
      return response;
    } catch (error) {
      console.error('Error updating cart item:', error);
      throw error;
    }
  }

  // Remove item from cart
  async removeItem(itemId) {
    try {
      const response = await api.delete(`/cart/items/${itemId}`);
      return response;
    } catch (error) {
      console.error('Error removing cart item:', error);
      throw error;
    }
  }

  // Clear entire cart
  async clearCart() {
    try {
      const response = await api.delete('/cart');
      return response;
    } catch (error) {
      console.error('Error clearing cart:', error);
      throw error;
    }
  }

  // Get cart summary (totals, counts, etc.)
  async getCartSummary() {
    try {
      const response = await api.get('/cart/summary');
      return response;
    } catch (error) {
      console.error('Error fetching cart summary:', error);
      throw error;
    }
  }

  // Apply coupon code
  async applyCoupon(couponCode) {
    try {
      const response = await api.post('/cart/coupon', {
        coupon_code: couponCode
      });
      return response;
    } catch (error) {
      console.error('Error applying coupon:', error);
      throw error;
    }
  }

  // Remove coupon
  async removeCoupon() {
    try {
      const response = await api.delete('/cart/coupon');
      return response;
    } catch (error) {
      console.error('Error removing coupon:', error);
      throw error;
    }
  }

  // Calculate shipping costs
  async calculateShipping(shippingAddress) {
    try {
      const response = await api.post('/cart/shipping', shippingAddress);
      return response;
    } catch (error) {
      console.error('Error calculating shipping:', error);
      throw error;
    }
  }

  // Get available shipping methods
  async getShippingMethods(shippingAddress = null) {
    try {
      const response = await api.post('/cart/shipping-methods', shippingAddress || {});
      return response;
    } catch (error) {
      console.error('Error fetching shipping methods:', error);
      throw error;
    }
  }

  // Validate cart before checkout
  async validateCart() {
    try {
      const response = await api.post('/cart/validate');
      return response;
    } catch (error) {
      console.error('Error validating cart:', error);
      throw error;
    }
  }

  // Get cart taxes
  async calculateTaxes(billingAddress) {
    try {
      const response = await api.post('/cart/taxes', billingAddress);
      return response;
    } catch (error) {
      console.error('Error calculating taxes:', error);
      throw error;
    }
  }

  // Save cart for later (wishlist functionality)
  async saveForLater(itemId) {
    try {
      const response = await api.post(`/cart/items/${itemId}/save-for-later`);
      return response;
    } catch (error) {
      console.error('Error saving item for later:', error);
      throw error;
    }
  }

  // Move item from saved to cart
  async moveToCart(savedItemId) {
    try {
      const response = await api.post(`/cart/saved-items/${savedItemId}/move-to-cart`);
      return response;
    } catch (error) {
      console.error('Error moving item to cart:', error);
      throw error;
    }
  }

  // Get saved items
  async getSavedItems() {
    try {
      const response = await api.get('/cart/saved-items');
      return response;
    } catch (error) {
      console.error('Error fetching saved items:', error);
      throw error;
    }
  }

  // Merge guest cart with user cart (after login)
  async mergeCart(guestCartData) {
    try {
      const response = await api.post('/cart/merge', {
        guest_cart: guestCartData
      });
      return response;
    } catch (error) {
      console.error('Error merging cart:', error);
      throw error;
    }
  }

  // Get cart recommendations
  async getCartRecommendations() {
    try {
      const response = await api.get('/cart/recommendations');
      return response;
    } catch (error) {
      console.error('Error fetching cart recommendations:', error);
      throw error;
    }
  }

  // Check item availability in cart
  async checkItemsAvailability() {
    try {
      const response = await api.get('/cart/check-availability');
      return response;
    } catch (error) {
      console.error('Error checking cart items availability:', error);
      throw error;
    }
  }

  // Update multiple cart items at once
  async updateMultipleItems(updates) {
    try {
      const response = await api.put('/cart/items/bulk', {
        updates
      });
      return response;
    } catch (error) {
      console.error('Error updating multiple cart items:', error);
      throw error;
    }
  }

  // Get cart history
  async getCartHistory(limit = 10) {
    try {
      const response = await api.get('/cart/history', { limit });
      return response;
    } catch (error) {
      console.error('Error fetching cart history:', error);
      throw error;
    }
  }
}

// Create and export a singleton instance
export const cartService = new CartService();
export default cartService;