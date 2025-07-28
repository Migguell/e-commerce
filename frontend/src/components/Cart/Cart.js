import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import './Cart.css';

const Cart = () => {
  const { cartItems, updateQuantity, removeFromCart, getCartTotal, clearCart } = useCart();
  const navigate = useNavigate();

  const handleQuantityChange = (item, newQuantity) => {
    if (newQuantity <= 0) {
      removeFromCart(item.cartId || item.id);
    } else {
      updateQuantity(item.cartId || item.id, newQuantity);
    }
  };

  const handleCheckout = () => {
    // In a real app, this would navigate to checkout process
    alert('Checkout functionality would be implemented here!');
  };

  const handleContinueShopping = () => {
    navigate('/products');
  };

  if (cartItems.length === 0) {
    return (
      <div className="cart-container">
        <div className="container">
          <div className="empty-cart">
            <div className="empty-cart-icon">🛒</div>
            <h2>Your cart is empty</h2>
            <p>Looks like you haven't added any items to your cart yet.</p>
            <Link to="/products" className="btn btn-primary">
              Start Shopping
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const subtotal = getCartTotal();
  const shipping = subtotal > 50 ? 0 : 9.99;
  const tax = subtotal * 0.08; // 8% tax
  const total = subtotal + shipping + tax;

  return (
    <div className="cart-container">
      <div className="container">
        <div className="cart-header">
          <h1>Shopping Cart</h1>
          <p>{cartItems.length} {cartItems.length === 1 ? 'item' : 'items'} in your cart</p>
        </div>

        <div className="cart-content">
          {/* Cart Items */}
          <div className="cart-items">
            <div className="cart-items-header">
              <span>Product</span>
              <span>Price</span>
              <span>Quantity</span>
              <span>Total</span>
              <span></span>
            </div>

            {cartItems.map((item) => {
              const itemTotal = item.price * item.quantity;
              
              return (
                <div key={item.cartId || item.id} className="cart-item">
                  <div className="item-info">
                    <Link to={`/product/${item.id}`} className="item-image">
                      <img
                        src={item.image || '/api/placeholder/100/100'}
                        alt={item.name}
                        onError={(e) => {
                          e.target.src = '/api/placeholder/100/100';
                        }}
                      />
                    </Link>
                    <div className="item-details">
                      <Link to={`/product/${item.id}`} className="item-name">
                        {item.name}
                      </Link>
                      <div className="item-options">
                        {item.selectedSize && (
                          <span className="option">Size: {item.selectedSize}</span>
                        )}
                        {item.selectedColor && (
                          <span className="option">Color: {item.selectedColor}</span>
                        )}
                      </div>
                      {item.stock && item.stock < 10 && (
                        <div className="low-stock-warning">
                          Only {item.stock} left in stock
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="item-price">
                    ${item.price.toFixed(2)}
                  </div>

                  <div className="item-quantity">
                    <div className="quantity-controls">
                      <button
                        className="quantity-btn"
                        onClick={() => handleQuantityChange(item, item.quantity - 1)}
                        disabled={item.quantity <= 1}
                      >
                        -
                      </button>
                      <span className="quantity-display">{item.quantity}</span>
                      <button
                        className="quantity-btn"
                        onClick={() => handleQuantityChange(item, item.quantity + 1)}
                        disabled={item.stock && item.quantity >= item.stock}
                      >
                        +
                      </button>
                    </div>
                  </div>

                  <div className="item-total">
                    ${itemTotal.toFixed(2)}
                  </div>

                  <div className="item-actions">
                    <button
                      className="remove-btn"
                      onClick={() => removeFromCart(item.cartId || item.id)}
                      title="Remove from cart"
                    >
                      ×
                    </button>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Cart Summary */}
          <div className="cart-summary">
            <div className="summary-card">
              <h3>Order Summary</h3>
              
              <div className="summary-line">
                <span>Subtotal ({cartItems.length} items)</span>
                <span>${subtotal.toFixed(2)}</span>
              </div>
              
              <div className="summary-line">
                <span>Shipping</span>
                <span>
                  {shipping === 0 ? (
                    <span className="free-shipping">FREE</span>
                  ) : (
                    `$${shipping.toFixed(2)}`
                  )}
                </span>
              </div>
              
              {shipping > 0 && (
                <div className="shipping-notice">
                  <small>Free shipping on orders over $50</small>
                </div>
              )}
              
              <div className="summary-line">
                <span>Tax</span>
                <span>${tax.toFixed(2)}</span>
              </div>
              
              <div className="summary-line total">
                <span>Total</span>
                <span>${total.toFixed(2)}</span>
              </div>
              
              <div className="summary-actions">
                <button
                  className="btn btn-primary checkout-btn"
                  onClick={handleCheckout}
                >
                  Proceed to Checkout
                </button>
                
                <button
                  className="btn btn-secondary continue-shopping"
                  onClick={handleContinueShopping}
                >
                  Continue Shopping
                </button>
              </div>
              
              <div className="security-badges">
                <div className="security-item">
                  <span className="icon">🔒</span>
                  <span>Secure Checkout</span>
                </div>
                <div className="security-item">
                  <span className="icon">↩️</span>
                  <span>Easy Returns</span>
                </div>
              </div>
            </div>
            
            {/* Promo Code */}
            <div className="promo-code">
              <h4>Have a promo code?</h4>
              <div className="promo-input">
                <input
                  type="text"
                  placeholder="Enter promo code"
                  className="promo-field"
                />
                <button className="btn btn-secondary apply-promo">
                  Apply
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Cart Actions */}
        <div className="cart-footer">
          <button
            className="btn btn-outline clear-cart"
            onClick={() => {
              if (window.confirm('Are you sure you want to clear your cart?')) {
                clearCart();
              }
            }}
          >
            Clear Cart
          </button>
          
          <div className="cart-footer-info">
            <div className="info-item">
              <span className="icon">🚚</span>
              <span>Free shipping on orders over $50</span>
            </div>
            <div className="info-item">
              <span className="icon">💳</span>
              <span>Secure payment with SSL encryption</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;