<template>
  <div class="movie-recommend-container">
    <!-- 배너 박스 -->
    <div class="banner-box">
      <h1 class="greeting">안녕하세요, {{ username }}님!</h1>
      <h2 class="recommendation-title">오늘 볼만한 영화 추천</h2>
    </div>

    <!-- 선호도 설정이 안된 경우 -->
    <div v-if="!hasPreferences" class="setup-container">
      <h2 class="setup-title">영화 추천 받기 시작하기</h2>

      <!-- 지역 선택 -->
      <div v-if="!movieStore.selectedRegion" class="selection-section">
        <h3 class="selection-title">영화 지역을 선택해주세요</h3>
        <div class="button-group">
          <button @click="selectRegion('domestic')" class="region-btn">
            국내 영화
          </button>
          <button @click="selectRegion('foreign')" class="region-btn">
            해외 영화
          </button>
        </div>
      </div>

      <!-- 장르 선택 -->
      <div
        v-else-if="!movieStore.selectedGenres.length"
        class="selection-section"
      >
        <h3 class="selection-title">장르를 선택해주세요</h3>
        <p class="description">원하는 장르를 여러 개 선택할 수 있습니다.</p>
        <div class="genre-buttons">
          <button
            v-for="genre in availableGenres"
            :key="genre"
            class="genre-btn"
            @click="selectGenre(genre)"
          >
            {{ genre }}
          </button>
        </div>
      </div>
    </div>

    <!-- 선호도 설정 완료된 경우 -->
    <div v-else>
      <h2 class="recommendation-title">{{ username }}님을 위한 추천 영화</h2>
      <div class="movie-list">
        <div
          v-for="movie in movieStore.filteredMovies"
          :key="movie.id"
          class="movie-card-wrapper"
        >
          <MovieCard :movie="movie" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useMovieStore } from "@/stores/movie";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from "vue-router";
import MovieCard from "@/components/MovieCard.vue";

const movieStore = useMovieStore();
const counterStore = useCounterStore();
const router = useRouter();

const username = computed(() => counterStore.username);

// 선호도 설정 여부
const hasPreferences = computed(
  () => movieStore.selectedRegion && movieStore.selectedGenres.length > 0
);

// 이용 가능한 장르 목록
const availableGenres = [
  "액션",
  "드라마",
  "코미디",
  "로맨스",
  "SF",
  "애니메이션",
  "스릴러",
  "공포",
  "판타지",
];

// 컴포넌트 마운트 시 사용자 선호도 로드
onMounted(async () => {
  await movieStore.loadUserPreferences();
  if (!hasPreferences.value) {
    router.push({ name: "region-select" });
  } else {
    await movieStore.fetchMovies();
  }
});

// 지역 선택 핸들러
const selectRegion = (region) => {
  movieStore.setSelectedRegion(region);
  router.push("/movies/select-genre");
};

// 장르 선택 핸들러
const selectGenre = (genre) => {
  movieStore.addSelectedGenre(genre);
};
</script>

<style scoped>
.movie-recommend-container {
  font-family: "Arial", sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 배너 박스 스타일 */
.banner-box {
  background: linear-gradient(45deg, #1d72b8, #6c5ce7);
  color: #fff;
  padding: 60px 40px;
  border-radius: 15px;
  text-align: center;
  margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  animation: slideIn 1s ease-out;
}

@keyframes slideIn {
  0% {
    transform: translateY(-30px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

.greeting {
  font-size: 2.4rem;
  font-weight: 700;
  margin: 0;
  letter-spacing: 1px;
}

.recommendation-title {
  font-size: 1.8rem;
  margin-top: 15px;
  font-weight: 500;
}

/* 기존 스타일 유지 */
.setup-container {
  text-align: center;
  padding: 30px 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.setup-title {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 20px;
}

.selection-section {
  margin-bottom: 30px;
}

.selection-title {
  font-size: 1.5rem;
  color: #444;
  margin-bottom: 15px;
}

.description {
  font-size: 1rem;
  color: #777;
  margin-bottom: 20px;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.region-btn,
.genre-btn {
  padding: 14px 30px;
  font-size: 1.1rem;
  background-color: #1d72b8;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.region-btn:hover,
.genre-btn:hover {
  background-color: #155a8a;
  transform: translateY(-3px);
}

.genre-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
}

.movie-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.movie-card-wrapper {
  display: flex;
  justify-content: center;
}

.recommendation-title {
  font-size: 1.8rem;
  color: #333;
  text-align: center;
  margin-bottom: 30px;
}
</style>
