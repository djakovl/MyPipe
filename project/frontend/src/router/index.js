import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import FeedView from '@/views/FeedView.vue'
import ProfileView from '@/views/ProfileView.vue'
import UploadView from '@/views/UploadView.vue'
import VideoView from '@/views/VideoView.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/feed', name: 'Feed', component: FeedView },
  { path: '/profile', name: 'Profile', component: ProfileView },
  { path: '/upload', name: 'Upload', component: UploadView },
  { path: '/watch/:id', name: 'Video', component: VideoView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router