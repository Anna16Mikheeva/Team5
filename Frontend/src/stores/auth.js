import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null
  }),
  actions: {
    async login({ email, password }) {
      // Реализуйте запрос к API для логина
      // Для теста - имитация:
      if (email === 'admin@tusur.ru' && password === 'admin123') {
        this.user = { id: 1, email, role: 'admin', lastName: 'Админ', firstName: 'Администратор' }
        this.token = 'admin-token'
      } else {
        this.user = { id: 2, email, role: 'user', lastName: 'Иванов', firstName: 'Иван' }
        this.token = 'user-token'
      }
    },
    async register(userData) {
      // Реализуйте запрос к API для регистрации
      this.user = { ...userData, id: 3, role: 'user' }
      this.token = 'new-user-token'
    },
    logout() {
      this.user = null
      this.token = null
    }
  }
})
