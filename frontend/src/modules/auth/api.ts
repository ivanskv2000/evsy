import { api } from '@/shared/utils/api'
import type {
  UserInfo,
  UserCredentials,
  LoginResponse,
  SignupResponse,
  OAuthResponse,
  OAuthProvider,
} from './types'

export const getUser = () => api.get<UserInfo>('/auth/me')

export const loginWithEmail = (payload: UserCredentials) =>
  api.post<LoginResponse>('/auth/login', payload)

export const signupWithEmail = (payload: UserCredentials) =>
  api.post<SignupResponse>('/auth/signup', payload)

export const loginWithOAuth = (provider: OAuthProvider, code: string) =>
  api.post<OAuthResponse>('/auth/oauth', {
    provider,
    token: code,
  })
