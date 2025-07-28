import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useProducts } from '../../context/ProductContext';
import { productService } from '../../services/productService';
import './HomePage.css';

const HomePage = () => {
  const { state, dispatch } = useProducts();
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadFeaturedProducts = async () => {
      try {
        setLoading(true);
        // Try to load featured products from API
        const response = await productService.getFeaturedProducts();
        // Handle both API response structure and direct array
        const products = response.products || response;
        setFeaturedProducts(products.slice(0, 6)); // Show only 6 featured products
      } catch (error) {
        console.error('Failed to load featured products:', error);
        // Fallback to mock data if API fails
        setFeaturedProducts(getMockProducts());
      } finally {
        setLoading(false);
      }
    };

    loadFeaturedProducts();
  }, []);

  const getMockProducts = () => [
    {
      id: 1,
      name: 'Wireless Headphones',
      price: 99.99,
      image: 'https://via.placeholder.com/300x300?text=Headphones',
      rating: 4.5
    },
    {
      id: 2,
      name: 'Smart Watch',
      price: 199.99,
      image: 'https://via.placeholder.com/300x300?text=Smart+Watch',
      rating: 4.8
    },
    {
      id: 3,
      name: 'Laptop Backpack',
      price: 49.99,
      image: 'https://via.placeholder.com/300x300?text=Backpack',
      rating: 4.3
    },
    {
      id: 4,
      name: 'Bluetooth Speaker',
      price: 79.99,
      image: 'https://via.placeholder.com/300x300?text=Speaker',
      rating: 4.6
    },
    {
      id: 5,
      name: 'Smartphone Case',
      price: 24.99,
      image: 'https://via.placeholder.com/300x300?text=Phone+Case',
      rating: 4.2
    },
    {
      id: 6,
      name: 'Wireless Charger',
      price: 39.99,
      image: 'https://via.placeholder.com/300x300?text=Charger',
      rating: 4.4
    }
  ];

  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(
        <span key={i} className="star filled">★</span>
      );
    }

    if (hasHalfStar) {
      stars.push(
        <span key="half" className="star half">★</span>
      );
    }

    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(
        <span key={`empty-${i}`} className="star empty">★</span>
      );
    }

    return stars;
  };

  return (
    <div className="homepage">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">Welcome to E-Shop</h1>
          <p className="hero-subtitle">
            Discover amazing products at unbeatable prices. Shop with confidence and enjoy fast, secure delivery.
          </p>
          <div className="hero-actions">
            <Link to="/products" className="btn btn-primary">
              Shop Now
            </Link>
            <Link to="/products?featured=true" className="btn btn-secondary">
              View Featured
            </Link>
          </div>
        </div>
        <div className="hero-image">
          <img 
            src="https://via.placeholder.com/600x400?text=E-Commerce+Hero" 
            alt="E-commerce hero"
            onError={(e) => {
              e.target.src = 'https://via.placeholder.com/600x400?text=E-Commerce+Hero';
            }}
          />
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <div className="container">
          <h2 className="section-title">Why Choose E-Shop?</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🚚</div>
              <h3>Fast Delivery</h3>
              <p>Free shipping on orders over $50. Get your products delivered quickly and safely.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔒</div>
              <h3>Secure Payment</h3>
              <p>Your payment information is protected with industry-standard encryption.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">↩️</div>
              <h3>Easy Returns</h3>
              <p>Not satisfied? Return your purchase within 30 days for a full refund.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🎧</div>
              <h3>24/7 Support</h3>
              <p>Our customer service team is here to help you anytime, anywhere.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Products Section */}
      <section className="featured-products">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">Featured Products</h2>
            <Link to="/products" className="view-all-link">
              View All Products →
            </Link>
          </div>
          
          {loading ? (
            <div className="loading">
              <div className="spinner"></div>
              <p>Loading featured products...</p>
            </div>
          ) : (
            <div className="products-grid">
              {featuredProducts.map((product) => (
                <div key={product.id} className="product-card">
                  <Link to={`/products/${product.id}`} className="product-link">
                    <div className="product-image">
                      <img 
                        src={product.image_url || product.image || 'https://via.placeholder.com/300x300?text=No+Image'} 
                        alt={product.name}
                        onError={(e) => {
                          e.target.src = 'https://via.placeholder.com/300x300?text=No+Image';
                        }}
                      />
                    </div>
                    <div className="product-info">
                      <h3 className="product-name">{product.name}</h3>
                      <div className="product-rating">
                        {renderStars(product.rating)}
                        <span className="rating-text">({product.rating})</span>
                      </div>
                      <div className="product-price">${product.price}</div>
                    </div>
                  </Link>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Newsletter Section */}
      <section className="newsletter">
        <div className="container">
          <div className="newsletter-content">
            <h2>Stay Updated</h2>
            <p>Subscribe to our newsletter and get the latest deals and updates.</p>
            <form className="newsletter-form">
              <input 
                type="email" 
                placeholder="Enter your email" 
                className="newsletter-input"
                required
              />
              <button type="submit" className="btn btn-primary">
                Subscribe
              </button>
            </form>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;