import { useState, useEffect, useCallback } from 'react';
import { api } from '../services/api';

export const useApi = (url, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const {
    method = 'GET',
    body = null,
    headers = {},
    immediate = true,
    onSuccess,
    onError
  } = options;

  const execute = useCallback(async (overrideOptions = {}) => {
    try {
      setLoading(true);
      setError(null);

      const requestOptions = {
        method: overrideOptions.method || method,
        headers: {
          'Content-Type': 'application/json',
          ...headers,
          ...overrideOptions.headers
        },
        ...(overrideOptions.body || body ? { 
          body: JSON.stringify(overrideOptions.body || body) 
        } : {})
      };

      const response = await api.request(
        overrideOptions.url || url, 
        requestOptions
      );
      
      setData(response);
      
      if (onSuccess) {
        onSuccess(response);
      }
      
      return response;
    } catch (err) {
      setError(err);
      
      if (onError) {
        onError(err);
      }
      
      throw err;
    } finally {
      setLoading(false);
    }
  }, [url, method, body, headers, onSuccess, onError]);

  // Execute immediately if requested
  useEffect(() => {
    if (immediate && url) {
      execute();
    }
  }, [execute, immediate, url]);

  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setLoading(false);
  }, []);

  return {
    data,
    loading,
    error,
    execute,
    reset
  };
};

export default useApi;