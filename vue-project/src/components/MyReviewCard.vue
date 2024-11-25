<template>
    <div class="review-card" @click="goToMovie">
      <div class="movie-poster">
        <img 
          :src="`https://image.tmdb.org/t/p/w200${review.movie_poster}`" 
          :alt="review.movie_title"
        >
      </div>
      <div class="review-content">
        <h3 class="movie-title">{{ review.movie_title }}</h3>
        <div class="rating">{{ '⭐'.repeat(review.rating) }}</div>
        <p class="review-text">{{ review.content }}</p>
        <div class="review-date">
          {{ formatDate(review.updated_at || review.created_at) }}
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router'
  
  const props = defineProps({
    review: {
      type: Object,
      required: true
    }
  })
  
  const router = useRouter()
  
  const goToMovie = () => {
    router.push(`/movies/${props.review.movie_id}`)
  }
  const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}

  </script>
  
  <style scoped>
  .review-card {
    display: flex;
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    margin-bottom: 20px;
  }
  
  .review-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
  .review-date {
  font-size: 0.8em;
  color: #888;
  margin-top: 8px;
  font-style: italic;
}
  .movie-poster {
    width: 120px;
    flex-shrink: 0;
  }
  
  .movie-poster img {
    width: 100%;
    height: 180px;
    object-fit: cover;
  }
  
  .review-content {
    padding: 15px;
    flex-grow: 1;
  }
  
  .movie-title {
    font-size: 1.2em;
    font-weight: bold;
    margin-bottom: 8px;
    color: #333;
  }
  
  .rating {
    color: #ffd700;
    margin-bottom: 8px;
  }
  
  .review-text {
    color: #666;
    font-size: 0.9em;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  </style>