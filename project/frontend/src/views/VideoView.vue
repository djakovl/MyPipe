<!-- src/views/VideoView.vue -->
<template>
  <div class="video-page" v-if="video">
    <div class="player">
      <video v-if="videoUrl" :src="videoUrl" controls preload="metadata" width="100%">
        Ваш браузер не поддерживает видео.
      </video>
      <div v-else class="placeholder">Загрузка видео...</div>
    </div>

    <div class="video-details">
      <h1>{{ video.name }}</h1>
      <p class="description">{{ video.description }}</p>

      <div class="actions">
        <button @click="like" :disabled="loading">👍 {{ video.likes }}</button>
        <button @click="dislike" :disabled="loading">👎 {{ video.dislikes }}</button>
        <span class="views">👁️ {{ video.views }} просмотров</span>
      </div>

      <!-- Форма добавления комментария -->
      <div class="add-comment">
        <textarea
          v-model="newCommentText"
          placeholder="Напишите комментарий..."
          :disabled="loading"
        ></textarea>
        <button @click="postComment" :disabled="!newCommentText.trim() || loading">
          Отправить
        </button>
      </div>

      <!-- Список комментариев -->
      <div class="comments-section">
        <h3>Комментарии ({{ comments.length }})</h3>
        <div v-if="loadingComments">Загрузка...</div>
        <div v-else-if="comments.length === 0">Комментариев пока нет.</div>
        <div v-else class="comments-list">
          <div v-for="comment in rootComments" :key="comment.id" class="comment">
            <div class="comment-header">
              <span class="user-id">Пользователь {{ comment.user_id }}</span>
              <span class="comment-date">{{ formatDate(comment.date) }}</span>
            </div>
            <p class="comment-text">{{ comment.text }}</p>
          </div>
        </div>
      </div>

      <!-- Рекомендации -->
      <div class="recommendations" v-if="recommendations.length">
        <h3>Рекомендации</h3>
        <VideoCard
          v-for="v in recommendations"
          :key="v.id"
          :video="{
            id: v.id,
            title: v.name,
            thumbnail: defaultThumb,
            views: v.views,
            uploader: 'Автор'
          }"
        />
      </div>
    </div>
  </div>
  <div v-else class="loading">
    Загрузка видео...
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import VideoCard from '@/components/VideoCard.vue'


const API_BASE = '/api'

// ⚠️ Замените на реальный ID пользователя (например, из localStorage)
const CURRENT_USER_ID = '550e8400-e29b-41d4-a716-446655440000'

export default {
  components: { VideoCard },
  setup() {
    const route = useRoute()
    const videoId = route.params.id

    const video = ref(null)
    const videoUrl = ref(null)
    const comments = ref([])
    const recommendations = ref([])
    const loading = ref(false)
    const loadingComments = ref(false)
    const newCommentText = ref('')

    const loadVideo = async () => {
      try {
        const videoRes = await fetch(`${API_BASE}/video/${videoId}`)
        if (!videoRes.ok) throw new Error('Видео не найдено')
        video.value = await videoRes.json()

        const linkRes = await fetch(`${API_BASE}/video/${videoId}/get_link`)
        const { video_url } = await linkRes.json()
        videoUrl.value = video_url

        await loadComments()

        const allRes = await fetch(`${API_BASE}/videos`)
        const allVideos = await allRes.json()
        recommendations.value = allVideos
          .filter(v => v.id !== videoId && v.is_public && !v.is_deleted)
          .slice(0, 4)
      } catch (err) {
        console.error('Ошибка загрузки видео:', err)
        alert('Не удалось загрузить видео')
      }
    }

    const loadComments = async () => {
      try {
        loadingComments.value = true
        const res = await fetch(`${API_BASE}/video/${videoId}/comments`)
        comments.value = await res.json()
      } catch (err) {
        console.error('Ошибка загрузки комментариев:', err)
      } finally {
        loadingComments.value = false
      }
    }

    const postComment = async () => {
      if (!newCommentText.value.trim() || !CURRENT_USER_ID) return

      try {
        loading.value = true
        const response = await fetch(`${API_BASE}/video/${videoId}/comment`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_id: CURRENT_USER_ID,
            text: newCommentText.value.trim(),
            parent_id: null // корневой комментарий
          })
        })

        if (response.ok) {
          newCommentText.value = ''
          await loadComments() // обновляем список
        } else {
          throw new Error('Не удалось отправить комментарий')
        }
      } catch (err) {
        alert('Ошибка при отправке комментария')
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    const like = async () => {
      if (loading.value) return
      try {
        loading.value = true
        await fetch(`${API_BASE}/video/${videoId}/likes`, { method: 'POST' })
        video.value.likes += 1
      } catch (err) {
        alert('Не удалось поставить лайк')
      } finally {
        loading.value = false
      }
    }

    const dislike = async () => {
      if (loading.value) return
      try {
        loading.value = true
        await fetch(`${API_BASE}/video/${videoId}/dislikes`, { method: 'POST' })
        video.value.dislikes += 1
      } catch (err) {
        alert('Не удалось поставить дизлайк')
      } finally {
        loading.value = false
      }
    }

    const rootComments = computed(() => {
      return comments.value.filter(c => c.parent_id === null)
    })

    const formatDate = (isoString) => {
      return new Date(isoString).toLocaleString('ru-RU')
    }

    onMounted(() => {
      loadVideo()
    })

    return {
      video,
      videoUrl,
      comments,
      recommendations,
      loading,
      loadingComments,
      newCommentText,
      rootComments,
      like,
      dislike,
      postComment,
      formatDate
    }
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
  font-family: Arial, sans-serif;
}
.placeholder, .loading {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 500px;
  background: #f0f0f0;
  color: #666;
}
.player video {
  width: 100%;
  border-radius: 12px;
}
.video-details {
  flex: 1;
}
.description {
  color: #555;
  margin: 12px 0;
  line-height: 1.5;
}
.actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 16px 0;
}
.actions button {
  padding: 8px 16px;
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
}
.actions button:disabled {
  opacity: 0.6;
}
.views {
  color: #666;
  font-size: 14px;
}

/* Форма комментария */
.add-comment {
  margin: 24px 0;
}
.add-comment textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
  margin-bottom: 8px;
}
.add-comment button {
  padding: 8px 20px;
  background: #ff0000;
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
}
.add-comment button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* Комментарии */
.comments-section h3 {
  margin-bottom: 16px;
  color: #222;
}
.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.comment {
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}
.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
}
.user-id {
  font-weight: bold;
  color: #222;
}
.comment-date {
  color: #999;
  font-size: 0.9em;
}
.comment-text {
  margin: 0;
  color: #333;
  line-height: 1.4;
}

/* Рекомендации */
.recommendations {
  margin-top: 32px;
}
.recommendations h3 {
  margin-bottom: 16px;
  color: #222;
}
</style>