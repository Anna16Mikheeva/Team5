<template>
  <AuthForm :isLogin="true" @toggle-auth-mode="goRegister" />
</template>

<script setup>
import AuthForm from '@/components/AuthForm.vue'
import { useRouter } from 'vue-router'
const router = useRouter()
function goRegister() {
  router.push('/register')
}
</script>
