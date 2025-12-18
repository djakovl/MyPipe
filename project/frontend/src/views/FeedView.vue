<!-- src/views/FeedView.vue -->
<template>
  <div class="feed">
    <h2>Лента видео</h2>

    <div v-if="loading" class="loading">Загрузка видео...</div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else class="video-grid">
      <VideoCard
        v-for="video in videos"
        :key="video.id"
        :video="{
          id: video.id,
          title: video.name,
          views: formatViews(video.views),
          uploader: getUploaderName(video.user_id),
        }"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import VideoCard from '@/components/VideoCard.vue'

// ⚠️ Замените на реальный способ получения имён (или добавьте /api/users/batch)
const mockUserNames = {
  '550e8400-e29b-41d4-a716-446655440000': 'Katya',
  '550e8400-e29b-41d4-a716-446655440001': 'Tanya'
}

export default {
  components: { VideoCard },
  setup() {
    const videos = ref([
      { id: 1, title: 'Как сделать YouTube-клон', views: '10K', uploader: 'Dev', thumbnail: 'https://via.placeholder.com/320x180?text=Video+1  ' },
      { id: 2, title: 'Vue 3 с нуля', views: '5K', uploader: 'Luna', thumbnail: 'https://via.placeholder.com/320x180?text=Video+2  ' },
      { id: 3, title: 'Роутинг в Vue', views: '2K', uploader: 'Frontend', thumbnail: 'https://via.placeholder.com/320x180?text=Video+3  ' },
      { id: 4, title: 'Комментарии и лайки', views: '1K', uploader: 'WebDev', thumbnail: 'https://via.placeholder.com/320x180?text=Video+4  ' },
    ])
    const loading = ref(false)
    const error = ref(null)

    const fetchVideos = async () => {
      try {
        loading.value = true
        error.value = null

        const res = await fetch('/api/videos')
        if (!res.ok) throw new Error('Не удалось загрузить видео')
        //videos.value = await res.json()
      } catch (err) {
        console.error('Ошибка загрузки ленты:', err)
        error.value = 'Не удалось загрузить видео. Попробуйте позже.'
      } finally {
        loading.value = false
      }
    }

    const formatViews = (views) => {
      if (views >= 1000) {
        return (views / 1000).toFixed(1) + 'K'
      }
      return views.toString()
    }

    const getUploaderName = (userId) => {
      // В идеале: загружать имена через /api/users/batch
      return mockUserNames[userId] || 'Аноним'
    }


    onMounted(() => {
      fetchVideos()
    })

    return {
      videos,
      loading,
      error,
      formatViews,
      getUploaderName
    }
  }
}
</script>

<style scoped>
.feed {
  padding: 24px 20px;
  max-width: 1400px;
  margin: 0 auto;
}
.feed h2 {
  font-size: 28px;
  margin-bottom: 24px;
  color: #222;
}

.loading,
.error {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #555;
}

.error {
  color: #d32f2f;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

/* Адаптивность */
@media (max-width: 768px) {
  .video-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 16px;
  }
}
</style>