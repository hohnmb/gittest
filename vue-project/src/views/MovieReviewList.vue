<template>
  <div class="reviews-list">
    <h2 class="reviews-title">리뷰 ({{ reviews.length }})</h2>
    <div v-if="reviews.length > 0" class="reviews-container">
      <div v-for="review in reviews" :key="review.id" class="review">
        <div class="review-header">
          <div class="user-rating">
            <span class="review-author">{{ review.user }}</span>
            <!-- 수정 모드일 때는 별점 수정 가능하게 -->
            <div v-if="editingReviewId === review.id" class="rating-select">
              <span
                v-for="star in 5"
                :key="star"
                @click="editedRating = star"
                :class="{ 'selected': editedRating >= star }"
              >
                ⭐
              </span>
            </div>
            <span v-else class="rating">{{ '⭐'.repeat(review.rating) }}</span>
          </div>
          <div class="date-info">
            <span class="review-date">{{ formatDate(review.created_at) }}</span>
            <span v-if="review.updated_at && review.updated_at !== review.created_at" 
                  class="updated-date">
              (수정됨: {{ formatDate(review.updated_at) }})
            </span>
          </div>
        </div>
        <!-- 수정 모드일 때는 textarea 표시 -->
        <div v-if="editingReviewId === review.id">
          <textarea 
            v-model="editedContent" 
            class="review-textarea"
          ></textarea>
          <div class="edit-actions">
            <button @click="saveEdit(review)" class="action-button">저장</button>
            <button @click="cancelEdit" class="action-button">취소</button>
          </div>
        </div>
        <!-- 일반 모드일 때는 내용 표시 -->
        <p v-else class="review-content">{{ review.content }}</p>
        <div class="review-footer">
          <button 
            @click="$emit('toggle-like', review)"
            :class="{ 'liked': review.is_liked }"
            class="like-button"
          >
            ❤️ {{ review.like_count || 0 }}
          </button>
          <div v-if="review.user === currentUser" class="review-actions">
            <button v-if="editingReviewId !== review.id" 
              @click="startEdit(review)" 
              class="action-button"
            >
              수정
            </button>
            <button @click="$emit('delete-review', review.id)" class="action-button delete">
              삭제
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="no-reviews">
      <p>아직 작성된 리뷰가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  reviews: {
    type: Array,
    required: true,
    default: () => [],
  },
  currentUser: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['toggle-like', 'edit-review', 'delete-review'])

const editingReviewId = ref(null)
const editedContent = ref('')
const editedRating = ref(5)

const startEdit = (review) => {
  editingReviewId.value = review.id
  editedContent.value = review.content
  editedRating.value = review.rating
}

const saveEdit = (review) => {
  emit('edit-review', {
    ...review,
    content: editedContent.value,
    rating: editedRating.value
  })
  editingReviewId.value = null
}

const cancelEdit = () => {
  editingReviewId.value = null
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
  .date-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  font-size: 0.8em;
  color: #666;
}

.updated-date {
  font-size: 0.9em;
  color: #888;
  font-style: italic;
  margin-top: 2px;
}

/* 나머지 기존 스타일 */
.reviews-list {
  width: 100%;
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* 개별 리뷰 항목 */
.review {
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 15px;
  padding: 15px;
  background-color: #f3f4f6; /* 리뷰 배경을 좀 더 어두운 색상으로 변경 */
  border-radius: 8px;
  transition: background-color 0.2s ease;
}
.reviews-title {
    color : #1e3a8a;
}
/* 리뷰 항목에 마우스를 올리면 색상이 변하도록 */
.review:hover {
  background-color: #e2e8f0; /* 호버 시 밝은 색으로 변 */
}

/* 리뷰 헤더 스타일 */
.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

/* 리뷰 작성자 및 별점 */
.user-rating {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* 리뷰 내용 */
.review-content {
  margin-top: 10px;
  padding: 5px;
  line-height: 1.5;
  color: #333; /* 리뷰 내용 텍스트 색상을 어두운 색으로 변경 */
}

/* 작성자 이름 */
.review-author {
  font-weight: bold;
  color: #1e3a8a; /* 작성자 이름 색상 변경 */
}

/* 리뷰 작성 날짜 */
.review-date {
  color: #666;
  font-size: 0.9em;
}

/* 별점 스타일 */
.rating {
  color: #fbbf24; /* 별점 색상 */
}

/* 리뷰 푸터 (좋아요 버튼 및 액션 버튼) */
.review-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  padding-top: 8px;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

/* 좋아요 버튼 스타일 */
.like-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

/* 좋아요 버튼 호버 효과 */
.like-button:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

/* 좋아요 버튼이 선택된 상태 */
.like-button.liked {
  color: #dc2626;
}

/* 리뷰 삭제 및 수정 버튼 */
.review-actions {
  display: flex;
  gap: 8px;
}

/* 기본 버튼 스타일 */
.action-button {
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #e5e7eb;
  color: #374151;
  transition: background-color 0.2s;
}

/* 버튼 호버 시 색상 변경 */
.action-button:hover {
  background-color: #d1d5db;
}

/* 삭제 버튼 스타일 */
.action-button.delete {
  background-color: #fee2e2;
  color: #dc2626;
}

.action-button.delete:hover {
  background-color: #fecaca;
}

/* 리뷰가 없을 때의 메시지 스타일 */
.no-reviews {
  text-align: center;
  padding: 20px;
  color: #666;
}

/* 댓글 작성 textarea 스타일 */
.review-textarea {
  width: 100%;
  min-height: 80px;
  margin: 10px 0;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}

/* 수정 버튼 관련 액션 */
.edit-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  margin-bottom: 10px;
}

/* 별점 선택 스타일 */
.rating-select {
  display: flex;
  gap: 4px;
}

.rating-select span {
  cursor: pointer;
}

.rating-select span.selected {
  opacity: 1;
}
  </style>