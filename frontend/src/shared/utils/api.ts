import axios from 'axios'

if (!import.meta.env.VITE_API_URL) {
  throw new Error('VITE_API_URL is not defined in your environment variables')
}

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.response.use(
  response => response,
  error => Promise.reject(error)
)
