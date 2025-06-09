<template>
  <form @submit.prevent="onSubmit">
    <h2>Анкета абитуриента</h2>
    <label>Фамилия</label>
    <input v-model="form.lastName" :readonly="readonly" />
    <label>Имя</label>
    <input v-model="form.firstName" :readonly="readonly" />
    <label>Отчество</label>
    <input v-model="form.patronymic" :readonly="readonly" />
    <label>Дата рождения</label>
    <input type="date" v-model="form.birthDate" :readonly="readonly" />
    <label>Пол</label>
    <select v-model="form.gender" :disabled="readonly">
      <option value="мужской">Мужской</option>
      <option value="женский">Женский</option>
    </select>
    <label>Год окончания школы</label>
    <input type="number" v-model="form.gradYear" :readonly="readonly" />
    <label>Факультет</label>
    <select v-model="form.faculty" :disabled="readonly">
      <option v-for="f in faculties" :key="f" :value="f">{{ f }}</option>
    </select>
    <label>Электронная почта для связи</label>
    <input type="email" v-model="form.contactEmail" :readonly="readonly" />
    <label>Мобильный телефон</label>
    <input type="tel" v-model="form.phone" :readonly="readonly" />
    <button v-if="!readonly" type="submit" class="primary-btn">Отправить заявку</button>
  </form>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCookies } from 'vue3-cookies'

const props = defineProps({ readonly: Boolean })
const emit = defineEmits(['submitted'])

const store = useAuthStore()
const { cookies } = useCookies()

const faculties = ref(['ФКТИ', 'ФРТ', 'РТФ', 'ФЭТ', 'ФВТ'])

const user = computed(() => store.user)

const form = ref({
  lastName: user.value?.lastName || '',
  firstName: user.value?.firstName || '',
  patronymic: user.value?.patronymic || '',
  birthDate: user.value?.birthDate || '',
  gender: 'мужской',
  gradYear: new Date().getFullYear(),
  faculty: cookies.get('selectedFaculty') || faculties.value[0],
  contactEmail: user.value?.email || '',
  phone: ''
})

const onSubmit = () => {
  // TODO: отправить данные на сервер
  emit('submitted')
}
</script>
