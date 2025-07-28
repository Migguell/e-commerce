import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import { useApp } from '../../context/AppContext';
import './Header.css';

const Header = () => {
  const { cart, getCartItemCount } = useCart();
  const { state: appState, dispatch: appDispatch } = useApp();
  const navigate = useNavigate();
  const itemCount = getCartItemCount();

  const handleSearch = (e) => {
    e.preventDefault();
    const searchTerm = e.target.search.value;
    if (searchTerm.trim()) {
      navigate(`/products?search=${encodeURIComponent(searchTerm)}`);
    }
  };

  const toggleSidebar = () => {
    appDispatch({ type: 'TOGGLE_SIDEBAR' });
  };

  return (
    <header className="header">
      <div className="header-container">
        {/* Logo and Brand */}
        <div className="header-brand">
          <button 
            className="sidebar-toggle"
            onClick={toggleSidebar}
            aria-label="Toggle menu"
          >
            <span className="hamburger"></span>
            <span className="hamburger"></span>
            <span className="hamburger"></span>
          </button>
          <Link to="/" className="brand-link">
            <h1 className="brand-name">E-Shop</h1>
          </Link>
        </div>

        {/* Search Bar */}
        <div className="header-search">
          <form onSubmit={handleSearch} className="search-form">
            <input
              type="text"
              name="search"
              placeholder="Search products..."
              className="search-input"
            />
            <button type="submit" className="search-button">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path
                  d="M21 21L16.514 16.506L21 21ZM19 10.5C19 15.194 15.194 19 10.5 19C5.806 19 2 15.194 2 10.5C2 5.806 5.806 2 10.5 2C15.194 2 19 5.806 19 10.5Z"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </button>
          </form>
        </div>

        {/* Navigation Links */}
        <nav className="header-nav">
          <Link to="/products" className="nav-link">
            Products
          </Link>
          <Link to="/cart" className="nav-link cart-link">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path
                d="M3 3H5L5.4 5M7 13H17L21 5H5.4M7 13L5.4 5M7 13L4.7 15.3C4.3 15.7 4.6 16.5 5.1 16.5H17M17 13V17C17 18.1 16.1 19 15 19H9C7.9 19 7 18.1 7 17V13M17 13H7"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            Cart
            {itemCount > 0 && (
              <span className="cart-badge">{itemCount}</span>
            )}
          </Link>
          <Link to="/login" className="nav-link">
            Login
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;