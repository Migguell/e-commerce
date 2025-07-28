// Email validation
export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Password validation
export const validatePassword = (password) => {
  const errors = [];
  
  if (!password) {
    errors.push('Password is required');
    return { isValid: false, errors };
  }
  
  if (password.length < 8) {
    errors.push('Password must be at least 8 characters long');
  }
  
  if (!/(?=.*[a-z])/.test(password)) {
    errors.push('Password must contain at least one lowercase letter');
  }
  
  if (!/(?=.*[A-Z])/.test(password)) {
    errors.push('Password must contain at least one uppercase letter');
  }
  
  if (!/(?=.*\d)/.test(password)) {
    errors.push('Password must contain at least one number');
  }
  
  if (!/(?=.*[@$!%*?&])/.test(password)) {
    errors.push('Password must contain at least one special character (@$!%*?&)');
  }
  
  return {
    isValid: errors.length === 0,
    errors,
    strength: getPasswordStrength(password)
  };
};

export const getPasswordStrength = (password) => {
  let score = 0;
  
  if (password.length >= 8) score++;
  if (password.length >= 12) score++;
  if (/(?=.*[a-z])/.test(password)) score++;
  if (/(?=.*[A-Z])/.test(password)) score++;
  if (/(?=.*\d)/.test(password)) score++;
  if (/(?=.*[@$!%*?&])/.test(password)) score++;
  if (password.length >= 16) score++;
  
  if (score <= 2) return { level: 'weak', color: 'red', text: 'Weak' };
  if (score <= 4) return { level: 'medium', color: 'orange', text: 'Medium' };
  if (score <= 6) return { level: 'strong', color: 'green', text: 'Strong' };
  return { level: 'very-strong', color: 'darkgreen', text: 'Very Strong' };
};

// Phone number validation
export const isValidPhoneNumber = (phone) => {
  // Remove all non-digit characters
  const cleaned = phone.replace(/\D/g, '');
  
  // Check if it's a valid US phone number (10 digits)
  return cleaned.length === 10;
};

export const formatPhoneInput = (value) => {
  // Remove all non-digit characters
  const cleaned = value.replace(/\D/g, '');
  
  // Limit to 10 digits
  const limited = cleaned.substring(0, 10);
  
  // Format as (XXX) XXX-XXXX
  if (limited.length >= 6) {
    return `(${limited.substring(0, 3)}) ${limited.substring(3, 6)}-${limited.substring(6)}`;
  } else if (limited.length >= 3) {
    return `(${limited.substring(0, 3)}) ${limited.substring(3)}`;
  } else {
    return limited;
  }
};

// Credit card validation
export const isValidCreditCard = (cardNumber) => {
  // Remove spaces and dashes
  const cleaned = cardNumber.replace(/[\s-]/g, '');
  
  // Check if all characters are digits
  if (!/^\d+$/.test(cleaned)) {
    return false;
  }
  
  // Check length (13-19 digits for most cards)
  if (cleaned.length < 13 || cleaned.length > 19) {
    return false;
  }
  
  // Luhn algorithm
  let sum = 0;
  let isEven = false;
  
  for (let i = cleaned.length - 1; i >= 0; i--) {
    let digit = parseInt(cleaned.charAt(i), 10);
    
    if (isEven) {
      digit *= 2;
      if (digit > 9) {
        digit -= 9;
      }
    }
    
    sum += digit;
    isEven = !isEven;
  }
  
  return sum % 10 === 0;
};

export const getCreditCardType = (cardNumber) => {
  const cleaned = cardNumber.replace(/[\s-]/g, '');
  
  if (/^4/.test(cleaned)) {
    return { type: 'visa', name: 'Visa' };
  } else if (/^5[1-5]/.test(cleaned) || /^2[2-7]/.test(cleaned)) {
    return { type: 'mastercard', name: 'Mastercard' };
  } else if (/^3[47]/.test(cleaned)) {
    return { type: 'amex', name: 'American Express' };
  } else if (/^6/.test(cleaned)) {
    return { type: 'discover', name: 'Discover' };
  } else {
    return { type: 'unknown', name: 'Unknown' };
  }
};

export const formatCreditCardInput = (value) => {
  // Remove all non-digit characters
  const cleaned = value.replace(/\D/g, '');
  
  // Add spaces every 4 digits
  const formatted = cleaned.replace(/(.{4})/g, '$1 ').trim();
  
  return formatted;
};

// CVV validation
export const isValidCVV = (cvv, cardType = 'visa') => {
  const cleaned = cvv.replace(/\D/g, '');
  
  if (cardType === 'amex') {
    return cleaned.length === 4;
  } else {
    return cleaned.length === 3;
  }
};

// Expiry date validation
export const isValidExpiryDate = (month, year) => {
  const currentDate = new Date();
  const currentMonth = currentDate.getMonth() + 1;
  const currentYear = currentDate.getFullYear();
  
  const expMonth = parseInt(month, 10);
  const expYear = parseInt(year, 10);
  
  // Check if month is valid
  if (expMonth < 1 || expMonth > 12) {
    return false;
  }
  
  // Check if year is in the future or current year
  if (expYear < currentYear) {
    return false;
  }
  
  // If it's the current year, check if month is current or future
  if (expYear === currentYear && expMonth < currentMonth) {
    return false;
  }
  
  return true;
};

