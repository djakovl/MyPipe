<!-- src/components/Header.vue -->
<template>
  <header class="header">
    <div class="header-content">
      <router-link to="/" class="logo">YouTube Clone</router-link>

      <div class="search-bar">
        <input type="text" placeholder="Поиск..." v-model="searchQuery" @keyup.enter="search" />
        <button @click="search">🔍</button>
      </div>

      <div class="nav-icons">
        <router-link to="/upload" title="Загрузить">📹</router-link>
        <router-link to="/profile" title="Аккаунт">👤</router-link>
      </div>
    </div>
  </header>
</template>

<script>
import { ref } from 'vue'


export default {
  name: 'HeaderComponent',
  setup() {
    const searchQuery = ref('')
    

    const search = () => {
      if (searchQuery.value.trim()) {
        console.log('Поиск:', searchQuery.value)
        // Позже можно сделать /search?q=...
      }
    }

    return { searchQuery, search }
  }
}
</script>

<style scoped>
.header {
  background: #fff;
  border-bottom: 1px solid #e5e5e5;
  padding: 10px 0;
  position: sticky;
  top: 0;
  z-index: 100;
}
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}
.logo {
  font-size: 20px;
  font-weight: bold;
  text-decoration: none;
  color: #ff0000;
}
.search-bar {
  display: flex;
  flex: 0 1 500px;
}
.search-bar input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 2px 0 0 2px;
}
.search-bar button {
  padding: 8px 12px;
  background: #f8f8f8;
  border: 1px solid #ccc;
  border-left: none;
  cursor: pointer;
}
.nav-icons a {
  margin-left: 20px;
  font-size: 20px;
  text-decoration: none;
  color: #333;
}
</style>