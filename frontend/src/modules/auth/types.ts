export interface UserInfo {
  email: string
}

export interface UserCredentials {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}
export type SignupResponse = LoginResponse
export type OAuthResponse = LoginResponse
export type OAuthProvider = 'google' | 'github'
