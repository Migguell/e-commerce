import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { productService } from '../services/productService';
import { categoryService } from '../services/categoryService';

const ProductContext = createContext();

const productReducer = (state, action) => {
  switch (action.type) {
    case 'SET_PRODUCTS':
      return {
        ...state,
        products: action.payload,
        loading: false
      };
    case 'SET_CATEGORIES':
      return {
        ...state,
        categories: action.payload
      };
    case 'SET_FILTERS':
      return {
        ...state,
        filters: { ...state.filters, ...action.payload }
      };
    case 'SET_SEARCH_QUERY':
      return {
        ...state,
        searchQuery: action.payload
      };
    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
        loading: false
      };
    case 'SET_PAGINATION':
      return {
        ...state,
        pagination: { ...state.pagination, ...action.payload }
      };
    default:
      return state;
  }
};

const initialState = {
  products: [],
  categories: [],
  loading: false,
  error: null,
  searchQuery: '',
  filters: {
    category: '',
    minPrice: '',
    maxPrice: '',
    sortBy: 'name',
    sortOrder: 'asc'
  },
  pagination: {
    currentPage: 1,
    totalPages: 1,
    totalItems: 0,
    itemsPerPage: 12
  }
};

export const ProductProvider = ({ children }) => {
  const [state, dispatch] = useReducer(productReducer, initialState);

  // Load initial data
  useEffect(() => {
    loadProducts();
    loadCategories();
  }, []);

  // Reload products when filters change
  useEffect(() => {
    loadProducts();
  }, [state.filters, state.searchQuery, state.pagination.currentPage]);

  const loadProducts = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      
      const params = {
        page: state.pagination.currentPage,
        limit: state.pagination.itemsPerPage,
        search: state.searchQuery,
        category: state.filters.category,
        minPrice: state.filters.minPrice,
        maxPrice: state.filters.maxPrice,
        sortBy: state.filters.sortBy,
        sortOrder: state.filters.sortOrder
      };

      const response = await productService.getProducts(params);
      
      dispatch({ type: 'SET_PRODUCTS', payload: response.products });
      dispatch({ 
        type: 'SET_PAGINATION', 
        payload: {
          totalPages: response.totalPages,
          totalItems: response.totalItems
        }
      });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
    }
  };

  const loadCategories = async () => {
    try {
      const categories = await categoryService.getCategories();
      dispatch({ type: 'SET_CATEGORIES', payload: categories });
    } catch (error) {
      console.error('Failed to load categories:', error);
    }
  };

  const setSearchQuery = (query) => {
    dispatch({ type: 'SET_SEARCH_QUERY', payload: query });
    dispatch({ type: 'SET_PAGINATION', payload: { currentPage: 1 } });
  };

  const setFilters = (newFilters) => {
    dispatch({ type: 'SET_FILTERS', payload: newFilters });
    dispatch({ type: 'SET_PAGINATION', payload: { currentPage: 1 } });
  };

  const setCurrentPage = (page) => {
    dispatch({ type: 'SET_PAGINATION', payload: { currentPage: page } });
  };

  const clearFilters = () => {
    dispatch({ 
      type: 'SET_FILTERS', 
      payload: {
        category: '',
        minPrice: '',
        maxPrice: '',
        sortBy: 'name',
        sortOrder: 'asc'
      }
    });
    dispatch({ type: 'SET_SEARCH_QUERY', payload: '' });
  };

  const getProductById = (id) => {
    return state.products.find(product => product.id === id);
  };

  const getFilteredProducts = () => {
    let filtered = [...state.products];

    // Apply search filter
    if (state.searchQuery) {
      const query = state.searchQuery.toLowerCase();
      filtered = filtered.filter(product => 
        product.name.toLowerCase().includes(query) ||
        product.description.toLowerCase().includes(query)
      );
    }

    // Apply category filter
    if (state.filters.category) {
      filtered = filtered.filter(product => 
        product.category_id === parseInt(state.filters.category)
      );
    }

    // Apply price filters
    if (state.filters.minPrice) {
      filtered = filtered.filter(product => 
        product.price >= parseFloat(state.filters.minPrice)
      );
    }

    if (state.filters.maxPrice) {
      filtered = filtered.filter(product => 
        product.price <= parseFloat(state.filters.maxPrice)
      );
    }

    // Apply sorting
    filtered.sort((a, b) => {
      const { sortBy, sortOrder } = state.filters;
      let aValue = a[sortBy];
      let bValue = b[sortBy];

      if (typeof aValue === 'string') {
        aValue = aValue.toLowerCase();
        bValue = bValue.toLowerCase();
      }

      if (sortOrder === 'asc') {
        return aValue > bValue ? 1 : -1;
      } else {
        return aValue < bValue ? 1 : -1;
      }
    });

    return filtered;
  };

  const value = {
    ...state,
    loadProducts,
    loadCategories,
    setSearchQuery,
    setFilters,
    setCurrentPage,
    clearFilters,
    getProductById,
    getFilteredProducts
  };

  return (
    <ProductContext.Provider value={value}>
      {children}
    </ProductContext.Provider>
  );
};

export const useProducts = () => {
  const context = useContext(ProductContext);
  if (!context) {
    throw new Error('useProducts must be used within a ProductProvider');
  }
  return context;
};

export default ProductContext;