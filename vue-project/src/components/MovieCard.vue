<template>
  <div class="movie-card">
    <img
      v-if="showPoster"
      :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
      :alt="movie.title"
      class="movie-poster"
      @click="showDetail ? goToDetail() : null"
    />
    <div>
      <div class="movie-info" @click="showDetail ? goToDetail() : null">
        <h3 v-if="showTitle">{{ movie.title }}</h3>
        <p v-if="showOverview" class="movie-overview">{{ movie.overview }}</p>
        <div v-if="showDetails" class="movie-details">
          <span v-if="showRating">평점: {{ movie.vote_avg }}</span>
          <span v-if="showReleaseDate">개봉일: {{ movie.released_date }}</span>
        </div>
      </div>
      <div v-if="showLikeButton" class="like-section">
        <movie-like-button :movie="movie" />
      </div>
    </div>

    
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import MovieLikeButton from "../components/MovieLikeButton.vue";

const router = useRouter();

const props = defineProps({
  movie: {
    type: Object,
    required: true,
  },
  showPoster: {
    type: Boolean,
    default: true
  },
  showTitle: {
    type: Boolean,
    default: true
  },
  showOverview: {
    type: Boolean,
    default: true
  },
  showDetails: {
    type: Boolean,
    default: true
  },
  showRating: {
    type: Boolean,
    default: true
  },
  showReleaseDate: {
    type: Boolean,
    default: true
  },
  showLikeButton: {
    type: Boolean,
    default: true
  },
  showDetail: {
    type: Boolean,
    default: true
  },
  isLiked: {
    type: Boolean,
    default: true
  }
});

const emit = defineEmits(["like"]);

const goToDetail = () => {
  router.push({
    name: "MovieDetail",
    params: { id: props.movie.id }, // 영화 ID를 URL 파라미터로 전달
  });
};
</script>


<style scoped>
.movie-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease;
  cursor: pointer; /* 마우스 오버시 포인터 표시 */
}

.movie-card:hover {
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

.like-button {
  margin-top: 10px;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #f0f0f0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.like-button.liked {
  background-color: #ff4757;
  color: white;
}

.poster-container {
  cursor: pointer;
  overflow: hidden;
}
</style>
