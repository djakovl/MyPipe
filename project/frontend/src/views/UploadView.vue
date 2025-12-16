<!-- src/views/UploadView.vue -->
<template>
  <div class="upload">
    <h2>Загрузить видео</h2>
    <input type="file" accept="video/*" @change="handleFile" />
    <input v-model="title" placeholder="Название видео" style="width: 100%; padding: 10px; margin: 10px 0;" />
    <textarea v-model="description" placeholder="Описание" rows="4" style="width: 100%; padding: 10px;"></textarea>
    <button @click="upload" :disabled="!file">Загрузить</button>
    <p v-if="uploadStatus">{{ uploadStatus }}</p>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  setup() {
    const file = ref(null)
    const title = ref('')
    const description = ref('')
    const uploadStatus = ref('')

    const handleFile = (e) => {
      file.value = e.target.files[0]
    }

    const upload = () => {
      if (!file.value) return
      uploadStatus.value = 'Видео загружено! (mock)'
      console.log('Загружаем:', { file: file.value.name, title: title.value, description: description.value })
      // Здесь позже будет fetch на бэкенд
    }

    return { file, title, description, uploadStatus, handleFile, upload }
  }
}
</script>

<style scoped>
.upload {
  padding: 40px;
  max-width: 600px;
  margin: 0 auto;
}
input, textarea, button {
  width: 100%;
  padding: 10px;
  margin: 8px 0;
}
button {
  background: #ff0000;
  color: white;
  border: none;
  cursor: pointer;
}
button:disabled {
  background: #ccc;
}
</style>