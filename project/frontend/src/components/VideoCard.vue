<!-- src/components/VideoCard.vue -->
<template>
  <router-link :to="`/watch/${video.id}`" class="video-card">
    <img :src="video.thumbnail" :alt="video.title" />
    <div class="video-info">
      <h3>{{ video.title }}</h3>
      <p>{{ video.uploader }}</p>
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
  border-radius: 8px;
}
.video-info {
  margin-top: 8px;
}
.video-info h3 {
  font-size: 16px;
  margin-bottom: 4px;
}
</style>