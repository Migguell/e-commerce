import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import { useProducts } from '../../context/ProductContext';
import './ProductDetail.css';

const ProductDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const { products, loading } = useProducts();
  const [product, setProduct] = useState(null);
  const [selectedImage, setSelectedImage] = useState(0);
  const [quantity, setQuantity] = useState(1);
  const [selectedSize, setSelectedSize] = useState('');
  const [selectedColor, setSelectedColor] = useState('');
  const [showFullDescription, setShowFullDescription] = useState(false);

  useEffect(() => {
    if (products.length > 0) {
      const foundProduct = products.find(p => p.id === parseInt(id));
      if (foundProduct) {
        setProduct(foundProduct);
        // Set default selections
        if (foundProduct.sizes && foundProduct.sizes.length > 0) {
          setSelectedSize(foundProduct.sizes[0]);
        }
        if (foundProduct.colors && foundProduct.colors.length > 0) {
          setSelectedColor(foundProduct.colors[0]);
        }
      }
    }
  }, [id, products]);

  const handleAddToCart = () => {
    if (!product) return;
    
    const cartItem = {
      ...product,
      quantity,
      selectedSize,
      selectedColor,
      cartId: `${product.id}-${selectedSize}-${selectedColor}`
    };
    
    addToCart(cartItem);
    
    // Show success message (you could use a toast library here)
    alert(`Added ${quantity} ${product.name} to cart!`);
  };

  const handleQuantityChange = (change) => {
    const newQuantity = quantity + change;
    if (newQuantity >= 1 && newQuantity <= (product?.stock || 99)) {
      setQuantity(newQuantity);
    }
  };

  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    
    for (let i = 0; i < fullStars; i++) {
      stars.push(<span key={i} className="star">★</span>);
    }
    
    if (hasHalfStar) {
      stars.push(<span key="half" className="star half">★</span>);
    }
    
    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<span key={`empty-${i}`} className="star empty">★</span>);
    }
    
    return stars;
  };

  if (loading) {
    return (
      <div className="product-detail-container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading product...</p>
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="product-detail-container">
        <div className="error">
          <h2>Product Not Found</h2>
          <p>The product you're looking for doesn't exist.</p>
          <button onClick={() => navigate('/products')} className="btn btn-primary">
            Browse Products
          </button>
        </div>
      </div>
    );
  }

  // Mock additional images if not provided
  const productImages = product.images || [product.image_url || product.image || '/api/placeholder/600/600'];
  if (productImages.length === 1 && (product.image_url || product.image)) {
    productImages.push(
      '/api/placeholder/600/600',
      '/api/placeholder/600/600',
      '/api/placeholder/600/600'
    );
  }

  return (
    <div className="product-detail-container">
      <div className="container">
        {/* Breadcrumb */}
        <nav className="breadcrumb">
          <button onClick={() => navigate('/')} className="breadcrumb-link">
            Home
          </button>
          <span className="breadcrumb-separator">›</span>
          <button onClick={() => navigate('/products')} className="breadcrumb-link">
            Products
          </button>
          <span className="breadcrumb-separator">›</span>
          <span className="breadcrumb-current">{product.name}</span>
        </nav>

        <div className="product-detail">
          {/* Product Images */}
          <div className="product-images">
            <div className="main-image">
              <img
                src={productImages[selectedImage]}
                alt={product.name}
                onError={(e) => {
                  e.target.src = '/api/placeholder/600/600';
                }}
              />
              {product.discount && (
                <div className="discount-badge">
                  -{product.discount}% OFF
                </div>
              )}
            </div>
            {productImages.length > 1 && (
              <div className="image-thumbnails">
                {productImages.map((image, index) => (
                  <button
                    key={index}
                    className={`thumbnail ${selectedImage === index ? 'active' : ''}`}
                    onClick={() => setSelectedImage(index)}
                  >
                    <img
                      src={image}
                      alt={`${product.name} ${index + 1}`}
                      onError={(e) => {
                        e.target.src = '/api/placeholder/150/150';
                      }}
                    />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Product Info */}
          <div className="product-info">
            <div className="product-header">
              <h1 className="product-title">{product.name}</h1>
              <div className="product-rating">
                <div className="stars">
                  {renderStars(product.rating || 0)}
                </div>
                <span className="rating-text">
                  ({product.rating || 0}) • {product.reviews || 0} reviews
                </span>
              </div>
            </div>

            <div className="product-price">
              {product.originalPrice && product.originalPrice > product.price && (
                <span className="original-price">${product.originalPrice}</span>
              )}
              <span className="current-price">${product.price}</span>
              {product.discount && (
                <span className="savings">
                  Save ${(product.originalPrice - product.price).toFixed(2)}
                </span>
              )}
            </div>

            <div className="product-description">
              <p className={showFullDescription ? 'full' : 'truncated'}>
                {product.description || 'No description available for this product.'}
              </p>
              {product.description && product.description.length > 150 && (
                <button
                  className="toggle-description"
                  onClick={() => setShowFullDescription(!showFullDescription)}
                >
                  {showFullDescription ? 'Show Less' : 'Show More'}
                </button>
              )}
            </div>

            {/* Product Options */}
            <div className="product-options">
              {product.sizes && product.sizes.length > 0 && (
                <div className="option-group">
                  <label>Size:</label>
                  <div className="size-options">
                    {product.sizes.map(size => (
                      <button
                        key={size}
                        className={`size-option ${selectedSize === size ? 'selected' : ''}`}
                        onClick={() => setSelectedSize(size)}
                      >
                        {size}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {product.colors && product.colors.length > 0 && (
                <div className="option-group">
                  <label>Color:</label>
                  <div className="color-options">
                    {product.colors.map(color => (
                      <button
                        key={color}
                        className={`color-option ${selectedColor === color ? 'selected' : ''}`}
                        onClick={() => setSelectedColor(color)}
                        style={{ backgroundColor: color.toLowerCase() }}
                        title={color}
                      >
                        {selectedColor === color && <span className="checkmark">✓</span>}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              <div className="option-group">
                <label>Quantity:</label>
                <div className="quantity-selector">
                  <button
                    className="quantity-btn"
                    onClick={() => handleQuantityChange(-1)}
                    disabled={quantity <= 1}
                  >
                    -
                  </button>
                  <span className="quantity-display">{quantity}</span>
                  <button
                    className="quantity-btn"
                    onClick={() => handleQuantityChange(1)}
                    disabled={quantity >= (product.stock || 99)}
                  >
                    +
                  </button>
                </div>
                {product.stock && (
                  <span className="stock-info">
                    {product.stock} in stock
                  </span>
                )}
              </div>
            </div>

            {/* Add to Cart */}
            <div className="product-actions">
              <button
                className="btn btn-primary add-to-cart"
                onClick={handleAddToCart}
                disabled={product.stock === 0}
              >
                {product.stock === 0 ? 'Out of Stock' : `Add to Cart - $${(product.price * quantity).toFixed(2)}`}
              </button>
              <button className="btn btn-secondary wishlist">
                ♡ Add to Wishlist
              </button>
            </div>

            {/* Product Features */}
            {product.features && (
              <div className="product-features">
                <h3>Features:</h3>
                <ul>
                  {product.features.map((feature, index) => (
                    <li key={index}>{feature}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Shipping Info */}
            <div className="shipping-info">
              <div className="shipping-item">
                <span className="icon">🚚</span>
                <div>
                  <strong>Free Shipping</strong>
                  <p>On orders over $50</p>
                </div>
              </div>
              <div className="shipping-item">
                <span className="icon">↩️</span>
                <div>
                  <strong>Easy Returns</strong>
                  <p>30-day return policy</p>
                </div>
              </div>
              <div className="shipping-item">
                <span className="icon">🔒</span>
                <div>
                  <strong>Secure Payment</strong>
                  <p>SSL encrypted checkout</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetail;