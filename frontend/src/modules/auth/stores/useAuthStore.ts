import { defineStore } from 'pinia'
import { ref, watch, onMounted } from 'vue'
import {
  getUser,
  loginWithEmail,
  signupWithEmail,
  loginWithOAuth,
  getAvailableOAuthProviders,
} from '../api'
import type { OAuthProvider } from '../types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const email = ref<string | null>(localStorage.getItem('email'))
  const availableProviders = ref<OAuthProvider[]>([])

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

  const fetchOAuthProviders = async () => {
    try {
      const response = await getAvailableOAuthProviders()
      availableProviders.value = response.data.providers
    } catch {
      availableProviders.value = []
    }
  }

  onMounted(fetchOAuthProviders)

  const login = async (emailInput: string, password: string) => {
    const response = await loginWithEmail({ email: emailInput, password })
    token.value = response.data.access_token
    email.value = emailInput
  }

  const signup = async (emailInput: string, password: string) => {
    const response = await signupWithEmail({ email: emailInput, password })
    token.value = response.data.access_token
    email.value = emailInput
  }

  const loginWithOAuthCode = async (provider: OAuthProvider, code: string) => {
    const response = await loginWithOAuth(provider, code)
    token.value = response.data.access_token
    await fetchCurrentUser()
  }

  const fetchCurrentUser = async () => {
    const response = await getUser()
    email.value = response.data.email
  }

  const logout = () => {
    token.value = null
    email.value = null
  }

  return {
    token,
    email,
    availableProviders,
    login,
    signup,
    loginWithOAuthCode,
    fetchCurrentUser,
    logout,
  }
})
