<template>
  <div style="max-width: 800px; margin: 2em auto;">
    <h1>Добро пожаловать в сервис подбора факультета ТУСУР!</h1>
    <p>
      Здесь вы можете подобрать факультет на основе ваших интересов и отправить заявку на поступление.
    </p>
    <FacultySelector />
  </div>
</template>

<script setup>
import FacultySelector from '@/components/FacultySelector.vue'
</script>
