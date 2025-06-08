import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(null)
  const router = useRouter()

  async function login(credentials) {
    try {
      const response = await axios.post('http://localhost:8000/api/login', credentials)
      user.value = response.data.user
      token.value = response.data.token
      localStorage.setItem('token', token.value)
    } catch (error) {
      throw error
    }
  }

  async function register(userData) {
    try {
      const response = await axios.post('http://localhost:8000/api/register', userData)
      user.value = response.data.user
      token.value = response.data.token
      localStorage.setItem('token', token.value)
    } catch (error) {
      throw error
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    router.push('/login')
  }

  return { user, token, login, register, logout }
})