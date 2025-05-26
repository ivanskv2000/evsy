import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/shared/utils/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null)
  const email = ref<string | null>(null)

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

  const logout = () => {
    token.value = null
    email.value = null
  }

  const fetchCurrentUser = async () => {
    const response = await api.get('/auth/me')
    email.value = response.data.email
  }

  return { token, email, login, signup, logout, fetchCurrentUser }
})
