<template>
  <div class="tmdb-movie-card">
    <img
      v-if="movie.poster_path"
      :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
      :alt="movie.title"
      class="movie-poster"
      @click="goToDetail"
    />
    <div class="movie-info">
      <h3>{{ movie.title }}</h3>
      <p class="movie-overview">{{ movie.overview }}</p>
      <div class="movie-details">
        <span>평점: {{ movie.vote_average || 'N/A' }}</span>
        <span>개봉일: {{ movie.release_date || '미정' }}</span>
      </div>
      <!-- 좋아요 버튼 -->
      <button @click="handleLikeClick" :class="['like-button', { liked: isLiked }]">
        <span class="heart-icon">
          {{ isLiked ? "❤️" : "🤍" }}
        </span>
        <span class="like-count">{{ likeCount }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useCounterStore } from "@/stores/counter"; // Pinia 스토어 가져오기
import { useRouter } from "vue-router";
import axios from "axios";

const props = defineProps({
  movie: {
    type: Object,
    required: true,
  },
});

const router = useRouter();
const store = useCounterStore();

// 좋아요 상태 확인 (로그인 여부와 관계)
const isLiked = computed(() => {
  if (store.isLogin) {
    return store.likeMovies[props.movie.id]?.is_liked || false;
  }
  return false;
});

// 좋아요 수 (로그인 상태에 관계없이 유지)
const likeCount = computed(() => store.likeMovies[props.movie.id]?.like_count || 0);

// 영화 상세 페이지로 이동하기 위한 함수
const goToDetail = async () => {
  try {
    await saveTmdbMovie(props.movie.id); // 영화 정보 저장
    router.push({
      name: "MovieDetail",
      params: { id: props.movie.id }, // 영화 ID를 URL 파라미터로 전달
    });
  } catch (error) {
    console.error("상세 페이지 이동 중 오류 발생:", error);
  }
};

// 좋아요 버튼 클릭 처리
const handleLikeClick = async () => {
  if (!store.isLogin) {
    alert("로그인 후 좋아요를 누를 수 있습니다.");
    return;
  }

  // 좋아요 상태 토글
  store.toggleMovieLike(props.movie.id);
};

// TMDB 영화 정보를 백엔드에 저장하는 함수
const saveTmdbMovie = async (movieId) => {
  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/api/v1/movies/${movieId}/save/`,
      {},
      { headers: { Authorization: `Token ${store.token}` } }
    );
    console.log("영화 저장 성공:", response.data);
  } catch (error) {
    console.error("영화를 저장하는 중 오류 발생:", error.response?.data || error.message);
    throw error;
  }
};
</script>

<style scoped>
.tmdb-movie-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease;
  cursor: pointer; /* 마우스 오버시 포인터 표시 */
}

.tmdb-movie-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.movie-poster {
  width: 100%;
  height: 350px;
  object-fit: cover;
}

.movie-info {
  padding: 15px;
}

.movie-overview {
  font-size: 0.9em;
  color: #666;
  margin: 10px 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.movie-details {
  display: flex;
  justify-content: space-between;
  font-size: 0.8em;
  color: #888;
}

/* 좋아요 버튼 디자인 */
.like-button {
  display: flex;
  align-items: center;
  padding: 12px 24px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-size: 1.1em;
  font-weight: bold;
  margin-top: 10px;
  transition: all 0.3s ease;
}

.like-button.liked {
  background-color: #ff5e57;
}

.heart-icon {
  font-size: 1.4em;
}

.like-count {
  margin-left: 10px;
  font-size: 1.1em;
}
</style>
