<template>
  <form @submit.prevent="onRegister">
    <h2>Регистрация</h2>
    <label>Email</label>
    <input v-model="email" type="email" required />
    <label>Фамилия</label>
    <input v-model="lastName" required />
    <label>Имя</label>
    <input v-model="firstName" required />
    <label>Отчество</label>
    <input v-model="patronymic" required />
    <label>Дата рождения</label>
    <input v-model="birthDate" type="date" required />
    <label>Пароль</label>
    <input v-model="password" type="password" required />
    <label>Подтверждение пароля</label>
    <input v-model="password2" type="password" required />
    <button type="submit" class="primary-btn">Зарегистрироваться</button>
    <p v-if="error" class="error">{{ error }}</p>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const email = ref('')
const lastName = ref('')
const firstName = ref('')
const patronymic = ref('')
const birthDate = ref('')
const password = ref('')
const password2 = ref('')
const error = ref('')
const auth = useAuthStore()
const router = useRouter()

const onRegister = async () => {
  if (password.value !== password2.value) {
    error.value = 'Пароли не совпадают'
    return
  }
  try {
    await auth.register({
      email: email.value,
      lastName: lastName.value,
      firstName: firstName.value,
      patronymic: patronymic.value,
      birthDate: birthDate.value,
      password: password.value
    })
    router.push('/profile')
  } catch {
    error.value = 'Ошибка регистрации'
  }
}
</script>

