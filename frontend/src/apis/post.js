import apiClient from './axios'

export const getPosts = () => {
  return apiClient.get('/posts/')
}

export const createPost = (title, content) => {
  return apiClient.post('/posts/', { title, content })
}