<template>
    <div class="review-section">
      <!-- 리뷰 작성 폼 -->
      <div class="review-form" v-if="!userHasReview && store.isLogin">
        <textarea 
          v-model="newReview.content" 
          placeholder="리뷰를 작성해주세요"
          class="review-textarea"
        ></textarea>
        <div class="rating-select">
          <span
            v-for="star in 5"
            :key="star"
            @click="setRating(star)"
            :class="{ 'selected': newReview.rating >= star }"
          >
            ⭐
          </span>
        </div>
        <button 
          @click="submitReview" 
          class="submit-btn"
          :disabled="!newReview.content.trim()"
        >
          리뷰 작성
        </button>
      </div>
  
      <!-- ReviewList 컴포넌트 사용 -->
      <MovieReviewList
  :reviews="reviews"
  :currentUser="store.username"
  @toggle-like="toggleLike"
  @edit-review="editReview"
  @delete-review="deleteReview"
/>
  
    
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import axios from 'axios'
  import { useCounterStore } from '@/stores/counter'
  import MovieReviewList from '../views/MovieReviewList.vue'
  //import MovieReviewEditView from './MovieReviewEditView.vue'
  const store = useCounterStore()
  const route = useRoute()
  const router = useRouter()
  const reviews = ref([])
  const userHasReview = ref(false)
  const newReview = ref({
    content: '',
    rating: 5
  })
//defineEmits(['update', 'close'])


const editReview = async (review) => {
  try {
    const response = await axios({
      method: 'put',
      url: `${store.API_URL}/api/v1/movies/reviews/${review.id}/`,
      data: {
        content: review.content,
        rating: review.rating,
        movie: route.params.id
      },
      headers: {
        Authorization: `Token ${store.token}`,
        'Content-Type': 'application/json'
      }
    })
    const index = reviews.value.findIndex(r => r.id === review.id)
    reviews.value[index] = response.data
  } catch (error) {
    console.error('리뷰 수정 실패:', error)
    alert('리뷰 수정에 실패했습니다.')
  }
}
  // 리뷰 목록 조회
  const fetchReviews = async () => {
    try {
      const response = await axios({
        method: 'get',
        url: `${store.API_URL}/api/v1/movies/${route.params.id}/reviews/`,
        headers: {
          Authorization: store.token ? `Token ${store.token}` : null
        }
      })
      reviews.value = response.data
      userHasReview.value = reviews.value.some(
        review => review.user === store.username
      )
    } catch (error) {
      console.error('리뷰 목록 조회 실패:', error)
    }
  }
  
  // 리뷰 작성
  const submitReview = async () => {
    if (!store.token) {
      alert('로그인 후 리뷰를 작성해주세요.')
      return
    }
  
    try {
      const response = await axios({
        method: 'post',
        url: `${store.API_URL}/api/v1/movies/${route.params.id}/reviews/`,
        data: {
          content: newReview.value.content,
          rating: newReview.value.rating,
          movie: route.params.id
        },
        headers: {
          Authorization: `Token ${store.token}`,
          'Content-Type': 'application/json'
        }
      })
      
      reviews.value.unshift(response.data)
      newReview.value.content = ''
      userHasReview.value = true
    } catch (error) {
      console.error('리뷰 작성 실패:', error)
      if (error.response?.status === 400) {
        alert('이미 리뷰를 작성했습니다.')
      } else {
        alert('리뷰 작성에 실패했습니다.')
      }
    }
  }
  
  // 리뷰 수정 핸들러 추가
