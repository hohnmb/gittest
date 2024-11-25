<template>
    <div class="main-container">
      <!-- 메인 배너 섹션 -->
      <section
        class="main-banner"
        :style="bannerStyle"
        @click="goToMovieDetail"
        role="button"
        tabindex="0"
      >
        <div class="banner-content">
          <h1>{{ username }}님을 위한<br />오늘의 추천 영화</h1>
  
          <!-- 선호도 설정 후 메시지 -->
          <p v-if="hasPreferences" class="genre-description">
            {{ selectedRegionText }}영화와 {{ selectedGenresText }} 장르를
            좋아하는 당신,<br />
            오늘은 <strong>{{ selectedMovieTitle }}</strong
            >을 추천합니다!
          </p>
  
          <!-- 선호도 설정 전 메시지 -->
          <p v-else class="genre-description">
            아직 선호도를 설정하지 않으셨군요!<br />
            혹시 <strong>{{ selectedMovieTitle }}</strong
            >은 어떠신가요?
          </p>
        </div>
      </section>
  
      <!-- 추천 영화 섹션 -->
      <section class="movie-recommendations" v-if="hasPreferences">
        <h2>{{ selectedGenresText }} 장르, 더 많은 영화 추천!</h2>
        <div class="carousel-container">
          <button class="nav-button prev" @click="slide('prev')">&lt;</button>
          <div class="movie-carousel">
            <div v-for="movie in randomMovies" :key="movie.id" class="movie-card">
              <MovieCard :movie="movie" />
            </div>
          </div>
          <button class="nav-button next" @click="slide('next')">&gt;</button>
        </div>
      </section>
  
      <section v-if="!isPreferenceCompleted" class="preference-setup">
        <h2>오늘 볼만한 영화 추천 받기</h2>
  
        <!-- 지역 선택 -->
        <div class="region-selection">
          <h3>영화 지역 선택</h3>
          <div class="button-group">
            <button
              @click="selectRegion('domestic')"
              :class="[
                'region-btn',
                { active: movieStore.selectedRegion === 'domestic' },
              ]"
            >
              국내 영화
            </button>
            <button
              @click="selectRegion('foreign')"
              :class="[
                'region-btn',
                { active: movieStore.selectedRegion === 'foreign' },
              ]"
            >
              해외 영화
            </button>
          </div>
        </div>
  
        <!-- 장르 선택 -->
        <div class="genre-selection">
          <h3>장르 선택</h3>
          <p class="genre-description">
            원하는 장르를 여러 개 선택할 수 있습니다.
          </p>
          <div class="genre-buttons">
            <button
              v-for="genre in genres"
              :key="genre.id"
              @click="selectGenre(genre.id)"
              :class="{ active: isGenreSelected(genre.id) }"
              class="genre-btn"
            >
              {{ genre.name }}
            </button>
          </div>
        </div>
  
        <!-- 선택 완료 버튼 -->
        <button
          @click="completeSelection"
          class="complete-btn"
          :disabled="!canComplete || !movieStore.selectedRegion"
        >
          선택 완료
        </button>
      </section>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted, watch } from "vue";
  import { useMovieStore } from "@/stores/movie";
  import { useCounterStore } from "@/stores/counter";
  import { useRouter } from "vue-router";
  import MovieCard from "@/components/MovieCard.vue";
  const isPreferenceCompleted = ref(false);
  const selectedMovie = ref(null);
  const movieStore = useMovieStore();
  const counterStore = useCounterStore();
  const router = useRouter();
  
  const randomMovies = computed(() => {
    const movies = [...movieStore.filteredMovies];
    return movies.sort(() => Math.random() - 0.5).slice(0, 10);
  });
  
  // 슬라이드 위치
  const currentPosition = ref(0);
  
  // 슬라이드 이동 함수
  const slide = (direction) => {
    const carousel = document.querySelector(".movie-carousel");
    const cardWidth = carousel.querySelector(".movie-card").offsetWidth + 20; // 카드 너비 + 간격 계산
  
    if (direction === "next") {
      currentPosition.value = Math.max(
        currentPosition.value - cardWidth,
        -cardWidth * (randomMovies.value.length - 5)
      );
    } else {
      currentPosition.value = Math.min(currentPosition.value + cardWidth, 0);
    }
  
    carousel.style.transform = `translateX(${currentPosition.value}px)`;
  };
  
  // 랜덤 영화 선택 함수 수정
  const selectRandomMovie = () => {
    const movies = movieStore.filteredMovies;
    if (movies.length > 0) {
      const randomIndex = Math.floor(Math.random() * movies.length);
      selectedMovie.value = movies[randomIndex];
      console.log("Selected movie:", selectedMovie.value); // 디버깅용
    }
  };
  
  // filteredMovies 변경 감지
  watch(
    () => movieStore.filteredMovies,
    (newMovies) => {
      if (newMovies.length > 0) {
        // 선호도 설정 여부와 관계없이 항상 랜덤 영화 선택
        selectRandomMovie();
      }
    },
    { immediate: true }
  );
  
  const username = computed(() => counterStore.username);
  const hasPreferences = computed(
    () => movieStore.selectedRegion && movieStore.selectedGenres.length > 0
  );
  
  const selectedMovieTitle = computed(() => {
    return selectedMovie.value?.title || "추천 영화"; // 추천 영화 제목을 없으면 기본값 사용
  });
  const genres = [
    { id: 28, name: "Action" },
    { id: 12, name: "Adventure" },
    { id: 16, name: "Animation" },
    { id: 35, name: "Comedy" },
    { id: 80, name: "Crime" },
    { id: 99, name: "Documentary" },
    { id: 18, name: "Drama" },
    { id: 10751, name: "Family" },
    { id: 14, name: "Fantasy" },
    { id: 36, name: "History" },
    { id: 27, name: "Horror" },
    { id: 10402, name: "Music" },
    { id: 9648, name: "Mystery" },
    { id: 10749, name: "Romance" },
    { id: 878, name: "Science Fiction" },
    { id: 10770, name: "TV Movie" },
    { id: 53, name: "Thriller" },
    { id: 10752, name: "War" },
    { id: 37, name: "Western" },
  ];
  
  const selectRegion = (region) => {
    movieStore.setSelectedRegion(region);
  };
  
  const selectGenre = (genreId) => {
    movieStore.setSelectedGenre(genreId);
  };
  
  const isGenreSelected = (genreId) => {
    return movieStore.selectedGenres.some((g) => g.id === genreId);
  };
  
  const canComplete = computed(() => movieStore.selectedGenres.length >= 2);
  
  const completeSelection = () => {
    if (canComplete.value && movieStore.selectedRegion) {
      isPreferenceCompleted.value = true;
      router.push({ name: "filtered-movies" });
    }
  };
  // 배너 스타일 계산
  const bannerStyle = computed(() => {
    if (selectedMovie.value?.poster_path) {
      return {
        backgroundImage: `linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url(https://image.tmdb.org/t/p/original${selectedMovie.value.poster_path})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        cursor: "pointer",
      };
    }
    return {};
  });
  
  // 영화 상세 페이지로 이동
  const goToMovieDetail = () => {
    if (selectedMovie.value) {
      router.push({
        name: "MovieDetail",
        params: { id: selectedMovie.value.id },
      });
    }
  };
  
  // 장르 이름을 가져오는 computed 속성
  const selectedGenresText = computed(() => {
    if (movieStore.selectedGenres.length > 0) {
      return movieStore.selectedGenres.map((genre) => genre.name).join(", ");
    }
    return null; // 장르가 없으면 null 반환
  });
  
  // 지역 텍스트 계산
  const selectedRegionText = computed(() => {
    return movieStore.selectedRegion === "domestic" ? "국내" : "해외";
  });
  
  // 기타 메서드들 생략
  // onMounted 수정
  onMounted(async () => {
    try {
      await movieStore.loadUserPreferences();
      await movieStore.fetchMovies();
      // 이전에 저장된 선호도가 있는지 확인
      if (movieStore.selectedRegion && movieStore.selectedGenres.length >= 2) {
        isPreferenceCompleted.value = true;
      }
    } catch (error) {
      console.error("Error loading data:", error);
    }
  });
  </script>
  
  <style scoped>
  .main-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 3rem;
  }
  
  .main-banner {
    position: relative;
    background-size: cover;
    background-position: center;
    height: 400px;
    transition: transform 0.3s ease-in-out;
    cursor: pointer;
    border-radius: 10px;
  }
  
  .main-banner:hover {
    transform: scale(1.05);
  }
  
  .banner-content {
    position: relative;
    z-index: 1;
    color: white;
    padding: 20px;
    backdrop-filter: blur(5px);
  }
  
  h1 {
    font-size: 3rem;
    font-weight: 600;
    margin-bottom: 1rem;
  }
  
  .featured-movie-title {
    font-size: 2rem;
    font-weight: 500;
    text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.7);
  }
  
  .genre-description {
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.8);
    margin-top: 1rem;
  }
  
  .no-preference-message {
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.8);
    margin-top: 1rem;
    text-align: center;
  }
  
  .movie-recommendations h2 {
    font-size: 2rem;
    font-weight: 600;
    margin-bottom: 1rem;
    text-align: center;
    color: #333;
  }
  
  .movie-carousel {
    display: flex;
    gap: 20px;
    transition: transform 0.3s ease;
  }
  
  .region-selection,
  .genre-selection {
    background-color: #f4f4f4;
    border-radius: 8px;
    padding: 2rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  h3 {
    font-size: 1.5rem;
    font-weight: 500;
    margin-bottom: 1rem;
  }
  
  .button-group {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 1.5rem;
  }
  
  .region-btn,
  .genre-btn {
    padding: 12px 24px;
    font-size: 1rem;
    border: 2px solid #007bff;
    border-radius: 8px;
    background-color: white;
    color: #007bff;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .region-btn:hover,
  .genre-btn:hover,
  .genre-btn.active {
    background-color: #007bff;
    color: white;
    border-color: #0056b3;
  }
  
  .genre-buttons {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
    margin-top: 2rem;
  }
  
  .complete-btn {
    display: block;
    width: 240px;
    margin: 2rem auto;
    padding: 12px;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 1.1rem;
    cursor: pointer;
  }
  
  .complete-btn:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
  
  .complete-btn:hover:not(:disabled) {
    background-color: #218838;
  }
  
  .carousel-container {
    position: relative;
    display: flex;
    align-items: center;
    padding: 0 40px;
    overflow: hidden;
  }
  
  .movie-card {
    flex: 0 0 auto;
    width: 220px;
  }
  
  .nav-button {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(0, 0, 0, 0.5);
    color: white;
    border: none;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    cursor: pointer;
    z-index: 1;
  }
  
  .prev {
    left: 0;
  }
  
  .next {
    right: 0;
  }
  </style>
  