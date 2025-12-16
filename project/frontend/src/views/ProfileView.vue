<!-- src/views/ProfileView.vue -->
<template>
  <div class="profile">
    <div class="avatar">
      👤
    </div>
    <h2>Мой канал</h2>
    <p>Загружено видео: {{ uploadedVideos.length }}</p>

    <div class="video-list">
      <VideoCard
        v-for="video in uploadedVideos"
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
    const uploadedVideos = [
      { id: 1, title: 'Мой первый урок', thumbnail: 'https://via.placeholder.com/320x180?text=My+Video' },
      { id: 5, title: 'Как я учу Vue', thumbnail: 'https://via.placeholder.com/320x180?text=Vue+Learn' }
    ]
    return { uploadedVideos }
  }
}
</script>

<style scoped>
.profile {
  padding: 30px;
  text-align: center;
}
.avatar {
  font-size: 60px;
  margin-bottom: 20px;
}
.video-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
</style>