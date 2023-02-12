import apiClient from './api'
import { putToken } from './token'

interface AuthRequest {
  username: string
  password: string
}

interface AuthResponse {
  access_token: string
}

async function auth(username: string, password: string): Promise<any> {
  console.log(username, password)
  const resp = await apiClient.postForm<AuthRequest, AuthResponse>('/user/token', {
    username: username,
    password: password,
  })
  putToken(resp.access_token)
}

async function me(): Promise<any> {
  await apiClient.get<any>('/user/me')
}

export { auth, me }