const handleEditReview = async (review) => {
  try {
    const response = await axios({
      method: 'put',
      url: `${store.API_URL}/api/v1/movies/reviews/${review.id}/`,
      data: {
        content: review.content,
        rating: review.rating,
        movie: route.params.id
      },
      headers: {
        Authorization: `Token ${store.token}`,
        'Content-Type': 'application/json'
      }
    })
    
    const index = reviews.value.findIndex(r => r.id === review.id)
    if (index !== -1) {
      reviews.value[index] = response.data
    }
  } catch (error) {
    console.error('리뷰 수정 실패:', error)
    alert('리뷰 수정에 실패했습니다.')
  }
}

  
  // 리뷰 삭제
  const deleteReview = async (reviewId) => {
  if (!confirm('정말로 삭제하시겠습니까?')) return

  try {
    await axios({
      method: 'delete',
      url: `${store.API_URL}/api/v1/movies/reviews/${reviewId}/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    
    const index = reviews.value.findIndex(r => r.id === reviewId)
    reviews.value.splice(index, 1)
    userHasReview.value = false
  } catch (error) {
    console.error('리뷰 삭제 실패:', error)
    alert('리뷰 삭제에 실패했습니다.')
  }
}

const toggleLike = async (review) => {
  try {
    const response = await axios({
      method: 'post',
      url: `${store.API_URL}/api/v1/movies/reviews/${review.id}/like/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    
    const index = reviews.value.findIndex(r => r.id === review.id)
    reviews.value[index].is_liked = !reviews.value[index].is_liked
    reviews.value[index].like_count = response.data.like_count
  } catch (error) {
    console.error('좋아요 토글 실패:', error)
    if (!store.token) {
      alert('로그인이 필요한 기능입니다.')
    }
  }
}

  
  // 별점 설정
  const setRating = (value) => {
    newReview.value.rating = value
  }
  
  // 날짜 포맷팅
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
  const props = defineProps({
  movieId: {
    type: [String, Number],
    required: true
  }
})
  onMounted(() => {
    fetchReviews()
  })
  </script>
  
  <style scoped>
  .review-section {
    margin: 30px 0;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1); /* ★ 수정된 부분: 그림자 깊이 증가 */
  }
  
  .review-form {
    background-color: #fff;
    padding: 25px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* ★ 수정된 부분: 리뷰 작성 폼에 더 강한 그림자 */
  }
  
  textarea {
    width: 100%;
    height: 120px;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 8px;
    resize: none;
    font-size: 16px;
    color: #333;
    box-sizing: border-box;
    transition: border-color 0.3s ease;
  }
  
  textarea:focus {
    outline: none;
    border-color: #5c6bc0;
  }
  
  .rating-select {
    margin: 10px 0;
  }
  
  .rating-select span {
    cursor: pointer;
    font-size: 30px;
    color: #ffd700;
    transition: opacity 0.2s ease;
    opacity: 0.6;
  }
  
  .rating-select span.selected {
    opacity: 1;
  }
  
  .submit-btn {
    background-color: #5c6bc0;
    color: #fff;
    padding: 12px 25px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease, transform 0.2s ease;
  }
  
  .submit-btn:hover {
    background-color: #4a5cb8;
    transform: translateY(-2px);
  }
  
  .submit-btn:disabled {
    background-color: #bbb;
    cursor: not-allowed;
  }
  
  .review-list {
    margin-top: 30px;
  }
  
  .review-item {
    background-color: #fff;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  }
  
  .review-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  
  .review-content {
    font-size: 14px;
    color: #555;
    margin-bottom: 15px;
  }
  
  .review-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: #888;
  }
  
  .timestamp {
    font-size: 12px;
  }
  
  .like-btn {
    background: none;
    border: none;
    color: #ff4081;
    cursor: pointer;
    transition: color 0.3s ease;
  }
  
  .like-btn:hover {
    color: #d500f9;
  }
  
  .liked {
    color: #e53935;
  }
  
  .review-actions button {
    background: none;
    border: none;
    color: #5c6bc0;
    font-size: 14px;
    cursor: pointer;
    margin-left: 10px;
    transition: color 0.3s ease;
  }
  
  .review-actions button:hover {
    color: #3f51b5;
  }
  
  @media (max-width: 768px) {
    .review-section {
      margin: 15px;
    }
  
    .review-form,
    .review-item {
      padding: 15px;
    }
  
    .submit-btn {
      width: 100%;
    }
  }
  </style>
  