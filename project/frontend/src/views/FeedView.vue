<!-- src/views/FeedView.vue -->
<template>
  <div class="feed">
    <h2>Лента видео</h2>
    <div class="video-grid">
      <VideoCard
        v-for="video in videos"
        :key="video.id"
        :video="video"
      />
    </div>
  </div>
</template>

<script>
import VideoCard from '@/components/VideoCard.vue'

export default {
  components: { VideoCard },
  setup() {
    // Mock-данные
    const videos = [
      { id: 1, title: 'Как сделать YouTube-клон', views: '10K', uploader: 'Dev', thumbnail: 'https://via.placeholder.com/320x180?text=Video+1' },
      { id: 2, title: 'Vue 3 с нуля', views: '5K', uploader: 'Luna', thumbnail: 'https://via.placeholder.com/320x180?text=Video+2' },
      { id: 3, title: 'Роутинг в Vue', views: '2K', uploader: 'Frontend', thumbnail: 'https://via.placeholder.com/320x180?text=Video+3' },
      { id: 4, title: 'Комментарии и лайки', views: '1K', uploader: 'WebDev', thumbnail: 'https://via.placeholder.com/320x180?text=Video+4' },
    ]

    return { videos }
  }
}
</script>

<style scoped>
.feed {
  padding: 20px;
}
.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
</style>