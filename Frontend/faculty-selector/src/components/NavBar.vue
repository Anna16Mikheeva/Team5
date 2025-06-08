<template>
  <nav class="navbar">
    <div class="nav-left">
      <!-- Белый логотип ТУСУР слева -->
      <router-link to="/" class="logo-link" aria-label="Главная страница">
        <svg
          width="120"
          height="32"
          viewBox="0 0 120 32"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          class="logo"
          role="img"
        >
          <g>
            <path fill-rule="evenodd" clip-rule="evenodd" d="M13.1 29L13.13 9.2H21.2V3.5H0V9.2H8.07V29H13.1Z" fill="#FFFFFF"/>
            <path fill-rule="evenodd" clip-rule="evenodd" d="M114.2 3.5H99L98.97 28.97H103.8V23.1H114.17C117.6 23.1 120 20.7 120 17.3V12.3C120.03 8.9 117.63 6.5 114.2 6.5V3.5ZM115.2 19.1H103.8V9.2H115.2V19.1Z" fill="#FFFFFF"/>
            <path fill-rule="evenodd" clip-rule="evenodd" d="M55.9 29H69.1V23.3H54.9V9.2H69.1V3.5H55.9C52.5 3.5 50.1 5.9 50.1 9.3V22.7C50.1 26.1 52.5 28.5 55.9 28.5Z" fill="#FFFFFF"/>
            <path fill-rule="evenodd" clip-rule="evenodd" d="M37 28.97L47.6 3.5H42.5L36.1 15.8L29 3.5H23.9L31 17.1C31.6 18.2 32.7 18.9 34 18.9L34.03 18.9L31.4 28.97H37Z" fill="#FFFFFF"/>
            <path fill-rule="evenodd" clip-rule="evenodd" d="M83.2 18.9L83.23 18.9L80.6 28.97H86.2L96.8 3.5H91.7L85.3 15.8L78.2 3.5H73.1L80.2 17.1C80.8 18.2 81.9 18.9 83.2 18.9Z" fill="#FFFFFF"/>
          </g>
        </svg>
      </router-link>
    </div>

    <div class="nav-right">
      <router-link v-if="!user" to="/login" class="nav-link">Вход</router-link>
      <!--<router-link v-if="!user" to="/register" class="nav-link">Регистрация</router-link>-->

      <!--<router-link v-if="user" to="/profile" class="nav-link">Профиль</router-link>-->
      <!--<router-link v-if="user" to="/application" class="nav-link">Моя анкета</router-link>-->
      <router-link v-if="user && user.role === 'admin'" to="/admin" class="nav-link">Админ-панель</router-link>
      <span v-if="user" class="user-email">{{ user.email }}</span>
      <button v-if="user" @click="logout" class="primary-btn">Выйти</button>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const store = useAuthStore()
const user = computed(() => store.user)
const logout = () => store.logout()
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #3C388D; /* фирменный сине-фиолетовый цвет */
  padding: 1rem 2rem;
  color: white;
}

.nav-left {
  display: flex;
  align-items: center;
}

.logo {
  height: 32px;
  width: auto;
  cursor: pointer;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-link {
  color: white;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s;
}

.nav-link:hover {
  color: white; /* без голубого акцента */
}

.user-email {
  font-weight: 600;
  margin-right: 1rem;
}

.primary-btn {
  background: transparent; /* фирменный фиолетовый */
  border: none;
  color: white;
  padding: 0.5em 1em;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s;
}

.primary-btn:hover {
  background: transparent; /* более тёмный фиолетовый без голубого */
  color: white;
}
</style>
