<template>
  <form @submit.prevent="handleSubmit" class="card" style="max-width: 320px; margin: auto;">
    <h2>{{ isLogin ? 'Вход' : 'Регистрация' }}</h2>

    <label>Email</label>
    <input type="email" v-model="form.email" required />

    <label v-if="!isLogin">Фамилия</label>
    <input v-if="!isLogin" type="text" v-model="form.lastName" required />

    <label v-if="!isLogin">Имя</label>
    <input v-if="!isLogin" type="text" v-model="form.firstName" required />

    <label v-if="!isLogin">Отчество</label>
    <input v-if="!isLogin" type="text" v-model="form.middleName" />

    <label v-if="!isLogin">Дата рождения</label>
    <input v-if="!isLogin" type="date" v-model="form.birthDate" required />

    <label>Пароль</label>
    <input type="password" v-model="form.password" required minlength="6" />

    <label v-if="!isLogin">Подтверждение пароля</label>
    <input v-if="!isLogin" type="password" v-model="form.confirmPassword" required minlength="6" />

    <p v-if="passwordMismatch" class="form-error">Пароли не совпадают</p>

    <button class="primary-btn" type="submit" :disabled="loading">{{ isLogin ? 'Войти' : 'Зарегистрироваться' }}</button>

    <p style="margin-top: 1rem;">
      {{ isLogin ? 'Нет аккаунта?' : 'Уже есть аккаунт?' }}
      <button type="button" @click="toggleMode" class="primary-btn" style="background:#36CCE8; color:#3C388D; margin-left:0.5rem;">
        {{ isLogin ? 'Зарегистрироваться' : 'Войти' }}
      </button>
    </p>

    <p v-if="error" class="form-error">{{ error }}</p>
  </form>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const isLogin = ref(true)
const loading = ref(false)
const error = ref('')

const form = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  firstName: '',
  lastName: '',
  middleName: '',
  birthDate: ''
})

const passwordMismatch = computed(() => !isLogin.value && form.password !== form.confirmPassword && form.confirmPassword.length > 0)

function toggleMode() {
  isLogin.value = !isLogin.value
  error.value = ''
}

async function handleSubmit() {
  error.value = ''
  if (!isLogin.value && passwordMismatch.value) {
    error.value = 'Пароли не совпадают'
    return
  }
  loading.value = true
  try {
    if (isLogin.value) {
      await auth.login({ email: form.email, password: form.password })
    } else {
      await auth.register({
        name: form.firstName,
        lastName: form.lastName,
        patronymic: form.middleName,
        email: form.email,
        password: form.password,
        birthDate: form.birthDate
      })
    }
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.error || 'Ошибка авторизации'
  } finally {
    loading.value = false
  }
}
</script>