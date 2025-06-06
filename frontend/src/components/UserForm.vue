<template>
  <form @submit.prevent="onSave" style="max-width: 500px; margin: 2em auto;">
    <h2>{{ user.id ? 'Редактирование' : 'Создание' }} пользователя</h2>
    <label>Фото</label>
    <input type="file" @change="onPhoto" />
    <label>ID</label>
    <input :value="user.id || '(будет сгенерирован)'" disabled />
    <label>Фамилия</label>
    <input v-model="user.lastName" required />
    <label>Имя</label>
    <input v-model="user.firstName" required />
    <label>Отчество</label>
    <input v-model="user.patronymic" required />
    <label>Дата рождения</label>
    <input v-model="user.birthDate" type="date" required />
    <label>Email</label>
    <input v-model="user.email" type="email" required />
    <label>Роль</label>
    <select v-model="user.role">
      <option value="user">Пользователь</option>
      <option value="admin">Администратор</option>
    </select>
    <label>Пароль</label>
    <input v-model="password" type="password" :required="!user.id" />
    <label>Подтверждение пароля</label>
    <input v-model="password2" type="password" :required="!user.id" />
    <button type="submit" class="primary-btn">Сохранить</button>
    <button type="button" @click="$emit('close')" style="margin-left: 1em;">Отмена</button>
    <p v-if="error" class="error">{{ error }}</p>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  user: Object
})

const emit = defineEmits(['close'])

const user = ref(props.user ? { ...props.user } : {
  lastName: '',
  firstName: '',
  patronymic: '',
  birthDate: '',
  email: '',
  role: 'user',
  photo: ''
})

const password = ref('')
const password2 = ref('')
const error = ref('')

watch(() => props.user, (val) => {
  if (val) user.value = { ...val }
})

const onPhoto = (event) => {
  // TODO: загрузка фото
}

const onSave = () => {
  if ((password.value || !user.value.id) && password.value !== password2.value) {
    error.value = 'Пароли не совпадают'
    return
  }
  // TODO: отправить данные на сервер
  emit('close')
}
</script>
