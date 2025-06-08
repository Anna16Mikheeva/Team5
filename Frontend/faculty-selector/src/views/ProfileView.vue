<template>
  <UserForm :user="user" :isNew="false" @saved="onSaved" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import UserForm from '@/components/UserForm.vue'

const auth = useAuthStore()
const user = ref(null)

onMounted(async () => {
  await auth.fetchProfile()
  user.value = auth.user
})

function onSaved() {
  alert('Профиль успешно обновлен!')
}
</script>
