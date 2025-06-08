<template>
  <div class="card">
    <h2>Список пользователей</h2>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Фото</th>
          <th>ФИО</th>
          <th>Роль</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td><img :src="user.avatarUrl || '/default-avatar.png'" class="avatar" /></td>
          <td>{{ user.lastName }} {{ user.firstName }} {{ user.middleName }}</td>
          <td>{{ user.role === 'admin' ? 'Администратор' : 'Пользователь' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'

const users = ref([])

onMounted(async () => {
  try {
    const { data } = await api.get('/users')
    users.value = data
  } catch {
    users.value = []
  }
})
</script>
