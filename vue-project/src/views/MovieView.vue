<template>
  <div class="movie-container">
    <h1 class="movie-title">Movie List</h1>
        <!-- 필터링 페이지로 이동하는 버튼 추가 -->
    <button @click="$router.push('/movies/select-region')" class="filter-btn">
      영화 필터링하기
    </button>
    <div class="movie-grid">
      <MovieCard
        v-for="movie in movieStore.movies"
        :key="movie.id"
        :movie="movie"
      />
    </div>
    <!-- [추가] 필터 선택 UI -->
    <div class="filter-section">
      <select v-model="selectedRegion" class="region-filter">
        <option value="all">전체 영화</option>
        <option value="domestic">국내 영화</option>
        <option value="foreign">해외 영화</option>
      </select>
    </div>
    <div class="movie-grid">
      <MovieCard
        v-for="movie in filteredMovies"
        :key="movie.id"
        :movie="movie"
      />
    </div>
  </div>
</template>

<script setup>
// [수정] import문에 ref와 computed 추가
import { ref, computed, onMounted } from 'vue'
import { useMovieStore } from '../stores/movie'
import MovieCard from '../components/MovieCard.vue'

const movieStore = useMovieStore()

// [추가] 필터 선택값 저장용 ref
const selectedRegion = ref('all')

// [추가] 필터링 로직
const filteredMovies = computed(() => {
  if (selectedRegion.value === 'all') {
    return movieStore.movies
  }
  
  return movieStore.movies.filter(movie => {
    const isDomestic = movie.original_language === 'ko' && 
                      movie.production_countries.includes('KR')
    return selectedRegion.value === 'domestic' ? isDomestic : !isDomestic
  })
})

onMounted(() => {
  movieStore.fetchMovies()
})
</script>

<style scoped>
.movie-container {
  padding: 20px;
}

.movie-title {
  text-align: center;
  margin-bottom: 30px;
}

/* [추가] 필터 관련 스타일 */
.filter-section {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.region-filter {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  background-color: white;
  cursor: pointer;
}

.region-filter:focus {
  outline: none;
  border-color: #666;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
}
</style>