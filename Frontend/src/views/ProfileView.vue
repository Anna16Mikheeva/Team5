<template>
  <form @submit.prevent="onSave">
    <h2>Профиль пользователя</h2>
    <label>ID</label>
    <input :value="user.id" disabled />
    <label>Фамилия</label>
    <input v-model="lastName" />
    <label>Имя</label>
    <input v-model="firstName" />
    <label>Отчество</label>
    <input v-model="patronymic" />
    <label>Дата рождения</label>
    <input type="date" v-model="birthDate" />
    <label>Email</label>
    <input type="email" v-model="email" />
    <label>Пароль</label>
    <input type="password" v-model="password" placeholder="Оставьте пустым, если не хотите менять" />
    <label>Подтверждение пароля</label>
    <input type="password" v-model="passwordConfirm" />
    <button type="submit" class="primary-btn">Сохранить</button>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="saved" class="success">Профиль сохранён</p>
  </form>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const user = computed(() => auth.user)

const lastName = ref('')
const firstName = ref('')
const patronymic = ref('')
const birthDate = ref('')
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
const error = ref('')
const saved = ref(false)

watch(user, (val) => {
  if (val) {
    lastName.value = val.lastName
    firstName.value = val.firstName
    patronymic.value = val.patronymic
    birthDate.value = val.birthDate
    email.value = val.email
  }
}, { immediate: true })

const onSave = () => {
  if (password.value && password.value !== passwordConfirm.value) {
    error.value = 'Пароли не совпадают'
    return
  }
  // TODO: отправить на сервер
  error.value = ''
  saved.value = true
  setTimeout(() => saved.value = false, 3000)
}
</script>
