export interface AppConfig {
  env: 'development' | 'production' | 'demo'
  isDev: boolean
  isProd: boolean
  isDemo: boolean
  apiUrl: string
  frontendUrl: string
  version: string
}
