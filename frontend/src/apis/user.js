import apiClient from './axios'

export const register = (email, username, password) => {
  return apiClient.post('/users/register', { email, username, password })
}

export const login = (email, password) => {
  return apiClient.post('/users/login', { email, password })
}