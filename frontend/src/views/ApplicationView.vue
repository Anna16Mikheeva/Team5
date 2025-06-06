<template>
  <div>
    <div v-if="submitted" class="success" style="padding:1em; border-radius: 8px;">
      Ваша заявка успешно отправлена. Мы свяжемся с вами в ближайшее время по указанным вами контактам.
      <button class="primary-btn" @click="editAgain" style="margin-left: 1em;">Подать заявку заново</button>
    </div>
    <ApplicationForm
      v-if="!submitted || editing"
      :readonly="submitted && !editing"
      @submitted="onSubmitted"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ApplicationForm from '@/components/ApplicationForm.vue'

const submitted = ref(false)
const editing = ref(false)

const onSubmitted = () => {
  submitted.value = true
  editing.value = false
}

const editAgain = () => {
  editing.value = true
}
</script>

