<template>
  <div v-if="movie" class="movie-detail">
    <div class="movie-header">
      <img
        v-if="movie.poster_path"
        :src="`https://image.tmdb.org/t/p/w1280${movie.poster_path}`"
        :alt="movie.title"
        class="backdrop"
      />
      <div class="movie-info">
        <div class="play-button">▶</div>
        <div class="movie-meta">
          <div class="rating-info">
            <span class="language">{{ movie.original_language.toUpperCase() }}</span>
            <span class="release-date">{{ movie.released_date }}</span>
            <span class="popularity">인기도: {{ movie.popularity }}</span>
          </div>
          <h1 class="title">{{ movie.title }}</h1>
          <div class="genres">
            <span v-for="genre in movie.genres" :key="genre.id" class="genre-tag">
              {{ genre.name }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="content-section">
      <div class="description">
        <h2>DESCRIPTION</h2>
        <p>{{ movie.overview }}</p>
      </div>

      <div class="hype-section">
        <h2>RATINGS</h2>
        <div class="ratings">
          <div class="rating-item">
            <span class="rating-score">{{ movie.vote_avg }}/10</span>
            <span class="rating-source">평점</span>
          </div>
          <MovieLikeButton :movie="movie" />
        </div>
      </div>
    </div>

    <MovieReview v-if="movie.id" :movieId="movie.id" />
  </div>
  <div v-else class="loading">로딩 중...</div>
</template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { useRoute } from "vue-router";
  import axios from "axios";
  import MovieLikeButton from "../components/MovieLikeButton.vue";
  import { useCounterStore } from "../stores/counter";
  import MovieReview from "@/views/MovieReview.vue";
  const route = useRoute();
  const movie = ref(null);
  const store = useCounterStore();
  
  const fetchMovieDetail = async () => {
  try {
    movie.value = null; // 초기화

    // 백엔드에서 영화 상세 정보 가져오기
    const response = await axios.get(
      `http://127.0.0.1:8000/api/v1/movies/${route.params.id}/`,
      { headers: { Authorization: `Token ${store.token}` } }
    );

    movie.value = response.data; // 영화 데이터 저장
  } catch (error) {
    console.error("영화 상세 정보 로딩 실패:", error.response?.data || error.message);
    movie.value = null;
  }
};

  // 영화 상세 정보 가져오기
  // const fetchMovieDetail = async () => {
  //   try {
  //     const response = await axios.get(
  //       `http://127.0.0.1:8000/api/v1/movies/${route.params.id}/`
  //     );
  //     movie.value = response.data;
  //   } catch (error) {
  //     console.error("영화 정보를 불러오는데 실패했습니다:", error);
  //   }
  // };
  
  onMounted(async () => {
  if (!route.params.id) {
    return;
  }
  await fetchMovieDetail();
});

  </script>
  
  <style scoped>
  .movie-detail {
    background-color: #0a1014;
    color: white;
    min-height: 100vh;
  }
  
  .backdrop {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  filter: brightness(0.7);
}

.movie-header {
  position: relative;
  height: 600px; /* 높이 조절 */
  overflow: hidden;
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: contain; /* cover 대신 contain 사용 */
  background-position: center;
  background-repeat: no-repeat;
}
  
  .movie-info {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 2rem;
    background: linear-gradient(transparent, #0a1014);
  }
  
  .play-button {
    width: 60px;
    height: 60px;
    background: #4CAF50;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    cursor: pointer;
    margin-bottom: 1rem;
  }
  
  .rating-info {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .rating-info span {
    padding: 0.3rem 0.8rem;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    font-size: 0.9rem;
  }
  
  .title {
    font-size: 2.5rem;
    margin-bottom: 1rem;
  }
  
  .genres {
    display: flex;
    gap: 0.5rem;
  }
  
  .genre-tag {
    padding: 0.3rem 0.8rem;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    font-size: 0.9rem;
  }
  
  .content-section {
    padding: 2rem;
  }
  
  .description h2, .hype-section h2 {
    color: #666;
    margin-bottom: 1rem;
    font-size: 1rem;
  }
  
  .ratings {
    display: flex;
    gap: 2rem;
  }
  
  .rating-item {
    display: flex;
    flex-direction: column;
  }
  
  .rating-score {
    font-size: 1.5rem;
    font-weight: bold;
    color: #4CAF50;
  }
  
  .rating-source {
    font-size: 0.9rem;
    color: #666;
  }
  </style>