<!-- CommentList.vue -->
<template>
  <div class="comments-list">
    <h2 class="comments-title">댓글 ({{ comments.length }})</h2>
    <div v-if="comments.length > 0" class="comments-container">
      <div v-for="comment in comments" :key="comment.id" class="comment">
        <div class="comment-header">
          <span class="comment-author">{{ comment.user }}</span>
          <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
        </div>
        <p class="comment-content">{{ comment.content }}</p>
      </div>
    </div>
    <div v-else class="no-comments">
      <p>아직 작성된 댓글이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  comments: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};
</script>

<style scoped>
/* CommentList.vue의 스타일 수정 */
.comments-list {
  width: 100%;
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.comment {
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 15px;
  padding: 15px;
  background-color: #f8f9fa; /* 연한 회색 배경 */
  /*border-left: 4px solid #1e3a8a;   왼쪽 테두리 강조 */
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

/* 호버 효과 */
.comment:hover {
  background-color: #e2e8f0;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.comment-content {
  margin-top: 10px;
  padding: 5px;
  line-height: 1.5;
}

.comment-author {
  font-weight: bold;
  color: #1e3a8a;
}

.comment-date {
  color: #666;
  font-size: 0.9em;
}
</style>
