import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { useCart } from '../../context/CartContext';
import './Profile.css';

const Profile = () => {
  const { user, updateUser, logout } = useApp();
  const { clearCart, getCartTotal, cartItems } = useCart();
  
  const [activeTab, setActiveTab] = useState('profile');
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const [formData, setFormData] = useState({
    firstName: user?.firstName || '',
    lastName: user?.lastName || '',
    email: user?.email || '',
    phone: user?.phone || '',
    dateOfBirth: user?.dateOfBirth || '',
    address: {
      street: user?.address?.street || '',
      city: user?.address?.city || '',
      state: user?.address?.state || '',
      zipCode: user?.address?.zipCode || '',
      country: user?.address?.country || 'United States'
    },
    preferences: {
      newsletter: user?.preferences?.newsletter || false,
      notifications: user?.preferences?.notifications || false,
      darkMode: user?.preferences?.darkMode || false
    }
  });
  
  const [errors, setErrors] = useState({});

  // Mock order data
  const mockOrders = [
    {
      id: 'ORD-001',
      date: '2024-01-15',
      status: 'Delivered',
      total: 129.99,
      items: [
        { name: 'Wireless Headphones', quantity: 1, price: 79.99 },
        { name: 'Phone Case', quantity: 2, price: 25.00 }
      ]
    },
    {
      id: 'ORD-002',
      date: '2024-01-10',
      status: 'Shipped',
      total: 89.99,
      items: [
        { name: 'Bluetooth Speaker', quantity: 1, price: 89.99 }
      ]
    },
    {
      id: 'ORD-003',
      date: '2024-01-05',
      status: 'Processing',
      total: 199.99,
      items: [
        { name: 'Smart Watch', quantity: 1, price: 199.99 }
      ]
    }
  ];

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (name.includes('.')) {
      const [parent, child] = name.split('.');
      setFormData(prev => ({
        ...prev,
        [parent]: {
          ...prev[parent],
          [child]: type === 'checkbox' ? checked : value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: type === 'checkbox' ? checked : value
      }));
    }
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.firstName.trim()) {
      newErrors.firstName = 'First name is required';
    }
    
    if (!formData.lastName.trim()) {
      newErrors.lastName = 'Last name is required';
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!emailRegex.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }
    
    if (formData.phone && !/^[\d\s\-\(\)\+]+$/.test(formData.phone)) {
      newErrors.phone = 'Please enter a valid phone number';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSave = async () => {
    if (!validateForm()) {
      return;
    }
    
    setIsLoading(true);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const updatedUser = {
        ...user,
        ...formData,
        name: `${formData.firstName} ${formData.lastName}`,
        updatedAt: new Date().toISOString()
      };
      
      updateUser(updatedUser);
      setIsEditing(false);
      
    } catch (error) {
      console.error('Update error:', error);
      setErrors({ submit: 'Failed to update profile. Please try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    setFormData({
      firstName: user?.firstName || '',
      lastName: user?.lastName || '',
      email: user?.email || '',
      phone: user?.phone || '',
      dateOfBirth: user?.dateOfBirth || '',
      address: {
        street: user?.address?.street || '',
        city: user?.address?.city || '',
        state: user?.address?.state || '',
        zipCode: user?.address?.zipCode || '',
        country: user?.address?.country || 'United States'
      },
      preferences: {
        newsletter: user?.preferences?.newsletter || false,
        notifications: user?.preferences?.notifications || false,
        darkMode: user?.preferences?.darkMode || false
      }
    });
    setErrors({});
    setIsEditing(false);
  };

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'delivered': return '#22c55e';
      case 'shipped': return '#3b82f6';
      case 'processing': return '#eab308';
      case 'cancelled': return '#ef4444';
      default: return '#6b7280';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (!user) {
    return (
      <div className="profile-container">
        <div className="container">
          <div className="not-logged-in">
            <h2>Please log in to view your profile</h2>
            <p>You need to be logged in to access this page.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-container">
      <div className="container">
        <div className="profile-header">
          <div className="user-info">
            <div className="avatar">
              <img src={user.avatar} alt={user.name} />
            </div>
            <div className="user-details">
              <h1>Welcome back, {user.firstName}!</h1>
              <p>Manage your account and view your orders</p>
            </div>
          </div>
        </div>

        <div className="profile-content">
          {/* Navigation Tabs */}
          <div className="profile-tabs">
            <button 
              className={`tab ${activeTab === 'profile' ? 'active' : ''}`}
              onClick={() => setActiveTab('profile')}
            >
              👤 Profile
            </button>
            <button 
              className={`tab ${activeTab === 'orders' ? 'active' : ''}`}
              onClick={() => setActiveTab('orders')}
            >
              📦 Orders
            </button>
            <button 
              className={`tab ${activeTab === 'settings' ? 'active' : ''}`}
              onClick={() => setActiveTab('settings')}
            >
              ⚙️ Settings
            </button>
          </div>

          {/* Profile Tab */}
          {activeTab === 'profile' && (
            <div className="tab-content">
              <div className="section-header">
                <h2>Personal Information</h2>
                {!isEditing ? (
                  <button className="btn btn-secondary" onClick={() => setIsEditing(true)}>
                    ✏️ Edit Profile
                  </button>
                ) : (
                  <div className="edit-actions">
                    <button 
                      className="btn btn-secondary" 
                      onClick={handleCancel}
                      disabled={isLoading}
                    >
                      Cancel
                    </button>
                    <button 
                      className="btn btn-primary" 
                      onClick={handleSave}
                      disabled={isLoading}
                    >
                      {isLoading ? (
                        <>
                          <div className="spinner"></div>
                          Saving...
                        </>
                      ) : (
                        'Save Changes'
                      )}
                    </button>
                  </div>
                )}
              </div>

              {errors.submit && (
                <div className="error-message">
                  <span className="error-icon">⚠️</span>
                  {errors.submit}
                </div>
              )}

              <div className="profile-form">
                <div className="form-row">
                  <div className="form-group">
                    <label>First Name</label>
                    {isEditing ? (
                      <input
                        type="text"
                        name="firstName"
                        value={formData.firstName}
                        onChange={handleInputChange}
                        className={errors.firstName ? 'error' : ''}
                        disabled={isLoading}
                      />
                    ) : (
                      <div className="form-value">{user.firstName}</div>
                    )}
                    {errors.firstName && <span className="field-error">{errors.firstName}</span>}
                  </div>
                  
                  <div className="form-group">
                    <label>Last Name</label>
                    {isEditing ? (
                      <input
                        type="text"
                        name="lastName"
                        value={formData.lastName}
                        onChange={handleInputChange}
                        className={errors.lastName ? 'error' : ''}
                        disabled={isLoading}
                      />
                    ) : (
                      <div className="form-value">{user.lastName}</div>
                    )}
                    {errors.lastName && <span className="field-error">{errors.lastName}</span>}
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Email Address</label>
                    {isEditing ? (
                      <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        className={errors.email ? 'error' : ''}
                        disabled={isLoading}
                      />
                    ) : (
                      <div className="form-value">{user.email}</div>
                    )}
                    {errors.email && <span className="field-error">{errors.email}</span>}
                  </div>
                  
                  <div className="form-group">
                    <label>Phone Number</label>
                    {isEditing ? (
                      <input
                        type="tel"
                        name="phone"
                        value={formData.phone}
                        onChange={handleInputChange}
                        placeholder="(555) 123-4567"
                        className={errors.phone ? 'error' : ''}
                        disabled={isLoading}
                      />
                    ) : (
                      <div className="form-value">{user.phone || 'Not provided'}</div>
                    )}
                    {errors.phone && <span className="field-error">{errors.phone}</span>}
                  </div>
                </div>

                <div className="form-group">
                  <label>Date of Birth</label>
                  {isEditing ? (
                    <input
                      type="date"
                      name="dateOfBirth"
                      value={formData.dateOfBirth}
                      onChange={handleInputChange}
                      disabled={isLoading}
                    />
                  ) : (
                    <div className="form-value">
                      {user.dateOfBirth ? formatDate(user.dateOfBirth) : 'Not provided'}
                    </div>
                  )}
                </div>

                <h3>Address</h3>
                <div className="form-group">
                  <label>Street Address</label>
                  {isEditing ? (
                    <input
                      type="text"
                      name="address.street"
                      value={formData.address.street}
                      onChange={handleInputChange}
                      placeholder="123 Main Street"
                      disabled={isLoading}
                    />
                  ) : (
                    <div className="form-value">{user.address?.street || 'Not provided'}</div>
                  )}
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>City</label>
                    {isEditing ? (
                      <input
                        type="text"
                        name="address.city"
                        value={formData.address.city}
                        onChange={handleInputChange}
                        placeholder="New York"
                        disabled={isLoading}
                      />
                    ) : (
                      <div className="form-value">{user.address?.city || 'Not provided'}</div>
                    )}
                  </div>
                  
                  <div className="form-group">
                    <label>State</label>
                    {isEditing ? (
                      <input
                        type="text"
                        name="address.state"
                        value={formData.address.state}
                        onChange={handleInputChange}
                        placeholder="NY"
                        disabled={isLoading}
                      />
                    ) : (
                      <div className="form-value">{user.address?.state || 'Not provided'}</div>
                    )}
                  </div>
                  
                  <div className="form-group">
                    <label>ZIP Code</label>
                    {isEditing ? (
                      <input
                        type="text"
                        name="address.zipCode"
                        value={formData.address.zipCode}
                        onChange={handleInputChange}
                        placeholder="10001"
                        disabled={isLoading}
                      />
                    ) : (
                      <div className="form-value">{user.address?.zipCode || 'Not provided'}</div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Orders Tab */}
          {activeTab === 'orders' && (
            <div className="tab-content">
              <div className="section-header">
                <h2>Order History</h2>
                <div className="order-stats">
                  <span className="stat">
                    <strong>{mockOrders.length}</strong> Total Orders
                  </span>
                  <span className="stat">
                    <strong>${mockOrders.reduce((sum, order) => sum + order.total, 0).toFixed(2)}</strong> Total Spent
                  </span>
                </div>
              </div>

              <div className="orders-list">
                {mockOrders.map(order => (
                  <div key={order.id} className="order-card">
                    <div className="order-header">
                      <div className="order-info">
                        <h3>Order #{order.id}</h3>
                        <p>Placed on {formatDate(order.date)}</p>
                      </div>
                      <div className="order-status">
                        <span 
                          className="status-badge" 
                          style={{ backgroundColor: getStatusColor(order.status) }}
                        >
                          {order.status}
                        </span>
                        <div className="order-total">${order.total.toFixed(2)}</div>
                      </div>
                    </div>
                    
                    <div className="order-items">
                      {order.items.map((item, index) => (
                        <div key={index} className="order-item">
                          <span className="item-name">{item.name}</span>
                          <span className="item-quantity">Qty: {item.quantity}</span>
                          <span className="item-price">${item.price.toFixed(2)}</span>
                        </div>
                      ))}
                    </div>
                    
                    <div className="order-actions">
                      <button className="btn btn-secondary btn-sm">View Details</button>
                      {order.status === 'Delivered' && (
                        <button className="btn btn-secondary btn-sm">Reorder</button>
                      )}
                      {order.status === 'Shipped' && (
                        <button className="btn btn-secondary btn-sm">Track Package</button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Settings Tab */}
          {activeTab === 'settings' && (
            <div className="tab-content">
              <div className="section-header">
                <h2>Account Settings</h2>
              </div>

              <div className="settings-section">
                <h3>Preferences</h3>
                <div className="preference-item">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      name="preferences.newsletter"
                      checked={formData.preferences.newsletter}
                      onChange={handleInputChange}
                    />
                    <span className="checkmark"></span>
                    <div className="preference-info">
                      <strong>Newsletter Subscription</strong>
                      <p>Receive updates about new products and special offers</p>
                    </div>
                  </label>
                </div>
                
                <div className="preference-item">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      name="preferences.notifications"
                      checked={formData.preferences.notifications}
                      onChange={handleInputChange}
                    />
                    <span className="checkmark"></span>
                    <div className="preference-info">
                      <strong>Order Notifications</strong>
                      <p>Get notified about order status updates</p>
                    </div>
                  </label>
                </div>
                
                <div className="preference-item">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      name="preferences.darkMode"
                      checked={formData.preferences.darkMode}
                      onChange={handleInputChange}
                      disabled
                    />
                    <span className="checkmark"></span>
                    <div className="preference-info">
                      <strong>Dark Mode</strong>
                      <p>Switch to dark theme (Coming soon)</p>
                    </div>
                  </label>
                </div>
              </div>

              <div className="settings-section">
                <h3>Account Actions</h3>
                <div className="action-buttons">
                  <button className="btn btn-secondary">
                    🔒 Change Password
                  </button>
                  <button className="btn btn-secondary">
                    📧 Update Email
                  </button>
                  <button 
                    className="btn btn-warning"
                    onClick={() => {
                      if (window.confirm('Are you sure you want to clear your cart?')) {
                        clearCart();
                      }
                    }}
                  >
                    🛒 Clear Cart ({cartItems.length} items)
                  </button>
                  <button 
                    className="btn btn-danger"
                    onClick={() => {
                      if (window.confirm('Are you sure you want to log out?')) {
                        logout();
                      }
                    }}
                  >
                    🚪 Log Out
                  </button>
                </div>
              </div>

              <div className="settings-section">
                <h3>Account Information</h3>
                <div className="account-info">
                  <div className="info-item">
                    <label>Member Since</label>
                    <span>{formatDate(user.createdAt)}</span>
                  </div>
                  <div className="info-item">
                    <label>Last Updated</label>
                    <span>{formatDate(user.updatedAt || user.createdAt)}</span>
                  </div>
                  <div className="info-item">
                    <label>Cart Total</label>
                    <span>${getCartTotal().toFixed(2)}</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile;