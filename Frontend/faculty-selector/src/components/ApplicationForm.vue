<template>
  <form @submit.prevent="onSubmit" class="card" novalidate>
    <h2>Анкета абитуриента</h2>

    <label>Фамилия</label>
    <input v-model="form.lastName" :readonly="readonly" required />

    <label>Имя</label>
    <input v-model="form.firstName" :readonly="readonly" required />

    <label>Отчество</label>
    <input v-model="form.patronymic" :readonly="readonly" />

    <label>Дата рождения</label>
    <input type="date" v-model="form.birthDate" :readonly="readonly" required />

    <label>Пол</label>
    <select v-model="form.gender" :disabled="readonly" required>
      <option value="мужской">Мужской</option>
      <option value="женский">Женский</option>
    </select>

    <label>Год окончания школы</label>
    <input type="number" v-model="form.gradYear" :readonly="readonly" min="2000" max="2100" required />

    <label>Факультет</label>
    <select v-model="form.faculty" :disabled="readonly" required>
      <option v-for="f in faculties" :key="f" :value="f">{{ f }}</option>
    </select>

    <label>Электронная почта для связи</label>
    <input type="email" v-model="form.contactEmail" :readonly="readonly" required />

    <label>Мобильный телефон</label>
    <input type="tel" v-model="form.phone" :readonly="readonly" required pattern="^((\\+7|7|8)+([0-9]){10})$" />

    <p v-if="error" class="form-error">{{ error }}</p>

    <button v-if="!readonly" type="submit" class="primary-btn" :disabled="loading">Отправить заявку</button>

    <p v-if="success" style="color: var(--success); margin-top: 1rem;">
      Ваша заявка успешно отправлена. Мы свяжемся с вами в ближайшее время по указанным контактам.
    </p>

    <button v-if="readonly" type="button" class="primary-btn" @click="editAgain" style="margin-top: 1rem;">
      Подать заявку заново
    </button>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'
import { useCookies } from 'vue3-cookies'

const { cookies } = useCookies()
const store = useAuthStore()

const faculties = [
  'ФВС', 'ФСУ', 'ФИТ', 'ЭФ', 'ГФ', 'ЮФ', 'ФБ', 'ЗиВФ', 'ФДО'
]

const readonly = ref(false)
const loading = ref(false)
const error = ref('')
const success = ref(false)

const form = ref({
  lastName: '',
  firstName: '',
  patronymic: '',
  birthDate: '',
  gender: 'мужской',
  gradYear: new Date().getFullYear(),
  faculty: cookies.get('selected_faculty') || faculties[0],
  contactEmail: '',
  phone: ''
})

onMounted(async () => {
  await store.fetchProfile()
  if (store.user) {
    form.value.lastName = store.user.lastName || ''
    form.value.firstName = store.user.firstName || ''
    form.value.patronymic = store.user.middleName || ''
    form.value.birthDate = store.user.birthDate || ''
    form.value.contactEmail = store.user.email || ''
  }
  try {
    const { data } = await api.get('/applications/mine')
    if (data) {
      Object.assign(form.value, data)
      readonly.value = true
      success.value = true
    }
  } catch {}
})

async function onSubmit() {
  error.value = ''
  success.value = false
  loading.value = true
  try {
    await api.post('/applications', form.value)
    success.value = true
    readonly.value = true
  } catch (e) {
    error.value = e.response?.data?.message || 'Ошибка отправки заявки'
  } finally {
    loading.value = false
  }
}

function editAgain() {
  readonly.value = false
  success.value = false
}
</script>
