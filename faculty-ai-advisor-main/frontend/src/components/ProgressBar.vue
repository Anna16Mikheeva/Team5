<template>
  <div class="mb-8">
    <div class="flex justify-between mb-2">
      <span class="text-sm font-medium text-gray-700">Прогресс</span>
      <span class="text-sm font-medium text-gray-700">{{ currentStep + 1 }}/{{ totalSteps }}</span>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-2.5">
      <div 
        class="bg-blue-600 h-2.5 rounded-full transition-all duration-500" 
        :style="{ width: `${((currentStep + 1) / totalSteps) * 100}%` }"
      ></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  currentStep: {
    type: Number,
    required: true
  },
  totalSteps: {
    type: Number,
    required: true
  }
})
</script>