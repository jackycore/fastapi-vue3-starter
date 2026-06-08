import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const apiClient = axios.create({
  baseURL: '/api',  // 通过vite代理转发到后端
  headers: {
    'Content-Type': 'application/json'
  }
})

apiClient.interceptors.request.use(config => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
})

export default apiClient