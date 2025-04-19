import axios from 'axios'

const baseURL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1'

export const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // You can add custom error handling here
    return Promise.reject(error)
  }
) 