<!-- src/views/FeedView.vue -->
<template>
  <div class="feed">
    <h2>Лента видео</h2>
    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-else-if="error" class="error">Ошибка загрузки: {{ error }}</div>
    <div v-else class="video-grid">
      <VideoCard
        v-for="video in videos"
        :key="video.id"
        :video="video"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import VideoCard from '@/components/VideoCard.vue'

export default {
  components: { VideoCard },
  setup() {
    const videos = ref([])
    const loading = ref(true)
    const error = ref(null)

    const formatDate = (isoString) => {
      const date = new Date(isoString)
      return new Intl.DateTimeFormat('ru-RU', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
      }).format(date)
    }

    const formatViews = (views) => {
      if (views >= 1000) {
        return (views / 1000).toFixed(1).replace(/\.0$/, '') + 'K'
      }
      return views.toString()
    }

    onMounted(async () => {
      try {
        const response = await fetch('http://localhost:8000/api/videos')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        // Добавляем вычисляемые поля для удобства отображения
        videos.value = data.map(video => ({
          ...video,
          formattedDate: formatDate(video.date),
          formattedViews: formatViews(video.views)
        }))
      } catch (err) {
        error.value = err.message
        console.error('Ошибка при загрузке видео:', err)
      } finally {
        loading.value = false
      }
    })

    return {
      videos,
      loading,
      error
    }
  }
}
</script>

<style scoped>
.feed {
  padding: 20px;
}

.loading,
.error {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #555;
}

.error {
  color: #e53935;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
</style>