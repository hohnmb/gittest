<!-- views/FilteredMoviesView.vue -->
<template>
  <div class="movie-container">
    <h1 class="movie-title">
      {{ movieStore.selectedRegion === 'domestic' ? '국내' : '해외' }} 
      영화 <span v-if="selectedGenreNames.length">- {{ selectedGenreNames.join(', ') }}</span>
    </h1>
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
import { computed } from 'vue'
import { useMovieStore } from '../stores/movie'
import MovieCard from '../components/MovieCard.vue'

const movieStore = useMovieStore()

// 필터링 로직은 store로 이동했으므로 store의 filteredMovies 사용
const filteredMovies = computed(() => movieStore.filteredMovies)

// 선택된 장르들의 이름을 가져오는 computed 속성
const selectedGenreNames = computed(() => {
  const genres = {
    28: '액션',
    12: '모험',
    16: '애니메이션',
    35: '코미디',
    80: '범죄',
    99: '다큐멘터리',
    18: '드라마',
    10751: '가족',
    14: '판타지',
    36: '역사',
    27: '공포',
    10402: '음악',
    9648: '미스터리',
    10749: '로맨스',
    878: 'SF',
    10770: 'TV 영화',
    53: '스릴러',
    10752: '전쟁',
    37: '서부'
  }
  
  return movieStore.selectedGenres.map(genreId => genres[genreId] || '')
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

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
}
</style>