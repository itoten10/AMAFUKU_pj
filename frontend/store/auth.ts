import { create } from 'zustand'
import { api } from '@/lib/api'

interface User {
  id: number
  username: string
  email: string
  full_name?: string
  total_score: number
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  login: (username: string, password: string) => Promise<void>
  register: (data: {
    username: string
    email: string
    password: string
    full_name?: string
  }) => Promise<void>
  logout: () => void
  fetchUser: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,

  login: async (username, password) => {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)

    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    localStorage.setItem('access_token', response.data.access_token)
    
    const userResponse = await api.get('/users/me')
    set({ user: userResponse.data, isAuthenticated: true })
  },

  register: async (data) => {
    await api.post('/auth/register', data)
  },

  logout: () => {
    localStorage.removeItem('access_token')
    set({ user: null, isAuthenticated: false })
  },

  fetchUser: async () => {
    try {
      const response = await api.get('/users/me')
      set({ user: response.data, isAuthenticated: true })
    } catch (error) {
      set({ user: null, isAuthenticated: false })
    }
  },
}))