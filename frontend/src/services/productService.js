import { api } from './api';

// Mock product data for fallback
const mockProducts = [
  {
    id: 1,
    name: 'Wireless Bluetooth Headphones',
    description: 'Premium quality wireless headphones with noise cancellation and 30-hour battery life.',
    price: 199.99,
    originalPrice: 249.99,
    category_id: 1,
    category: 'Electronics',
    image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&h=500&fit=crop',
    images: [
      'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&h=500&fit=crop',
      'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=500&h=500&fit=crop'
    ],
    rating: 4.5,
    reviewCount: 128,
    inStock: true,
    stockQuantity: 25,
    featured: true,
    colors: ['Black', 'White', 'Blue'],
    sizes: [],
    specifications: {
      'Battery Life': '30 hours',
      'Connectivity': 'Bluetooth 5.0',
      'Weight': '250g'
    }
  },
  {
    id: 2,
    name: 'Smart Fitness Watch',
    description: 'Advanced fitness tracking with heart rate monitor, GPS, and waterproof design.',
    price: 299.99,
    originalPrice: 349.99,
    category_id: 1,
    category: 'Electronics',
    image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop',
    images: [
      'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop',
      'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=500&h=500&fit=crop'
    ],
    rating: 4.7,
    reviewCount: 89,
    inStock: true,
    stockQuantity: 15,
    featured: true,
    colors: ['Black', 'Silver', 'Rose Gold'],
    sizes: ['Small', 'Medium', 'Large'],
    specifications: {
      'Display': '1.4" AMOLED',
      'Battery': '7 days',
      'Water Resistance': '50m'
    }
  },
  {
    id: 3,
    name: 'Organic Cotton T-Shirt',
    description: 'Comfortable and sustainable organic cotton t-shirt in various colors.',
    price: 29.99,
    originalPrice: 39.99,
    category_id: 2,
    category: 'Clothing',
    image: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop',
    images: [
      'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop',
      'https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=500&h=500&fit=crop'
    ],
    rating: 4.3,
    reviewCount: 156,
    inStock: true,
    stockQuantity: 50,
    featured: false,
    colors: ['White', 'Black', 'Navy', 'Gray'],
    sizes: ['XS', 'S', 'M', 'L', 'XL'],
    specifications: {
      'Material': '100% Organic Cotton',
      'Fit': 'Regular',
      'Care': 'Machine wash cold'
    }
  },
  {
    id: 4,
    name: 'Professional Camera Lens',
    description: '85mm f/1.4 portrait lens with exceptional image quality and beautiful bokeh.',
    price: 899.99,
    originalPrice: 999.99,
    category_id: 1,
    category: 'Electronics',
    image: 'https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=500&h=500&fit=crop',
    images: [
      'https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=500&h=500&fit=crop',
      'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=500&h=500&fit=crop'
    ],
    rating: 4.8,
    reviewCount: 67,
    inStock: true,
    stockQuantity: 8,
    featured: true,
    colors: ['Black'],
    sizes: [],
    specifications: {
      'Focal Length': '85mm',
      'Aperture': 'f/1.4',
      'Mount': 'Canon EF'
    }
  },
  {
    id: 5,
    name: 'Ergonomic Office Chair',
    description: 'Premium ergonomic office chair with lumbar support and adjustable height.',
    price: 449.99,
    originalPrice: 549.99,
    category_id: 3,
    category: 'Furniture',
    image: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500&h=500&fit=crop',
    images: [
      'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500&h=500&fit=crop',
      'https://images.unsplash.com/photo-1541558869434-2840d308329a?w=500&h=500&fit=crop'
    ],
    rating: 4.6,
    reviewCount: 234,
    inStock: true,
    stockQuantity: 12,
    featured: false,
    colors: ['Black', 'Gray', 'White'],
    sizes: [],
    specifications: {
      'Material': 'Mesh and Fabric',
      'Weight Capacity': '300 lbs',
      'Warranty': '5 years'
    }
  },
  {
    id: 6,
    name: 'Stainless Steel Water Bottle',
    description: 'Insulated stainless steel water bottle that keeps drinks cold for 24 hours.',
    price: 34.99,
    originalPrice: 44.99,
    category_id: 4,
    category: 'Sports',
    image: 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500&h=500&fit=crop',
    images: [
      'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500&h=500&fit=crop',
      'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop'
    ],
    rating: 4.4,
    reviewCount: 312,
    inStock: true,
    stockQuantity: 75,
    featured: true,
    colors: ['Silver', 'Black', 'Blue', 'Pink'],
    sizes: ['16oz', '20oz', '32oz'],
    specifications: {
      'Material': 'Stainless Steel',
      'Insulation': 'Double Wall',
      'Capacity': '20oz'
    }
  }
];

