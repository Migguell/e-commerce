// Price formatting utilities
export const formatPrice = (price, currency = 'USD', locale = 'en-US') => {
  if (price === null || price === undefined || isNaN(price)) {
    return '—';
  }

  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(price);
};

export const formatPriceRange = (minPrice, maxPrice, currency = 'USD', locale = 'en-US') => {
  if (minPrice === maxPrice) {
    return formatPrice(minPrice, currency, locale);
  }
  return `${formatPrice(minPrice, currency, locale)} - ${formatPrice(maxPrice, currency, locale)}`;
};

export const formatDiscount = (originalPrice, discountedPrice, currency = 'USD', locale = 'en-US') => {
  const savings = originalPrice - discountedPrice;
  const percentage = Math.round((savings / originalPrice) * 100);
  
  return {
    savings: formatPrice(savings, currency, locale),
    percentage: `${percentage}%`,
    original: formatPrice(originalPrice, currency, locale),
    discounted: formatPrice(discountedPrice, currency, locale)
  };
};

// Date formatting utilities
export const formatDate = (date, options = {}) => {
  if (!date) return '—';
  
  const defaultOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  };
  
  const formatOptions = { ...defaultOptions, ...options };
  
  try {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    return dateObj.toLocaleDateString('en-US', formatOptions);
  } catch (error) {
    console.error('Error formatting date:', error);
    return '—';
  }
};

export const formatDateTime = (date, options = {}) => {
  if (!date) return '—';
  
  const defaultOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  };
  
  const formatOptions = { ...defaultOptions, ...options };
  
  try {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    return dateObj.toLocaleDateString('en-US', formatOptions);
  } catch (error) {
    console.error('Error formatting datetime:', error);
    return '—';
  }
};

export const formatRelativeTime = (date) => {
  if (!date) return '—';
  
  try {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    const now = new Date();
    const diffInSeconds = Math.floor((now - dateObj) / 1000);
    
    if (diffInSeconds < 60) {
      return 'Just now';
    } else if (diffInSeconds < 3600) {
      const minutes = Math.floor(diffInSeconds / 60);
      return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    } else if (diffInSeconds < 86400) {
      const hours = Math.floor(diffInSeconds / 3600);
      return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    } else if (diffInSeconds < 604800) {
      const days = Math.floor(diffInSeconds / 86400);
      return `${days} day${days > 1 ? 's' : ''} ago`;
    } else {
      return formatDate(dateObj, { month: 'short', day: 'numeric' });
    }
  } catch (error) {
    console.error('Error formatting relative time:', error);
    return '—';
  }
};

// Number formatting utilities
export const formatNumber = (number, options = {}) => {
  if (number === null || number === undefined || isNaN(number)) {
    return '—';
  }
  
  const defaultOptions = {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2
  };
  
  const formatOptions = { ...defaultOptions, ...options };
  
  return new Intl.NumberFormat('en-US', formatOptions).format(number);
};

export const formatPercentage = (value, decimals = 1) => {
  if (value === null || value === undefined || isNaN(value)) {
    return '—';
  }
  
  return `${(value * 100).toFixed(decimals)}%`;
};

export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// Text formatting utilities
export const formatPhoneNumber = (phoneNumber) => {
  if (!phoneNumber) return '—';
  
  // Remove all non-digit characters
  const cleaned = phoneNumber.replace(/\D/g, '');
  
  // Format as (XXX) XXX-XXXX for US numbers
  if (cleaned.length === 10) {
    return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
  }
  
  // Return original if not a standard US number
  return phoneNumber;
};

export const formatAddress = (address) => {
  if (!address) return '—';
  
  const parts = [];
  
  if (address.street) parts.push(address.street);
  if (address.street2) parts.push(address.street2);
  
  const cityStateZip = [];
  if (address.city) cityStateZip.push(address.city);
  if (address.state) cityStateZip.push(address.state);
  if (address.zipCode) cityStateZip.push(address.zipCode);
  
  if (cityStateZip.length > 0) {
    parts.push(cityStateZip.join(', '));
  }
  
  if (address.country && address.country !== 'US') {
    parts.push(address.country);
  }
  
  return parts.join('\n');
};

export const formatName = (firstName, lastName) => {
  const parts = [];
  if (firstName) parts.push(firstName);
  if (lastName) parts.push(lastName);
  return parts.join(' ') || '—';
};

export const formatInitials = (firstName, lastName) => {
  const firstInitial = firstName ? firstName.charAt(0).toUpperCase() : '';
  const lastInitial = lastName ? lastName.charAt(0).toUpperCase() : '';
  return firstInitial + lastInitial;
};

// String utilities
export const truncateText = (text, maxLength = 100, suffix = '...') => {
  if (!text || text.length <= maxLength) {
    return text || '';
  }
  
  return text.substring(0, maxLength - suffix.length) + suffix;
};

export const capitalizeFirst = (str) => {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

export const capitalizeWords = (str) => {
  if (!str) return '';
  return str.replace(/\w\S*/g, (txt) => 
    txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
  );
};

export const slugify = (str) => {
  if (!str) return '';
  
  return str
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '') // Remove special characters
    .replace(/[\s_-]+/g, '-') // Replace spaces and underscores with hyphens
    .replace(/^-+|-+$/g, ''); // Remove leading/trailing hyphens
};

// Product-specific formatters
export const formatProductCode = (code) => {
  if (!code) return '—';
  return code.toUpperCase();
};

export const formatRating = (rating, maxRating = 5) => {
  if (rating === null || rating === undefined) {
    return '—';
  }
  
  return `${rating.toFixed(1)}/${maxRating}`;
};

export const formatReviewCount = (count) => {
  if (!count || count === 0) {
    return 'No reviews';
  }
  
  if (count === 1) {
    return '1 review';
  }
  
  if (count < 1000) {
    return `${count} reviews`;
  }
  
  if (count < 1000000) {
    return `${(count / 1000).toFixed(1)}k reviews`;
  }
  
  return `${(count / 1000000).toFixed(1)}m reviews`;
};

export const formatStockStatus = (quantity, threshold = 10) => {
  if (quantity === 0) {
    return { status: 'out-of-stock', text: 'Out of Stock', color: 'red' };
  } else if (quantity <= threshold) {
    return { status: 'low-stock', text: `Only ${quantity} left`, color: 'orange' };
  } else {
    return { status: 'in-stock', text: 'In Stock', color: 'green' };
  }
};

// Order status formatters
export const formatOrderStatus = (status) => {
  const statusMap = {
    'pending': { text: 'Pending', color: 'yellow' },
    'confirmed': { text: 'Confirmed', color: 'blue' },
    'processing': { text: 'Processing', color: 'blue' },
    'shipped': { text: 'Shipped', color: 'purple' },
    'delivered': { text: 'Delivered', color: 'green' },
    'cancelled': { text: 'Cancelled', color: 'red' },
    'refunded': { text: 'Refunded', color: 'gray' }
  };
  
  return statusMap[status] || { text: capitalizeFirst(status), color: 'gray' };
};

export const formatPaymentStatus = (status) => {
  const statusMap = {
    'pending': { text: 'Payment Pending', color: 'yellow' },
    'paid': { text: 'Paid', color: 'green' },
    'failed': { text: 'Payment Failed', color: 'red' },
    'refunded': { text: 'Refunded', color: 'gray' },
    'partially_refunded': { text: 'Partially Refunded', color: 'orange' }
  };
  
  return statusMap[status] || { text: capitalizeFirst(status), color: 'gray' };
};