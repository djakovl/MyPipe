<!-- src/components/VideoCard.vue -->
<template>
  <router-link :to="`/watch/${video.id}`" class="video-card">
    <img :src="thumbnailUrl" :alt="video.name" />
    <div class="video-info">
      <h3>{{ video.name }}</h3>
      <p>{{ uploaderName }}</p>
      <small>{{ video.views }} просмотров</small>
    </div>
  </router-link>
</template>

<script>
export default {
  props: {
    video: {
      type: Object,
      required: true
    }
  },
  computed: {
    thumbnailUrl() {
      // Предполагаем, что превью лежат в public/thumbnails/
      return `sirius-logo.jpg`;
    },
    uploaderName() {
      // Временно: можно заменить на имя из store, если будет API пользователей
      return "Автор"; // или this.video.user_id, если нужно показывать ID
    }
  }
}
</script>

<style scoped>
.video-card {
  text-decoration: none;
  color: inherit;
  display: block;
}
.video-card img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  object-fit: cover;
}
.video-info {
  margin-top: 8px;
}
.video-info h3 {
  font-size: 16px;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
.video-info p {
  font-size: 14px;
  color: #666;
  margin: 4px 0;
}
.video-info small {
  font-size: 12px;
  color: #999;
}
</style>