class ProductService {
  // Get all products with optional filtering and pagination
  async getProducts(params = {}) {
    try {
      const response = await api.get('/products', params);
      return response;
    } catch (error) {
      console.warn('API not available, using mock data:', error.message);
      // Return mock data with pagination
      const { page = 1, limit = 12 } = params;
      const startIndex = (page - 1) * limit;
      const endIndex = startIndex + limit;
      const paginatedProducts = mockProducts.slice(startIndex, endIndex);
      
      return {
        products: paginatedProducts,
        totalItems: mockProducts.length,
        totalPages: Math.ceil(mockProducts.length / limit),
        currentPage: page
      };
    }
  }

  // Get a single product by ID
  async getProductById(id) {
    try {
      const response = await api.get(`/products/${id}`);
      return response;
    } catch (error) {
      console.warn(`API not available, using mock data for product ${id}:`, error.message);
      const product = mockProducts.find(p => p.id === parseInt(id));
      if (product) {
        return product;
      }
      throw new Error(`Product with id ${id} not found`);
    }
  }

  // Search products
  async searchProducts(query, params = {}) {
    try {
      const searchParams = {
        search: query,
        ...params
      };
      const response = await api.get('/products/search', searchParams);
      return response;
    } catch (error) {
      console.warn('API not available, using mock search results:', error.message);
      const filteredProducts = mockProducts.filter(product => 
        product.name.toLowerCase().includes(query.toLowerCase()) ||
        product.description.toLowerCase().includes(query.toLowerCase()) ||
        product.category.toLowerCase().includes(query.toLowerCase())
      );
      const { page = 1, limit = 12 } = params;
      const startIndex = (page - 1) * limit;
      const endIndex = startIndex + limit;
      const paginatedProducts = filteredProducts.slice(startIndex, endIndex);
      
      return {
        products: paginatedProducts,
        totalItems: filteredProducts.length,
        totalPages: Math.ceil(filteredProducts.length / limit),
        currentPage: page
      };
    }
  }

  // Get products by category
  async getProductsByCategory(categoryId, params = {}) {
    try {
      const response = await api.get(`/products/category/${categoryId}`, params);
      return response;
    } catch (error) {
      console.warn(`API not available, using mock data for category ${categoryId}:`, error.message);
      const categoryProducts = mockProducts.filter(p => p.categoryId === parseInt(categoryId));
      const { page = 1, limit = 12 } = params;
      const startIndex = (page - 1) * limit;
      const endIndex = startIndex + limit;
      const paginatedProducts = categoryProducts.slice(startIndex, endIndex);
      
      return {
        products: paginatedProducts,
        totalItems: categoryProducts.length,
        totalPages: Math.ceil(categoryProducts.length / limit),
        currentPage: page
      };
    }
  }

  // Get featured products
  async getFeaturedProducts(limit = 8) {
    try {
      const response = await api.get('/products/featured', { limit });
      return response;
    } catch (error) {
      console.warn('API not available, using mock featured products:', error.message);
      const featuredProducts = mockProducts.filter(p => p.featured).slice(0, limit);
      return {
        products: featuredProducts,
        totalItems: featuredProducts.length
      };
    }
  }

  // Get related products
  async getRelatedProducts(productId, limit = 4) {
    try {
      const response = await api.get(`/products/${productId}/related`, { limit });
      return response;
    } catch (error) {
      console.warn(`API not available, using mock related products for ${productId}:`, error.message);
      const product = mockProducts.find(p => p.id === parseInt(productId));
      if (product) {
        const relatedProducts = mockProducts
          .filter(p => p.id !== parseInt(productId) && p.categoryId === product.categoryId)
          .slice(0, limit);
        return {
          products: relatedProducts,
          totalItems: relatedProducts.length
        };
      }
      return { products: [], totalItems: 0 };
    }
  }

  // Get product reviews
  async getProductReviews(productId, params = {}) {
    try {
      const response = await api.get(`/products/${productId}/reviews`, params);
      return response;
    } catch (error) {
      console.warn(`API not available, using mock reviews for product ${productId}:`, error.message);
      // Mock reviews data
      const mockReviews = [
        {
          id: 1,
          userId: 1,
          userName: 'John Doe',
          rating: 5,
          comment: 'Excellent product! Highly recommended.',
          date: '2024-01-15',
          verified: true
        },
        {
          id: 2,
          userId: 2,
          userName: 'Jane Smith',
          rating: 4,
          comment: 'Good quality, fast shipping.',
          date: '2024-01-10',
          verified: true
        }
      ];
      const { page = 1, limit = 10 } = params;
      const startIndex = (page - 1) * limit;
      const endIndex = startIndex + limit;
      const paginatedReviews = mockReviews.slice(startIndex, endIndex);
      
      return {
        reviews: paginatedReviews,
        totalItems: mockReviews.length,
        totalPages: Math.ceil(mockReviews.length / limit),
        currentPage: page,
        averageRating: 4.5
      };
    }
  }

