<template>
  <form @submit.prevent="onSubmit" class="card" novalidate>
    <h2>Подбор профессии</h2>

    <label>Любимые предметы (через запятую)</label>
    <input v-model="form.lovedSubjectsInput" placeholder="Введите любимые предметы через запятую" type="text" autocomplete="off" />

    <label>Нелюбимые предметы (через запятую)</label>
    <input v-model="form.hatedSubjectsInput" placeholder="Введите нелюбимые предметы через запятую" type="text" autocomplete="off" />

    <label>Предметы для экзамена (через запятую)</label>
    <input v-model="form.examsInput" placeholder="Введите предметы экзаменов через запятую" type="text" autocomplete="off" required />

    <label>Мне интересно</label>
    <textarea v-model="form.interests" rows="3" required></textarea>

    <label>Мне неинтересно</label>
    <textarea v-model="form.notInterests" rows="3"></textarea>

    <button class="primary-btn" type="submit" :disabled="loading">
      {{ loading ? 'Подбираем...' : 'Подобрать факультет' }}
    </button>

    <p v-if="error" class="form-error">{{ error }}</p>

    <ul v-if="results.length" style="margin-top:1rem;" v-for="faculty in results" :key="faculty.name">
        <b>{{ faculty.name }}</b> — {{ faculty.professions.join(', ') }}
        <!--<button class="primary-btn" @click="apply(faculty.name)" style="margin-left: 1rem;">Подать заявку</button>-->
    </ul>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useCookies } from 'vue3-cookies'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const { cookies } = useCookies()
const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  lovedSubjectsInput: '',
  hatedSubjectsInput: '',
  examsInput: '',
  interests: '',
  notInterests: ''
})

const loading = ref(false)
const error = ref('')
const results = ref([])

function parseSubjects(input) {
  return input.split(',').map(s => s.trim()).filter(s => s.length > 0)
}

async function onSubmit() {
  error.value = ''
  results.value = []
  loading.value = true

  const lovedSubjects = parseSubjects(form.value.lovedSubjectsInput)
  const hatedSubjects = parseSubjects(form.value.hatedSubjectsInput)
  const exams = parseSubjects(form.value.examsInput)

  if (exams.length === 0) {
    error.value = 'Пожалуйста, укажите хотя бы один предмет для экзамена'
    loading.value = false
    return
  }

  try {
    const payload = {
      answers: [
        `Любимые предметы: ${lovedSubjects.join(', ')}. Нелюбимые предметы: ${hatedSubjects.join(', ')}`,
        form.value.interests,
        `Хочу развивать навыки в: ${exams.join(', ')}`,
        'Мои карьерные цели не указаны',
        exams.join(', '),
        form.value.notInterests
      ]
    }

    const response = await axios.post(
      'http://localhost:8000/api/analyze',
      payload,
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.token}`
        }
      }
    )

    // Преобразуем ответ GigaChat в структуру, ожидаемую фронтендом
    const recommendations = response.data.recommendations
    const faculties = recommendations.split('\n')
      .filter(line => line.trim().length > 0)
      .map(line => {
        const match = line.match(/^(.+?) - (.+)$/)
        return match ? {
          name: match[1].trim(),
          professions: [match[2].trim()]
        } : {
          name: line.trim(),
          professions: ['Рекомендуемая профессия']
        }
      })

    results.value = faculties
  } catch (e) {
    error.value = e.response?.data?.error || 'Ошибка при подборе факультета'
    console.error(e)
  } finally {
    loading.value = false
  }
}

function apply(facultyName) {
  cookies.set('selected_faculty', facultyName)
  router.push('/register')
}
</script>