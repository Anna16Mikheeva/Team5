<template>
  <AuthForm :isLogin="false" @toggle-auth-mode="goLogin" />
</template>

<script setup>
import AuthForm from '@/components/AuthForm.vue'
import { useRouter } from 'vue-router'
const router = useRouter()
function goLogin() {
  router.push('/login')
}
</script>
