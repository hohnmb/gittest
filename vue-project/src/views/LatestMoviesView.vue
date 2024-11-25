<template>
  <div class="latest-movies-container">
    <h1 class="page-title">최신 영화 목록</h1>

    <!-- 정렬 옵션 -->
    <div class="sort-options">
      <label for="sort-key">정렬 기준:</label>
      <select id="sort-key" v-model="sortKey" @change="sortMovies">
        <option value="release_date">개봉일</option>
        <option value="vote_average">평점</option>
        <option value="title">이름</option>
      </select>

      <button @click="toggleSortOrder">
        {{ sortOrder === 'asc' ? '오름차순' : '내림차순' }}
      </button>
    </div>

    <!-- 로딩 및 에러 메시지 -->
    <div v-if="isLoading" class="loading">로딩 중...</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

    <!-- 영화 리스트 -->
    <div v-else class="movie-grid">
      <TmdbMovieCard
        v-for="movie in sortedMovies"
        :key="movie.id"
        :movie="movie"
        @save-tmdb-movie="saveTmdbMovie(movie.id)"
        @toggle-like="toggleMovieLike(movie.id)"
      />
    </div>
  </div>
</template>

<script setup>
// Vue와 Axios 관련 import
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import TmdbMovieCard from "../components/TmdbMovieCard.vue";

// TMDB API 데이터 상태 변수
const movies = ref([]); // 최신 영화 데이터
const sortKey = ref("release_date"); // 기본 정렬 기준: 개봉일
const sortOrder = ref("asc"); // 기본 정렬 순서: 오름차순

// 로딩 및 에러 상태 변수
const isLoading = ref(false);
const errorMessage = ref("");

// TMDB API 호출 함수
const fetchTmdbMovies = async () => {
  const apiKey = import.meta.env.VITE_TMDB_API_KEY; // 수정된 환경 변수 접근 방식
  const apiUrl = import.meta.env.VITE_API_URL; // 수정된 환경 변수 접근 방식

  isLoading.value = true;
  errorMessage.value = "";

  try {
    const response = await axios.get(`${apiUrl}/movie/now_playing`, {
      params: {
        api_key: apiKey,
        language: "ko-KR", // 한국어 데이터 요청
        page: 1,
      },
    });
    movies.value = response.data.results; // 영화 데이터 저장
  } catch (error) {
    console.error("TMDB 영화 데이터를 불러오는 중 오류 발생:", error);
    errorMessage.value = "영화 데이터를 불러오는 데 실패했습니다.";
  } finally {
    isLoading.value = false;
  }
};

// 정렬된 영화 리스트 계산
const sortedMovies = computed(() => {
  return [...movies.value].sort((a, b) => {
    let result = 0;

    if (sortKey.value === "title") {
      result = (a.title || "").localeCompare(b.title || "");
    } else if (sortKey.value === "release_date") {
      result =
        new Date(a.release_date || "1970-01-01") -
        new Date(b.release_date || "1970-01-01");
    } else if (sortKey.value === "vote_average") {
      result = (a.vote_average || 0) - (b.vote_average || 0);
    }

    return sortOrder.value === "asc" ? result : -result; // 오름차순/내림차순 적용
  });
});

// 정렬 순서 토글 함수
const toggleSortOrder = () => {
  sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
};

// 컴포넌트가 마운트될 때 TMDB API 호출
onMounted(() => {
  fetchTmdbMovies();
});
</script>

<style scoped>
.latest-movies-container { padding: 20px; }
.page-title { text-align: center; margin-bottom: 30px; }
.sort-options { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
.movie-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }
.loading { text-align: center; font-size: 1.5rem; color: #666; }
.error { text-align: center; color: red; font-size: 1.2rem; margin-bottom: 20px; }
</style>