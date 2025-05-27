import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { api } from '@/shared/utils/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const email = ref<string | null>(localStorage.getItem('email'))

  watch(token, newToken => {
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  })

  watch(email, newEmail => {
    if (newEmail) {
      localStorage.setItem('email', newEmail)
    } else {
      localStorage.removeItem('email')
    }
  })

  const login = async (emailInput: string, password: string) => {
    const response = await api.post('/auth/login', {
      email: emailInput,
      password,
    })
    token.value = response.data.access_token
    email.value = emailInput
  }

  const signup = async (emailInput: string, password: string) => {
    const response = await api.post('/auth/signup', {
      email: emailInput,
      password,
    })
    token.value = response.data.access_token
    email.value = emailInput
  }

  const loginWithOAuthCode = async (provider: 'google' | 'github', code: string) => {
    const response = await api.post('/auth/oauth', {
      provider,
      token: code, // this is the authorization code, not a token!
    })
    token.value = response.data.access_token
    await fetchCurrentUser()
  }

  const fetchCurrentUser = async () => {
    const response = await api.get('/auth/me')
    email.value = response.data.email
  }

  const logout = () => {
    token.value = null
    email.value = null
  }

  return {
    token,
    email,
    login,
    signup,
    loginWithOAuthCode,
    fetchCurrentUser,
    logout,
  }
})
