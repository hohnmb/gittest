<!-- views/GenreSelectView.vue -->
<template>
  <div class="select-container">
    <h2>장르 선택</h2>
    <p class="guide-text">원하는 장르를 여러 개 선택할 수 있습니다.</p>
    <div class="genre-grid">
      <!-- 여기서 genres 데이터가 제대로 표시되지 않는 문제 -->
      <button 
        v-for="genre in computedGenre" 
        :key="genre.pk"
        @click="selectGenre(genre.pk)"
        :class="['genre-btn', { 'selected': genre.isSelected }]"
      >
        {{ genre.fields.name }}
      </button>
    </div>
    <div class="action-buttons">
      <button 
        @click="goToFilteredMovies" 
        class="confirm-btn"
        :disabled="!movieStore.selectedGenres.length"
      >
        선택 완료
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMovieStore } from '../stores/movie'

const router = useRouter()
const movieStore = useMovieStore()

// 장르 데이터 정의
const genres = ref([
{
    "model": "movies.genre",
    "pk": 28,
    "fields": {
      "name": "Action"
    }
  },
  {
    "model": "movies.genre",
    "pk": 12,
    "fields": {
      "name": "Adventure"
    }
  },
  {
    "model": "movies.genre",
    "pk": 16,
    "fields": {
      "name": "Animation"
    }
  },
  {
    "model": "movies.genre",
    "pk": 35,
    "fields": {
      "name": "Comedy"
    }
  },
  {
    "model": "movies.genre",
    "pk": 80,
    "fields": {
      "name": "Crime"
    }
  },
  {
    "model": "movies.genre",
    "pk": 99,
    "fields": {
      "name": "Documentary"
    }
  },
  {
    "model": "movies.genre",
    "pk": 18,
    "fields": {
      "name": "Drama"
    }
  },
  {
    "model": "movies.genre",
    "pk": 10751,
    "fields": {
      "name": "Family"
    }
  },
  {
    "model": "movies.genre",
    "pk": 14,
    "fields": {
      "name": "Fantasy"
    }
  },
  {
    "model": "movies.genre",
    "pk": 36,
    "fields": {
      "name": "History"
    }
  },
  {
    "model": "movies.genre",
    "pk": 27,
    "fields": {
      "name": "Horror"
    }
  },
  {
    "model": "movies.genre",
    "pk": 10402,
    "fields": {
      "name": "Music"
    }
  },
  {
    "model": "movies.genre",
    "pk": 9648,
    "fields": {
      "name": "Mystery"
    }
  },
  {
    "model": "movies.genre",
    "pk": 10749,
    "fields": {
      "name": "Romance"
    }
  },
  {
    "model": "movies.genre",
    "pk": 878,
    "fields": {
      "name": "Science Fiction"
    }
  },
  {
    "model": "movies.genre",
    "pk": 10770,
    "fields": {
      "name": "TV Movie"
    }
  },
  {
    "model": "movies.genre",
    "pk": 53,
    "fields": {
      "name": "Thriller"
    }
  },
  {
    "model": "movies.genre",
    "pk": 10752,
    "fields": {
      "name": "War"
    }
  },
  {
    "model": "movies.genre",
    "pk": 37,
    "fields": {
      "name": "Western"
    }
  }
])

// 장르가 선택되었는지 확인하는 함수
// const isSelected = (genreId) => {
//   return movieStore.selectedGenres.includes(genreId)
// }

const computedGenre = computed(() => {
  // selectedGenres가 존재하는지 확인
  if (!movieStore.selectedGenres) {
    return genres.value.map(genre => ({...genre, isSelected: false}))
  }

  return genres.value.map((myGenre) => {
    if (movieStore.selectedGenres.some((selectedGenre) => selectedGenre.id === myGenre.pk)) {
      return {...myGenre, isSelected: true}
    } else {
      return {...myGenre, isSelected: false}
    }
  })
})

// 장르 선택 함수
const selectGenre = (genreId) => {
  movieStore.setSelectedGenre(genreId)
}

// 필터링된 영화 페이지로 이동
const goToFilteredMovies = () => {
  if (movieStore.selectedGenres.length > 0) {
    router.push('/movies/filtered')
  }
}
</script>

<style scoped>
.select-container {
  padding: 20px;
  text-align: center;
}

.guide-text {
  color: #666;
  margin-bottom: 20px;
}

.genre-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 15px;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.genre-btn {
  padding: 15px;
  font-size: 1rem;
  cursor: pointer;
  border: 2px solid #ddd;
  border-radius: 8px;
  background-color: white;
  transition: all 0.3s ease;
}

.genre-btn:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.genre-btn.selected {
  background-color: #007bff;
  color: white;
  border-color: #0056b3;
}

.action-buttons {
  margin-top: 30px;
}

.confirm-btn {
  padding: 12px 24px;
  font-size: 1.1rem;
  cursor: pointer;
  border: none;
  border-radius: 8px;
  background-color: #28a745;
  color: white;
  transition: all 0.3s ease;
}

.confirm-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.confirm-btn:not(:disabled):hover {
  background-color: #218838;
}
</style>