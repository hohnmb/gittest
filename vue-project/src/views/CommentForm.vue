<template>
  <div class="comment-form">
    <!-- 댓글 목록 표시 -->
    <CommentList :comments="comments" />
    <textarea
      v-model="content"
      placeholder="댓글을 입력하세요"
      rows="4"
      class="comment-input"
    ></textarea>
    <button @click="handleCommentSubmit" :disabled="!content.trim()">
      댓글 작성
    </button>
  </div>
  <LoginModal ref="loginModal" />
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRoute } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import CommentList from "./CommentList.vue";
import LoginModal from "./LoginModal.vue";

// comments prop 추가
const props = defineProps({
  comments: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const emit = defineEmits(["comment-created"]);

const content = ref(""); // 댓글 내용
const store = useCounterStore();
const route = useRoute(); // 게시글의 ID 가져오기

const submitComment = async () => {
  if (!store.token) {
    alert("로그인 후 댓글을 작성해주세요.");
    return;
  }

  try {
    // 게시글 ID와 댓글 내용으로 댓글 작성 요청
    const response = await axios.post(
      `${store.API_URL}/api/v1/community/${route.params.id}/comments/`,
      {
        content: content.value,
        post_id: route.params.id,
      },
      {
        headers: {
          Authorization: `Token ${store.token}`,
          "Content-Type": "application/json",
        },
      }
    );
    console.log("댓글 작성 응답:", response.data); // 응답 확인용
    content.value = ""; // 댓글 작성 후 입력창 초기화
    emit("comment-created"); // 부모 컴포넌트에 댓글 생성 알림
  } catch (error) {
    console.error("Error response:", error.response);
    console.error("Error message:", error.message);
    alert("댓글 작성에 실패했습니다.");
  }
};
const loginModal = ref(null);

const handleCommentSubmit = async () => {
  if (!store.token) {
    loginModal.value.show();
    return;
  }
  await submitComment();
};
</script>

/* CommentForm.vue의 스타일 수정 */
<style scoped>
.comment-form {
  width: 100%;
  max-width: 100%;
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  margin: 20px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

textarea {
  width: 100%;
  box-sizing: border-box;
  padding: 15px;
  margin-bottom: 15px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  resize: vertical;
  min-height: 100px;
}

.comments-section {
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 20px;
  box-sizing: border-box;
  background-color: #f8f9fa;
  border-radius: 8px;
}

/* 버튼 컨테이너 추가 */
.button-container {
  display: flex;
  justify-content: flex-end;
  width: 100%;
}

button {
  padding: 12px 24px;
  background-color: #1e3a8a;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
</style>
