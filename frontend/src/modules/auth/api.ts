import { api } from '@/shared/utils/api'
import type { UserInfo } from './types'

export const fetchCurrentUser = () => api.get<UserInfo>('/auth/me')