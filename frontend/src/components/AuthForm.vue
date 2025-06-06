<template>
  <form @submit.prevent="handleSubmit" class="auth-form">
    <h2>{{ isLogin ? 'Вход' : 'Регистрация' }}</h2>
    
    <div class="form-group">
      <label>Email:</label>
      <input 
        type="email" 
        v-model="form.email" 
        required
        placeholder="Введите ваш email"
      >
    </div>
    
    <div v-if="!isLogin" class="form-group">
      <label>Фамилия:</label>
      <input 
        type="text" 
        v-model="form.lastName" 
        required
        placeholder="Введите вашу фамилию"
      >
    </div>
    
    <div v-if="!isLogin" class="form-group">
      <label>Имя:</label>
      <input 
        type="text" 
        v-model="form.firstName" 
        required
        placeholder="Введите ваше имя"
      >
    </div>
    
    <div v-if="!isLogin" class="form-group">
      <label>Отчество:</label>
      <input 
        type="text" 
        v-model="form.middleName" 
        placeholder="Введите ваше отчество (если есть)"
      >
    </div>
    
    <div v-if="!isLogin" class="form-group">
      <label>Дата рождения:</label>
      <input 
        type="date" 
        v-model="form.birthDate" 
        required
      >
    </div>
    
    <div class="form-group">
      <label>Пароль:</label>
      <input 
        type="password" 
        v-model="form.password" 
        :required="!isEdit"
        placeholder="Введите пароль"
      >
    </div>
    
    <div v-if="!isLogin" class="form-group">
      <label>Подтверждение пароля:</label>
      <input 
        type="password" 
        v-model="form.confirmPassword" 
        :required="!isEdit"
        placeholder="Повторите пароль"
      >
      <p v-if="form.password && form.password !== form.confirmPassword" class="error">
        Пароли не совпадают
      </p>
    </div>
    
    <button type="submit" class="submit-btn">
      {{ isLogin ? 'Войти' : 'Зарегистрироваться' }}
    </button>
    
    <p class="toggle-auth">
      {{ isLogin ? 'Нет аккаунта?' : 'Уже есть аккаунт?' }}
      <button type="button" @click="toggleAuthMode" class="text-btn">
        {{ isLogin ? 'Зарегистрироваться' : 'Войти' }}
      </button>
    </p>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useCookies } from 'vue3-cookies'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  isLogin: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['toggle-auth-mode'])

const router = useRouter()
const { cookies } = useCookies()
const authStore = useAuthStore()
    
const form = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  firstName: '',
  lastName: '',
  middleName: '',
  birthDate: ''
})
    
function toggleAuthMode() {
  emit('toggle-auth-mode')
}
    
async function handleSubmit() {
  if (!props.isLogin && form.password !== form.confirmPassword) {
    return
  }
  
  if (props.isLogin) {
    try {
      await authStore.login({
        email: form.email,
        password: form.password
      })
      
      const selectedFaculty = cookies.get('selected_faculty')
      if (selectedFaculty) {
        router.push('/application')
      } else {
        router.push('/profile')
      }
    } catch (error) {
      console.error('Ошибка входа:', error)
    }
  } else {
    try {
      await authStore.register({
        email: form.email,
        password: form.password,
        firstName: form.firstName,
        lastName: form.lastName,
        middleName: form.middleName,
        birthDate: form.birthDate
      })
      
      const selectedFaculty = cookies.get('selected_faculty')
      if (selectedFaculty) {
        router.push('/application')
      } else {
        router.push('/profile')
      }
    } catch (error) {
      console.error('Ошибка регистрации:', error)
    }
  }
}
</script>

<style scoped>
.auth-form {
  max-width: 500px;
  margin: 0 auto;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #3C388D;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.error {
  color: #e74c3c;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.submit-btn {
  background-color: #3C388D;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  width: 100%;
  transition: background-color 0.3s;
}

.submit-btn:hover {
  background-color: #652580;
}

.toggle-auth {
  text-align: center;
  margin-top: 1rem;
}

.text-btn {
  background: none;
  border: none;
  color: #3C388D;
  text-decoration: underline;
  cursor: pointer;
  padding: 0;
}

.text-btn:hover {
  color: #652580;
}
</style>