export const formatExpiryInput = (value) => {
  // Remove all non-digit characters
  const cleaned = value.replace(/\D/g, '');
  
  // Add slash after 2 digits
  if (cleaned.length >= 2) {
    return `${cleaned.substring(0, 2)}/${cleaned.substring(2, 4)}`;
  }
  
  return cleaned;
};

// Name validation
export const isValidName = (name) => {
  if (!name || name.trim().length === 0) {
    return false;
  }
  
  // Allow letters, spaces, hyphens, and apostrophes
  const nameRegex = /^[a-zA-Z\s'-]+$/;
  return nameRegex.test(name.trim());
};

// Address validation
export const validateAddress = (address) => {
  const errors = [];
  
  if (!address.street || address.street.trim().length === 0) {
    errors.push('Street address is required');
  }
  
  if (!address.city || address.city.trim().length === 0) {
    errors.push('City is required');
  }
  
  if (!address.state || address.state.trim().length === 0) {
    errors.push('State is required');
  }
  
  if (!address.zipCode || !isValidZipCode(address.zipCode)) {
    errors.push('Valid ZIP code is required');
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
};

export const isValidZipCode = (zipCode) => {
  // US ZIP code format: 12345 or 12345-6789
  const zipRegex = /^\d{5}(-\d{4})?$/;
  return zipRegex.test(zipCode);
};

// URL validation
export const isValidURL = (url) => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

// Required field validation
export const isRequired = (value) => {
  if (value === null || value === undefined) {
    return false;
  }
  
  if (typeof value === 'string') {
    return value.trim().length > 0;
  }
  
  if (Array.isArray(value)) {
    return value.length > 0;
  }
  
  return true;
};

// Length validation
export const validateLength = (value, min = 0, max = Infinity) => {
  if (!value) {
    return {
      isValid: min === 0,
      error: min > 0 ? 'This field is required' : null
    };
  }
  
  const length = value.length;
  
  if (length < min) {
    return {
      isValid: false,
      error: `Must be at least ${min} characters long`
    };
  }
  
  if (length > max) {
    return {
      isValid: false,
      error: `Must be no more than ${max} characters long`
    };
  }
  
  return {
    isValid: true,
    error: null
  };
};

// Number validation
export const validateNumber = (value, min = -Infinity, max = Infinity) => {
  const num = parseFloat(value);
  
  if (isNaN(num)) {
    return {
      isValid: false,
      error: 'Must be a valid number'
    };
  }
  
  if (num < min) {
    return {
      isValid: false,
      error: `Must be at least ${min}`
    };
  }
  
  if (num > max) {
    return {
      isValid: false,
      error: `Must be no more than ${max}`
    };
  }
  
  return {
    isValid: true,
    error: null
  };
};

// Date validation
export const isValidDate = (dateString) => {
  const date = new Date(dateString);
  return date instanceof Date && !isNaN(date);
};

export const isDateInFuture = (dateString) => {
  const date = new Date(dateString);
  const now = new Date();
  return date > now;
};

export const isDateInPast = (dateString) => {
  const date = new Date(dateString);
  const now = new Date();
  return date < now;
};

// Age validation
export const validateAge = (birthDate, minAge = 0, maxAge = 150) => {
  const birth = new Date(birthDate);
  const today = new Date();
  
  if (!isValidDate(birthDate)) {
    return {
      isValid: false,
      error: 'Invalid birth date'
    };
  }
  
  if (birth > today) {
    return {
      isValid: false,
      error: 'Birth date cannot be in the future'
    };
  }
  
  const age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();
  
  const actualAge = monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate()) 
    ? age - 1 
    : age;
  
  if (actualAge < minAge) {
    return {
      isValid: false,
      error: `Must be at least ${minAge} years old`
    };
  }
  
  if (actualAge > maxAge) {
    return {
      isValid: false,
      error: `Must be no more than ${maxAge} years old`
    };
  }
  
  return {
    isValid: true,
    error: null,
    age: actualAge
  };
};

// Form validation helper
export const validateForm = (data, rules) => {
  const errors = {};
  let isValid = true;
  
  Object.keys(rules).forEach(field => {
    const fieldRules = rules[field];
    const value = data[field];
    
    fieldRules.forEach(rule => {
      if (errors[field]) return; // Skip if field already has an error
      
      const result = rule(value);
      if (!result.isValid) {
        errors[field] = result.error;
        isValid = false;
      }
    });
  });
  
  return {
    isValid,
    errors
  };
};

// Common validation rule creators
export const required = (message = 'This field is required') => {
  return (value) => ({
    isValid: isRequired(value),
    error: isRequired(value) ? null : message
  });
};

export const email = (message = 'Please enter a valid email address') => {
  return (value) => {
    if (!value) return { isValid: true, error: null };
    return {
      isValid: isValidEmail(value),
      error: isValidEmail(value) ? null : message
    };
  };
};

export const minLength = (min, message) => {
  return (value) => {
    const msg = message || `Must be at least ${min} characters long`;
    return validateLength(value, min, Infinity);
  };
};

export const maxLength = (max, message) => {
  return (value) => {
    const msg = message || `Must be no more than ${max} characters long`;
    return validateLength(value, 0, max);
  };
};

export const pattern = (regex, message = 'Invalid format') => {
  return (value) => {
    if (!value) return { isValid: true, error: null };
    return {
      isValid: regex.test(value),
      error: regex.test(value) ? null : message
    };
  };
};