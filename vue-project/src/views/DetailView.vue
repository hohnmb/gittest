<template>
  <div class="board-container">
    <h1>게시글 상세</h1>
    <div v-if="article" class="article-container">
      <!-- 게시글 정보 -->
      <div class="article-detail">
        <p class="article-id">NO : {{ article.id }}</p>
        <hr />
        <h2 class="article-title">{{ article.title }}</h2>
        <p class="article-content">{{ article.content }}</p>
        <hr />
        <p class="article-author">
          <router-link :to="{ name: 'UserProfile', params: { username: article.username }}"
    class="author-link"
  >
    {{ article.username }}
  </router-link>
        </p>
        <p class="article-date">
          작성일 : {{ formatDate(article.created_at) }}
        </p>
        <p class="article-update">
          수정일 : {{ formatDate(article.updated_at) }}
        </p>

        <div class="like-section">
          <!-- 좋아요 버튼 수정 -->
          <button
            @click="handleLikeClick"
            :class="{ liked: article.is_liked }"
            class="like-button"
          >
            {{ article.is_liked ? "❤️" : "🤍" }}
            좋아요 ({{ article.like_count }})
          </button>
        </div>
      </div>

      <!-- 댓글 목록 -->
      <div class="comments-section">
        <!-- 댓글 작성 폼 -->
        <CommentForm
          :comments="article.comment_set"
          @comment-created="getArticleDetail"
        />
      </div>

      <!-- 게시글 수정 및 삭제 버튼 -->
      <div class="action-buttons">
        <button @click="goToList">목록으로</button>
        <button
          v-if="article.username === store.username"
          @click="goToEdit"
          class="edit-btn"
        >
          수정
        </button>
        <button
          v-if="article.username === store.username"
          @click="deletePost"
          class="delete-btn"
        >
          삭제
        </button>
      </div>
    </div>
  </div>
  <!-- 로그인 모달 추가 -->
  <LoginModal ref="loginModal" @login-success="handleLoginSuccess" />
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRoute, useRouter } from "vue-router";
import CommentForm from "./CommentForm.vue";
import CommentList from "./CommentList.vue";
import LoginModal from "./LoginModal.vue";  // 로그인 모달 import 추가

const store = useCounterStore();
const route = useRoute();
const router = useRouter();
const article = ref(null);
const loginModal = ref(null);  // 로그인 모달 ref 추가

// 좋아요 버튼 클릭 핸들러 추가
const handleLikeClick = async () => {
  if (!store.token) {
    loginModal.value.show();
    return;
  }
  await toggleLike();
};

// 로그인 성공 핸들러 추가
const handleLoginSuccess = async () => {
  await toggleLike();
  loginModal.value.hide();
};

// 좋아요 토글 함수 수정
const toggleLike = async () => {
  try {
    const response = await axios.post(
      `${store.API_URL}/api/v1/community/${route.params.id}/like/`,
      {},
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );

    article.value.is_liked = response.data.liked;
    article.value.like_count = response.data.like_count;
  } catch (error) {
    console.error("Error:", error);
    alert("좋아요 처리 중 오류가 발생했습니다.");
  }
};

// 게시글 삭제
const deletePost = async () => {
  if (!confirm("정말 삭제하시겠습니까?")) {
    return;
  }

  try {
    await axios({
      method: "delete",
      url: `${store.API_URL}/api/v1/community/${route.params.id}/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });

    alert("게시글이 삭제되었습니다.");
    router.push({ name: "ArticleList" });
  } catch (err) {
    console.error(err);
    if (err.response?.status === 401) {
      alert("권한이 없습니다.");
    } else if (err.response?.status === 404) {
      alert("게시글을 찾을 수 없습니다.");
    } else {
      alert("게시글 삭제 중 오류가 발생했습니다.");
    }
  }
};

// 수정 페이지로 이동
const goToEdit = () => {
  router.push({
    name: "ArticleEditView",
    params: { id: route.params.id },
  });
};

// 날짜 포맷팅 함수
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

// 게시글 상세 정보 가져오기
const getArticleDetail = async () => {
  try {
    const response = await axios({
      method: "get",
      url: `${store.API_URL}/api/v1/community/${route.params.id}/`,
      headers: store.token ? {
        Authorization: `Token ${store.token}`
      } : {}
    });
    article.value = response.data;
  } catch (err) {
    console.log(err);
  }
};

const goToList = () => {
  router.push({ name: "ArticleList" });
};

onMounted(() => {
  getArticleDetail();
});
</script>

<style scoped>
.author-link {
  color: #1a73e8;
  text-decoration: none;
  cursor: pointer;
  transition: color 0.2s ease;
}

.author-link:hover {
  color: #1557b0;
  text-decoration: underline;
}
.like-section {
  margin: 20px 0;
  text-align: center;
}

.like-button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 20px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.like-button.liked {
  background-color: #ffebee;
  border-color: #ff4081;
  color: #ff4081;
}

.like-button:hover {
  transform: scale(1.05);
}
.board-container {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
}


h1 {
  text-align: center;
  font-size: 2em;
  margin-bottom: 20px;
}

.article-container {
  width: 100%;
  box-sizing: border-box;
}

.article-detail {
  margin-bottom: 30px;
}

.article-id,
.article-title,
.article-author,
.article-date,
.article-update {
  margin: 10px 0;
}

.article-title {
  font-size: 1.5em;
  font-weight: bold;
  margin-bottom: 10px;
}

.article-content {
  font-size: 1.2em;
  line-height: 1.6;
}

.comments-section {
  width: 100%;
  box-sizing: border-box;
  margin: 20px 0;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  overflow: hidden; /* 내용이 넘치지 않도록 */
}

.comments-list h3 {
  font-size: 1.3em;
  margin-bottom: 15px;
}

.comment-item {
  background-color: #fff;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.comment-content {
  font-size: 1em;
  margin-bottom: 10px;
}

.comment-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.9em;
  color: #777;
}

.comment-author {
  font-weight: bold;
}

.comment-date {
  color: #999;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s;
}

button:hover {
  opacity: 0.8;
}

button:disabled {
  cursor: not-allowed;
  background-color: #ccc;
}

.edit-btn {
  background-color: #4caf50;
  color: white;
}

.edit-btn:hover {
  background-color: #45a049;
}

.delete-btn {
  background-color: #f44336;
  color: white;
}

.delete-btn:hover {
  background-color: #d32f2f;
}

button:focus {
  outline: none;
}
</style>
