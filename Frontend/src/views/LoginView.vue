<template>
  <form @submit.prevent="onLogin">
    <h2>Вход</h2>
    <label>Email</label>
    <input v-model="email" type="email" required />
    <label>Пароль</label>
    <input v-model="password" type="password" required />
    <button type="submit" class="primary-btn">Войти</button>
    <p v-if="error" class="error">{{ error }}</p>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref('')
const auth = useAuthStore()
const router = useRouter()

const onLogin = async () => {
  try {
    await auth.login({ email: email.value, password: password.value })
    router.push('/profile')
  } catch {
    error.value = 'Неверный логин или пароль'
  }
}
</script>
