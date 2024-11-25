<template>
    <div class="edit-review-modal">
      <div class="modal-content">
        <h2>리뷰 수정</h2>
        <div class="edit-form">
          <textarea 
            v-model="editedContent" 
            class="review-textarea"
            placeholder="리뷰 내용을 수정해주세요"
          ></textarea>
          <div class="rating-select">
            <span
              v-for="star in 5"
              :key="star"
              @click="setRating(star)"
              :class="{ 'selected': editedRating >= star }"
            >
              ⭐
            </span>
          </div>
          <div class="button-group">
            <button @click="saveEdit" class="save-btn">저장</button>
            <button @click="cancelEdit" class="cancel-btn">취소</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import { useCounterStore } from '@/stores/counter'
  
  const props = defineProps({
    review: {
      type: Object,
      required: true
    }
  })
  
  const emit = defineEmits(['update', 'close'])
  const store = useCounterStore()
  const editedContent = ref('')
  const editedRating = ref(5)
  
  onMounted(() => {
    editedContent.value = props.review.content
    editedRating.value = props.review.rating
  })
  
  const setRating = (value) => {
    editedRating.value = value
  }
  
  const saveEdit = async () => {
    try {
      const response = await axios({
        method: 'put',
        url: `${store.API_URL}/api/v1/movies/reviews/${props.review.id}/`,
        data: {
          content: editedContent.value,
          rating: editedRating.value,
          movie: props.review.movie
        },
        headers: {
          Authorization: `Token ${store.token}`,
          'Content-Type': 'application/json'
        }
      })
      emit('update', response.data)
      emit('close')
    } catch (error) {
      console.error('리뷰 수정 실패:', error)
      alert('리뷰 수정에 실패했습니다.')
    }
  }
  
  const cancelEdit = () => {
    emit('close')
  }
  </script>
  
  <style scoped>
  .edit-review-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    width: 90%;
    max-width: 500px;
  }
  
  .button-group {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
  }
  
  .save-btn, .cancel-btn {
    padding: 0.5rem 1rem;
    border-radius: 4px;
    border: none;
    cursor: pointer;
  }
  
  .save-btn {
    background: #5c6bc0;
    color: white;
  }
  
  .cancel-btn {
    background: #e0e0e0;
  }
  </style>