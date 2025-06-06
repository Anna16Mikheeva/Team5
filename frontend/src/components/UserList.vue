<template>
  <table style="width: 100%; border-collapse: collapse;">
    <thead>
      <tr style="background: var(--primary); color: var(--white);">
        <th>ID</th>
        <th>Фото</th>
        <th>ФИО</th>
        <th>Роль</th>
        <th>Действия</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="user in users" :key="user.id" style="border-bottom: 1px solid #ccc;">
        <td>{{ user.id }}</td>
        <td><img :src="user.photo || placeholder" alt="Фото" style="height: 40px; border-radius: 50%;" /></td>
        <td>{{ user.lastName }} {{ user.firstName }} {{ user.patronymic }}</td>
        <td>{{ user.role }}</td>
        <td>
          <button class="primary-btn" @click="editUser(user)">Редактировать</button>
        </td>
      </tr>
    </tbody>
  </table>
  <UserForm v-if="editingUser" :user="editingUser" @close="editingUser = null" />
</template>

<script setup>
import { ref } from 'vue'
import UserForm from './UserForm.vue'

const placeholder = 'https://via.placeholder.com/40'
const users = ref([
  { id: 1, lastName: 'Админ', firstName: 'Администратор', patronymic: '', role: 'admin', photo: '' },
  { id: 2, lastName: 'Иванов', firstName: 'Иван', patronymic: 'Иванович', role: 'user', photo: '' }
])

const editingUser = ref(null)

const editUser = (user) => {
  editingUser.value = { ...user }
}
</script>
