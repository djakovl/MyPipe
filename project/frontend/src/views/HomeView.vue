<!-- src/views/HomeView.vue -->
<template>
  <div class="home">
    <h1>Добро пожаловать на SiriusTube!</h1>
    <router-link to="/feed">Перейти к ленте</router-link>
  </div>
</template>

<style scoped>
.home {
  padding: 40px;
  text-align: center;
}
.home a {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  background:  #119fb8;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}
</style>