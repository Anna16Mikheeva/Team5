<template>
  <div>
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto mb-4"></div>
      <p class="text-lg font-medium text-gray-700">Анализируем ваши ответы...</p>
    </div>
    
    <div v-else>
      <h2 class="text-2xl font-bold mb-6 text-center">Ваши рекомендации</h2>
      <div class="prose max-w-none text-gray-700 whitespace-pre-line">
        {{ recommendations }}
      </div>
      
      <div class="mt-8 text-center">
        <button
          @click="$emit('restart')"
          class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Пройти тест заново
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  recommendations: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['restart'])
</script>