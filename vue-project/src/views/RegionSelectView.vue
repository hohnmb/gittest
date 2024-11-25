<!-- views/RegionSelectView.vue -->
<template>
  <div class="select-container">
    <h2>★영화 지역 선택★</h2>
    <div class="select-buttons">
      <button @click="selectRegion('domestic')" class="select-btn">국내 영화</button>
      <button @click="selectRegion('foreign')" class="select-btn">해외 영화</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useMovieStore } from '../stores/movie'
import { useUserPreferencesStore } from '@/stores/userPreferences'

const router = useRouter()
const movieStore = useMovieStore()
const preferencesStore = useUserPreferencesStore()

const selectRegion = (region) => {
  movieStore.setSelectedRegion(region)
  router.push('/movies/select-genre')
}
</script>

<style scoped>
.select-container {
  padding: 20px;
  text-align: center;
}

.select-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.select-btn {
  padding: 10px 20px;
  font-size: 1.1rem;
  cursor: pointer;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: white;
}

.select-btn:hover {
  background-color: #0056b3;
}
</style>