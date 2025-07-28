import { api } from './api';

class CategoryService {
  // Get all categories
  async getCategories(params = {}) {
    try {
      const response = await api.get('/categories', params);
      return response;
    } catch (error) {
      console.error('Error fetching categories:', error);
      throw error;
    }
  }

  // Get category by ID
  async getCategoryById(id) {
    try {
      const response = await api.get(`/categories/${id}`);
      return response;
    } catch (error) {
      console.error(`Error fetching category ${id}:`, error);
      throw error;
    }
  }

  // Get category tree (hierarchical structure)
  async getCategoryTree() {
    try {
      const response = await api.get('/categories/tree');
      return response;
    } catch (error) {
      console.error('Error fetching category tree:', error);
      throw error;
    }
  }

  // Get top-level categories
  async getTopLevelCategories() {
    try {
      const response = await api.get('/categories/top-level');
      return response;
    } catch (error) {
      console.error('Error fetching top-level categories:', error);
      throw error;
    }
  }

  // Get subcategories of a parent category
  async getSubcategories(parentId) {
    try {
      const response = await api.get(`/categories/${parentId}/subcategories`);
      return response;
    } catch (error) {
      console.error(`Error fetching subcategories for ${parentId}:`, error);
      throw error;
    }
  }

  // Get category breadcrumb path
  async getCategoryBreadcrumb(categoryId) {
    try {
      const response = await api.get(`/categories/${categoryId}/breadcrumb`);
      return response;
    } catch (error) {
      console.error(`Error fetching breadcrumb for category ${categoryId}:`, error);
      throw error;
    }
  }

  // Get featured categories
  async getFeaturedCategories(limit = 6) {
    try {
      const response = await api.get('/categories/featured', { limit });
      return response;
    } catch (error) {
      console.error('Error fetching featured categories:', error);
      throw error;
    }
  }

  // Search categories
  async searchCategories(query) {
    try {
      const response = await api.get('/categories/search', { q: query });
      return response;
    } catch (error) {
      console.error('Error searching categories:', error);
      throw error;
    }
  }

  // Get category statistics
  async getCategoryStats(categoryId) {
    try {
      const response = await api.get(`/categories/${categoryId}/stats`);
      return response;
    } catch (error) {
      console.error(`Error fetching stats for category ${categoryId}:`, error);
      throw error;
    }
  }

  // Get categories with product counts
  async getCategoriesWithCounts() {
    try {
      const response = await api.get('/categories/with-counts');
      return response;
    } catch (error) {
      console.error('Error fetching categories with counts:', error);
      throw error;
    }
  }

  // Get category filters (attributes that can be used for filtering)
  async getCategoryFilters(categoryId) {
    try {
      const response = await api.get(`/categories/${categoryId}/filters`);
      return response;
    } catch (error) {
      console.error(`Error fetching filters for category ${categoryId}:`, error);
      throw error;
    }
  }

  // Get category brands
  async getCategoryBrands(categoryId) {
    try {
      const response = await api.get(`/categories/${categoryId}/brands`);
      return response;
    } catch (error) {
      console.error(`Error fetching brands for category ${categoryId}:`, error);
      throw error;
    }
  }

  // Get category price range
  async getCategoryPriceRange(categoryId) {
    try {
      const response = await api.get(`/categories/${categoryId}/price-range`);
      return response;
    } catch (error) {
      console.error(`Error fetching price range for category ${categoryId}:`, error);
      throw error;
    }
  }

  // Get popular categories
  async getPopularCategories(limit = 10) {
    try {
      const response = await api.get('/categories/popular', { limit });
      return response;
    } catch (error) {
      console.error('Error fetching popular categories:', error);
      throw error;
    }
  }

  // Get category recommendations based on user behavior
  async getCategoryRecommendations(limit = 5) {
    try {
      const response = await api.get('/categories/recommendations', { limit });
      return response;
    } catch (error) {
      console.error('Error fetching category recommendations:', error);
      throw error;
    }
  }

  // Get category image/banner
  async getCategoryImage(categoryId) {
    try {
      const response = await api.get(`/categories/${categoryId}/image`);
      return response;
    } catch (error) {
      console.error(`Error fetching image for category ${categoryId}:`, error);
      throw error;
    }
  }

  // Get category SEO data
  async getCategorySEO(categoryId) {
    try {
      const response = await api.get(`/categories/${categoryId}/seo`);
      return response;
    } catch (error) {
      console.error(`Error fetching SEO data for category ${categoryId}:`, error);
      throw error;
    }
  }
}

// Create and export a singleton instance
export const categoryService = new CategoryService();
export default categoryService;