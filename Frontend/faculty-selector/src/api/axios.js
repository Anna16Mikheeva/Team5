import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  withCredentials: true,  // Важно для отправки cookies
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Перехватчик для обработки ошибок
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
    }
    return Promise.reject(error)
  }
)

export default api