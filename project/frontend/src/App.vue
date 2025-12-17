<!-- src/App.vue -->
<template>
  <div id="app">
    <HeaderComponent />
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
import HeaderComponent from '@/components/HeaderComponent.vue'

export default {
  components: { HeaderComponent }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: Arial, sans-serif;
  background: #ffffff;
}
#app {
  min-height: 100vh;
}
</style>