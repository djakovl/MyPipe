<!-- src/views/VideoView.vue -->
<template>
  <div class="video-page">
    <div class="player">
      <!-- Используем HTML5-плеер -->
      <video controls width="100%">
        <source src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4" type="video/mp4">
        Ваш браузер не поддерживает видео.
      </video>
    </div>

    <div class="video-details">
      <h1>{{ video.title }}</h1>
      <div class="actions">
        <button @click="like">👍 {{ likes }}</button>
        <button @click="dislike">👎 {{ dislikes }}</button>
      </div>

      <div class="comments">
        <h3>Комментарии</h3>
        <p>Это mock-комментарий. Позже можно добавить форму и список.</p>
      </div>

      <div class="recommendations">
        <h3>Рекомендации</h3>
        <VideoCard
          v-for="v in recommended"
          :key="v.id"
          :video="v"
        />
      </div>
    </div>
  </div>
</template>

<script>
import VideoCard from '@/components/VideoCard.vue'
import { ref } from 'vue'

export default {
  components: { VideoCard },
  setup() {
    const video = { id: 1, title: 'Как сделать YouTube-клон' }
    const likes = ref(123)
    const dislikes = ref(5)

    const like = () => likes.value++
    const dislike = () => dislikes.value++

    const recommended = [
      { id: 2, title: 'Vue 3 с нуля', thumbnail: 'https://via.placeholder.com/160x90?text=Rec+1' },
      { id: 3, title: 'Роутинг в Vue', thumbnail: 'https://via.placeholder.com/160x90?text=Rec+2' }
    ]

    return { video, likes, dislikes, like, dislike, recommended }
  }
}
</script>

<style scoped>
.video-page {
  display: flex;
  gap: 24px;
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}
.player {
  flex: 3;
}
.video-details {
  flex: 1;
}
.actions button {
  margin-right: 10px;
  padding: 8px 16px;
  background: #f0f0f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.comments, .recommendations {
  margin-top: 20px;
}
.recommendations {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
</style>