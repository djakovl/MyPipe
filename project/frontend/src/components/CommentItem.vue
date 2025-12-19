<!-- src/components/CommentItem.vue -->
<template>
  <div class="comment">
    <img :src="userAvatar" :alt="author?.name" class="avatar" />
    <div class="comment-body">
      <div class="comment-header">
        <strong>{{ author?.name }}</strong>
        <span class="date">{{ formatDate(comment.date) }}</span>
      </div>
      <p>{{ comment.text }}</p>

      <!-- Ответы на комментарий -->
      <div v-if="replies.length > 0" class="replies">
        <CommentItem
          v-for="reply in replies"
          :key="reply.id"
          :comment="reply"
          :all-comments="allComments"
          :users="users"
          class="reply"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  props: {
    comment: { type: Object, required: true },
    allComments: { type: Array, required: true },
    users: { type: Object, required: true }
  },
  setup(props) {
    const author = computed(() => props.users[props.comment.user_id])
    const userAvatar = computed(() => author.value?.logo_loc || '/avatars/default.png')

    const replies = computed(() => {
      return props.allComments.filter(c => c.parent_id === props.comment.id && !c.is_deleted)
    })

    const formatDate = (isoDate) => {
      return new Date(isoDate).toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    return {
      author,
      userAvatar,
      replies,
      formatDate
    }
  }
}
</script>

<style scoped>
.comment {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}
.comment.reply {
  margin-left: 32px;
}
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  background: #ddd;
}
.comment-body {
  flex: 1;
}
.comment-header {
  display: flex;
  gap: 8px;
  margin-bottom: 4px;
}
.date {
  color: #666;
  font-size: 0.9em;
}
.replies {
  margin-top: 12px;
}
</style>