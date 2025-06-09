<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto">
      <!-- Шапка -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Помощник абитуриента</h1>
        <p class="mt-2 text-lg text-gray-600">Ответьте на вопросы, чтобы получить рекомендации по факультетам</p>
      </div>

      <!-- Прогресс-бар -->
      <ProgressBar :current-step="currentQuestionIndex" :total-steps="questions.length" />

      <!-- Контейнер вопросов -->
      <div class="bg-white shadow rounded-lg p-6 mb-8 transition-all duration-300">
        <Transition name="fade" mode="out-in">
          <div v-if="!showRecommendations">
            <!-- Текущий вопрос -->
            <div v-for="(question, index) in questions" 
                 :key="question.id" 
                 v-show="currentQuestionIndex === index">
              <h2 class="text-xl font-semibold mb-4">{{ question.text }}</h2>
              <p class="text-sm text-gray-500 mb-4">{{ question.hint }}</p>
              
              <textarea
                v-model="answers[question.id]"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows="5"
                placeholder="Введите ваш ответ..."
              ></textarea>
              
              <div class="flex justify-between mt-6">
                <button
                  v-if="currentQuestionIndex > 0"
                  @click="prevQuestion"
                  class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                >
                  Назад
                </button>
                <div v-else></div>
                
                <button
                  @click="nextQuestion"
                  :disabled="!answers[question.id]"
                  class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-blue-300"
                >
                  {{ isLastQuestion ? 'Получить рекомендации' : 'Далее' }}
                </button>
              </div>
            </div>
          </div>
          
          <!-- Результаты -->
          <RecommendationsView 
            v-else
            :recommendations="recommendations"
            @restart="restartQuiz"
            :loading="loading"
          />
        </Transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import ProgressBar from './components/ProgressBar.vue'
import RecommendationsView from './views/RecommendationsView.vue'

const questions = ref([])
const currentQuestionIndex = ref(0)
const answers = ref({})
const recommendations = ref('')
const loading = ref(false)
const showRecommendations = ref(false)

const isLastQuestion = computed(() => {
  return currentQuestionIndex.value === questions.value.length - 1
})

const fetchQuestions = async () => {
  try {
    const response = await axios.get('/api/questions')
    questions.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке вопросов:', error)
  }
}

const nextQuestion = () => {
  if (isLastQuestion.value) {
    submitAnswers()
  } else {
    currentQuestionIndex.value++
  }
}

const prevQuestion = () => {
  currentQuestionIndex.value--
}

const submitAnswers = async () => {
  loading.value = true
  try {
    const response = await axios.post('http://localhost:5000/api/analyze', {
      answers: Object.values(answers.value)
    })
    recommendations.value = response.data.recommendations
    showRecommendations.value = true
  } catch (error) {
    console.error('Ошибка при анализе ответов:', error)
    alert('Произошла ошибка при обработке ваших ответов. Пожалуйста, попробуйте позже.')
  } finally {
    loading.value = false
  }
}

const restartQuiz = () => {
  currentQuestionIndex.value = 0
  answers.value = {}
  recommendations.value = ''
  showRecommendations.value = false
}

onMounted(fetchQuestions)
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>