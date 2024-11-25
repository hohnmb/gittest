<template>
    <button @click="handleLikeClick" :class="['like-button', { liked: isLiked }]">
      <!-- 좋아요 상태에 따른 하트 아이콘 -->
      <span class="heart-icon">
        {{ isLiked ? "❤️" : "🤍" }}
      </span>
      <!-- 좋아요 수 표시 -->
      <span class="like-count">{{ likeCount }}</span>
    </button>
  </template>
  
  <script setup>
  import { computed } from "vue";
  import { useCounterStore } from "../stores/counter";
  
  // 부모 컴포넌트에서 전달받은 movie 데이터
  const props = defineProps({
    movie: Object,
  });
  
  const store = useCounterStore();
  
  // 로그인 상태에 따른 하트 아이콘 처리
  const isLiked = computed(() => {
    // 로그인한 유저만 하트 이모티콘 상태를 반영
    if (store.isLogin) {
      return store.likeMovies[props.movie.id]?.is_liked || false;
    }
    return false; // 비로그인 상태일 때는 기본적으로 하트는 비어 있음 (🤍)
  });
  
  // 좋아요 수는 로그인 여부와 상관없이 계속 유지
  const likeCount = computed(
    () => store.likeMovies[props.movie.id]?.like_count || 0
  );
  
  // 좋아요 버튼 클릭 핸들러
  const handleLikeClick = async () => {
    if (!store.isLogin) {
      alert("로그인 후 좋아요를 누를 수 있습니다.");
      return;
    }
    store.toggleMovieLike(props.movie.id); // 좋아요 상태 토글
  };
  </script>
  
  <style scoped>
  .like-button {
    padding: 12px 24px;
    border: none;
    border-radius: 50px;
    background-color: #007bff;
    color: white;
    font-size: 1.1em;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: all 0.3s ease;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0, 123, 255, 0.2);
  }
  
  .like-button.liked {
    background-color: #ff5e57;
  }
  
  .heart-icon {
    font-size: 1.4em;
  }
  
  .like-count {
    font-size: 1.1em;
    font-weight: bold;
  }
  </style>
  