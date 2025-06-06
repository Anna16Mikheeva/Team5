<template>
  <nav style="background: var(--primary); color: var(--white); padding: 1em;">
    <router-link to="/" style="font-weight: bold; margin-right: 2em; color: var(--white);">
      <img src="@/assets/logo.svg" alt="ТУСУР" style="height: 32px; vertical-align: middle; margin-right: 0.5em;" />
      ТУСУР
    </router-link>
    <router-link v-if="!user" to="/login" style="margin-right: 1em; color: var(--white);">Вход</router-link>
    <router-link v-if="!user" to="/register" style="margin-right: 1em; color: var(--white);">Регистрация</router-link>
    <router-link v-if="user" to="/profile" style="margin-right: 1em; color: var(--white);">Профиль</router-link>
    <router-link v-if="user" to="/application" style="margin-right: 1em; color: var(--white);">Моя анкета</router-link>
    <router-link v-if="user && user.role === 'admin'" to="/admin" style="margin-right: 1em; color: var(--white);">Админ-панель</router-link>
    <span v-if="user" style="margin-right: 1em;">{{ user.email }}</span>
    <button v-if="user" @click="logout" class="primary-btn" style="background: var(--secondary);">Выйти</button>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const user = computed(() => auth.user)

const logout = () => {
  auth.logout()
}
</script>
