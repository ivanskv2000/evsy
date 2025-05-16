// src/shared/composables/useAppConfig.ts

import { readonly } from 'vue'

type Env = 'dev' | 'prod' | 'demo'

interface AppConfig {
  env: Env
  isDev: boolean
  isProd: boolean
  isDemo: boolean
  apiUrl: string
  frontendUrl: string
  version: string
  logLevel: 'debug' | 'info' | 'warn' | 'error'
}

const env = (import.meta.env.VITE_ENV || 'prod') as Env

const config: AppConfig = {
  env,
  isDev: env === 'dev',
  isProd: env === 'prod',
  isDemo: env === 'demo',
  apiUrl: import.meta.env.VITE_API_URL ?? '',
  frontendUrl: import.meta.env.VITE_FRONTEND_URL ?? '',
  version: import.meta.env.VITE_APP_VERSION ?? '0.0.0',
  logLevel: (import.meta.env.VITE_LOG_LEVEL ?? 'info') as AppConfig['logLevel'],
}

export const useAppConfig = () => readonly(config)
