<template>
  <form @submit.prevent="onSubmit" class="card" novalidate>
    <h3>{{ isNew ? 'Создать пользователя' : 'Редактировать пользователя' }}</h3>

    <label>Фамилия</label>
    <input type="text" v-model="form.lastName" required />

    <label>Имя</label>
    <input type="text" v-model="form.firstName" required />

    <label>Отчество</label>
    <input type="text" v-model="form.middleName" />

    <label>Дата рождения</label>
    <input type="date" v-model="form.birthDate" required />

    <label>Email</label>
    <input type="email" v-model="form.email" required />

    <label>Роль</label>
    <select v-model="form.role" required>
      <option value="user">Пользователь</option>
      <option value="admin">Администратор</option>
    </select>

    <label>Пароль</label>
    <input type="password" v-model="form.password" :required="isNew" />

    <label>Подтверждение пароля</label>
    <input type="password" v-model="form.confirmPassword" :required="isNew" />

    <p v-if="passwordMismatch" class="form-error">Пароли не совпадают</p>

    <button class="primary-btn" type="submit">Сохранить</button>

    <p v-if="error" class="form-error">{{ error }}</p>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue'
import api from '@/api/axios'

const props = defineProps({
  user: Object,
  isNew: Boolean
})
const emit = defineEmits(['saved'])

const form = ref({
  lastName: props.user?.lastName || '',
  firstName: props.user?.firstName || '',
  middleName: props.user?.middleName || '',
  birthDate: props.user?.birthDate || '',
  email: props.user?.email || '',
  role: props.user?.role || 'user',
  password: '',
  confirmPassword: ''
})

const error = ref('')
const passwordMismatch = ref(false)

watch(() => [form.value.password, form.value.confirmPassword], () => {
  passwordMismatch.value = form.value.password !== form.value.confirmPassword
})

async function onSubmit() {
  error.value = ''
  if (passwordMismatch.value) {
    error.value = 'Пароли не совпадают'
    return
  }
  try {
    if (props.isNew) {
      await api.post('/users', form.value)
    } else {
      await api.put(`/users/${props.user.id}`, form.value)
    }
    emit('saved')
  } catch (e) {
    error.value = e.response?.data?.message || 'Ошибка сохранения'
  }
}
</script>
