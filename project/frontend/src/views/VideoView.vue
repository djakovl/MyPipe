<!-- src/views/VideoView.vue -->
<template>
  <div class="video-page">
    <div class="player">
      <video v-if="videoSrc" :src="videoSrc" controls preload="metadata" />
      <div v-else class="placeholder">Загрузка видео...</div>
    </div>

    <div class="video-details">
      <h1>{{ currentVideo?.name || 'Загрузка...' }}</h1>
      <p class="description">{{ currentVideo?.description || 'Описание недоступно' }}</p>

      <div class="actions">
        <button @click="like" :disabled="loading">👍 {{ currentVideo?.likes || 0 }}</button>
        <button @click="dislike" :disabled="loading">👎 {{ currentVideo?.dislikes || 0 }}</button>
        <span class="views">👁️ {{ currentVideo?.views || 0 }}</span>
      </div>

      <!-- Форма комментария -->
      <div class="add-comment">
        <textarea
          v-model="newCommentText"
          placeholder="Напишите комментарий..."
          :disabled="loading || !currentUser"
        ></textarea>
        <button @click="postComment" :disabled="!newCommentText.trim() || loading">
          Отправить
        </button>
      </div>

      <!-- Комментарии -->
      <div class="comments-section">
        <h3>Комментарии ({{ comments.length }})</h3>
        <div v-if="loadingComments">Загрузка комментариев...</div>
        <div v-else-if="comments.length === 0">Комментариев пока нет.</div>
        <div v-else>
          <CommentItem
            v-for="comment in rootComments"
            :key="comment.id"
            :comment="comment"
            :all-comments="comments"
            :users="usersMap"
          />
        </div>
      </div>

      <!-- Рекомендации -->
      <div class="recommendations">
        <h3>Рекомендации</h3>
        <VideoCard
          v-for="v in recommendedVideos"
          :key="v.id"
          :video="v"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import VideoCard from '@/components/VideoCard.vue'
import CommentItem from '@/components/CommentItem.vue'

// ⚠️ ЗАМЕНИТЕ НА ID ТЕКУЩЕГО ПОЛЬЗОВАТЕЛЯ (например, из localStorage или auth)
const CURRENT_USER_ID = '550e8400-e29b-41d4-a716-446655440000' // mock

export default {
  components: { VideoCard, CommentItem },
  setup() {
    const route = useRoute()
    const videoId = route.params.id

    const currentVideo = ref(null)
    const videoSrc = ref(null)
    const comments = ref([])
    const users = ref([])
    const loading = ref(false)
    const loadingComments = ref(false)
    const newCommentText = ref('')

    // Загрузка данных
    const fetchVideoData = async () => {
      try {
        loading.value = true

        // 1. Получить данные видео
        const videoRes = await fetch(`/api/videos/${videoId}`)
        if (!videoRes.ok) throw new Error('Видео не найдено')
        currentVideo.value = await videoRes.json()

        // 2. Получить ссылку на видеофайл
        const linkRes = await fetch(`/api/videos/${videoId}/get_link`)
        if (!linkRes.ok) throw new Error('Ссылка на видео недоступна')
        const { link } = await linkRes.json()
        videoSrc.value = `${link}`

        // 4. Загрузить комментарии
        await fetchComments()
      } catch (err) {
        console.error('Ошибка загрузки видео:', err)
        alert('Не удалось загрузить видео')
      } finally {
        loading.value = false
      }
    }

    const fetchComments = async () => {
      try {
        loadingComments.value = true
        const res = await fetch(`/api/videos/${videoId}/comments`)
        comments.value = await res.json()

        // Загрузить пользователей
        const userIds = [...new Set(comments.value.map(c => c.user_id))]
        if (userIds.length > 0) {
          const usersRes = await fetch(`/api/users/batch?ids=${userIds.join(',')}`)
          users.value = await usersRes.json()
        }
      } catch (err) {
        console.error('Ошибка загрузки комментариев:', err)
      } finally {
        loadingComments.value = false
      }
    }

    // Лайк / дизлайк
    const like = async () => {
      if (!currentVideo.value || loading.value) return
      try {
        const res = await fetch(`/api/videos/${videoId}/likes`, { method: 'POST' })
        const updated = await res.json()
        currentVideo.value.likes = updated.likes
      } catch (err) {
        alert('Не удалось поставить лайк')
      }
    }

    const dislike = async () => {
      if (!currentVideo.value || loading.value) return
      try {
        const res = await fetch(`/api/videos/${videoId}/dislikes`, { method: 'POST' })
        const updated = await res.json()
        currentVideo.value.dislikes = updated.dislikes
      } catch (err) {
        alert('Не удалось поставить дизлайк')
      }
    }

    // Отправка комментария
    const postComment = async () => {
      if (!newCommentText.value.trim() || !CURRENT_USER_ID) return

      try {
        const payload = {
          user_id: CURRENT_USER_ID,
          text: newCommentText.value.trim(),
          parent_id: null // можно сделать ответом
        }

        const res = await fetch(`/api/videos/${videoId}/comments`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })

        if (res.ok) {
          newCommentText.value = ''
          await fetchComments() // обновить список
        }
      } catch (err) {
        alert('Не удалось отправить комментарий')
      }
    }

    // Вычисляемые свойства
    const rootComments = computed(() => {
      return comments.value.filter(c => c.parent_id === null)
    })

    const usersMap = computed(() => {
      const map = {}
      users.value.forEach(u => {
        map[u.id] = u
      })
      return map
    })

    const recommendedVideos = ref([
      { id: '770e8400-e29b-41d4-a716-446655440001', title: 'Python Web Development', thumbnail: 'https://via.placeholder.com/160x90?text=Rec+1' },
      { id: '770e8400-e29b-41d4-a716-446655440002', title: 'Elden Ring Speedrun', thumbnail: 'https://via.placeholder.com/160x90?text=Rec+2' }
    ])

    const currentUser = computed(() => CURRENT_USER_ID)

    onMounted(() => {
      fetchVideoData()
    })

    return {
      currentVideo,
      videoSrc,
      comments,
      rootComments,
      usersMap,
      loading,
      loadingComments,
      newCommentText,
      currentUser,
      recommendedVideos,
      like,
      dislike,
      postComment
    }
  }
}
</script>

<style scoped>
.video-page {
  display: flex;
  gap: 32px;
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

.player {
  flex: 2;
  background: #000;
  border-radius: 12px;
  overflow: hidden;
}
.player video {
  width: 100%;
  display: block;
}
.placeholder {
  width: 100%;
  height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #222;
  color: #fff;
  font-size: 18px;
}

.video-details {
  flex: 1;
}
h1 {
  font-size: 24px;
  margin-bottom: 12px;
  color: #222;
}
.description {
  color: #555;
  margin-bottom: 20px;
  line-height: 1.5;
}

.actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}
.actions button {
  padding: 8px 16px;
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}
.actions button:hover {
  background: #e0e0e0;
}
.actions button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.views {
  color: #666;
  font-size: 14px;
}

.add-comment {
  margin-bottom: 24px;
}
.add-comment textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: vertical;
  min-height: 80px;
  margin-bottom: 8px;
  font-family: inherit;
}
.add-comment button {
  padding: 8px 20px;
  background: #ff0000;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}
.add-comment button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.comments-section h3,
.recommendations h3 {
  margin-bottom: 16px;
  color: #222;
}
.comments-section {
  margin-bottom: 24px;
}

.recommendations {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>