  // Add product review
  async addProductReview(productId, reviewData) {
    try {
      const response = await api.post(`/products/${productId}/reviews`, reviewData);
      return response;
    } catch (error) {
      console.error(`Error adding review for product ${productId}:`, error);
      throw error;
    }
  }

  // Get product availability
  async getProductAvailability(productId) {
    try {
      const response = await api.get(`/products/${productId}/availability`);
      return response;
    } catch (error) {
      console.warn(`API not available, using mock availability for product ${productId}:`, error.message);
      const product = mockProducts.find(p => p.id === parseInt(productId));
      if (product) {
        return {
          available: product.stock > 0,
          stock: product.stock,
          estimatedDelivery: '2-3 business days'
        };
      }
      return { available: false, stock: 0, estimatedDelivery: null };
    }
  }

  // Check multiple products availability
  async checkProductsAvailability(productIds) {
    try {
      const response = await api.post('/products/check-availability', {
        product_ids: productIds
      });
      return response;
    } catch (error) {
      console.error('Error checking products availability:', error);
      throw error;
    }
  }

  // Get product price history
  async getProductPriceHistory(productId, days = 30) {
    try {
      const response = await api.get(`/products/${productId}/price-history`, { days });
      return response;
    } catch (error) {
      console.error(`Error fetching price history for product ${productId}:`, error);
      throw error;
    }
  }

  // Get product variants
  async getProductVariants(productId) {
    try {
      const response = await api.get(`/products/${productId}/variants`);
      return response;
    } catch (error) {
      console.error(`Error fetching variants for product ${productId}:`, error);
      throw error;
    }
  }

  // Get product specifications
  async getProductSpecifications(productId) {
    try {
      const response = await api.get(`/products/${productId}/specifications`);
      return response;
    } catch (error) {
      console.error(`Error fetching specifications for product ${productId}:`, error);
      throw error;
    }
  }

  // Get product images
  async getProductImages(productId) {
    try {
      const response = await api.get(`/products/${productId}/images`);
      return response;
    } catch (error) {
      console.error(`Error fetching images for product ${productId}:`, error);
      throw error;
    }
  }

  // Get product filters (for filter sidebar)
  async getProductFilters() {
    try {
      const response = await api.get('/products/filters');
      return response;
    } catch (error) {
      console.warn('API not available, using mock product filters:', error.message);
      return {
        categories: [
          { id: 1, name: 'Electronics', count: 15 },
          { id: 2, name: 'Clothing', count: 25 },
          { id: 3, name: 'Home & Garden', count: 18 },
          { id: 4, name: 'Sports', count: 12 }
        ],
        brands: [
          { id: 1, name: 'TechBrand', count: 8 },
          { id: 2, name: 'FashionCo', count: 15 },
          { id: 3, name: 'HomePlus', count: 10 }
        ],
        priceRanges: [
          { min: 0, max: 50, count: 20 },
          { min: 50, max: 100, count: 25 },
          { min: 100, max: 200, count: 15 },
          { min: 200, max: null, count: 10 }
        ],
        colors: [
          { name: 'Black', hex: '#000000', count: 12 },
          { name: 'White', hex: '#FFFFFF', count: 10 },
          { name: 'Blue', hex: '#0066CC', count: 8 },
          { name: 'Red', hex: '#CC0000', count: 6 }
        ],
        sizes: [
          { name: 'XS', count: 5 },
          { name: 'S', count: 8 },
          { name: 'M', count: 12 },
          { name: 'L', count: 10 },
          { name: 'XL', count: 6 }
        ]
      };
    }
  }

  // Get price range for products
  async getPriceRange(categoryId = null) {
    try {
      const params = categoryId ? { category_id: categoryId } : {};
      const response = await api.get('/products/price-range', params);
      return response;
    } catch (error) {
      console.warn('API not available, using mock price range:', error.message);
      const relevantProducts = categoryId 
        ? mockProducts.filter(p => p.categoryId === parseInt(categoryId))
        : mockProducts;
      
      if (relevantProducts.length === 0) {
        return { min: 0, max: 0 };
      }
      
      const prices = relevantProducts.map(p => p.price);
      return {
        min: Math.min(...prices),
        max: Math.max(...prices)
      };
    }
  }
}

// Create and export a singleton instance
export const productService = new ProductService();
export default productService;