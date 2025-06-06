<template>
  <form @submit.prevent="onSubmit">
    <h2>Подбор факультета</h2>
    <label>Любимые предметы</label>
    <input v-model="likedSubjects" placeholder="Математика, Физика..." />
    <label>Нелюбимые предметы</label>
    <input v-model="dislikedSubjects" placeholder="Литература, История..." />
    <label>Экзамены (ЕГЭ)</label>
    <input v-model="exams" placeholder="Математика, Информатика..." />
    <label>Мне интересно</label>
    <textarea v-model="interests" placeholder="Опишите, что вам интересно"></textarea>
    <label>Мне неинтересно</label>
    <textarea v-model="notInterests" placeholder="Опишите, что вам неинтересно"></textarea>
    <button type="submit" class="primary-btn">Подобрать факультет</button>

    <div v-if="faculties.length" style="margin-top: 1em;">
      <h3>Рекомендуемые факультеты:</h3>
      <ul>
        <li v-for="f in faculties" :key="f.name">
          <b>{{ f.name }}</b> — {{ f.professions.join(', ') }}
          <button class="primary-btn" style="margin-left:1em" @click="apply(f.name)">Подать заявку</button>
        </li>
      </ul>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCookies } from 'vue3-cookies'

const likedSubjects = ref('')
const dislikedSubjects = ref('')
const exams = ref('')
const interests = ref('')
const notInterests = ref('')
const faculties = ref([])
const router = useRouter()
const { cookies } = useCookies()

const onSubmit = async () => {
  // Здесь должен быть запрос к нейросети/ML API
  // Для примера — имитация ответа:
  faculties.value = [
    { name: 'ФКТИ', professions: ['Программист', 'Инженер ПО'] },
    { name: 'ФРТ', professions: ['Радиоинженер', 'Системотехник'] }
  ]
}

const apply = (facultyName) => {
  cookies.set('selectedFaculty', facultyName)
  router.push('/register')
}
</script>
