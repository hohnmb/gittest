<template>
  <header>
    <nav class="navbar">
      <!-- 왼쪽에 커뮤니티 링크 -->
      <RouterLink :to="{ name: 'MainView' }" class="nav-link">Home</RouterLink>
      <RouterLink :to="{ name: 'ArticleList' }" class="nav-link"
        >커뮤니티</RouterLink
      >
      <RouterLink :to="{ name: 'MovieRecommendView' }" class="nav-link"
        >영화 추천</RouterLink
      >
      <RouterLink :to="{ name: 'MovieView' }" class="nav-link"
        >영화 목록</RouterLink
      >
      <RouterLink :to="{ name: 'LatestMoviesView' }" class="nav-link"
        >최신 영화 목록</RouterLink
      >
      <!-- 추가 -->

      <div class="auth-links" v-if="!username">
        <RouterLink :to="{ name: 'SignUpView' }" class="nav-link"
          >회원가입</RouterLink
        >
        <RouterLink :to="{ name: 'LogInView' }" class="nav-link"
          >로그인</RouterLink
        >
      </div>

      <div class="user-links" v-if="username">
        <RouterLink
          :to="{ name: 'UserProfile', params: { username: store.username } }"
          class="nav-link user-link"
        >
          {{ store.username }}
        </RouterLink>
        <form @submit.prevent="logOut" class="logout-form">
          <input type="submit" value="Logout" class="logout-button" />
        </form>
      </div>
    </nav>
  </header>

  <RouterView />
</template>

<script setup>
import { RouterView, RouterLink } from "vue-router";
import { storeToRefs } from "pinia";
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
const { username } = storeToRefs(store);

const logOut = function () {
  store.logOut();
};
</script>

<style scoped>
/* 전체 초기화 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
  background-color: #121212; /* 어두운 배경 */
  color: #ffffff; /* 흰색 텍스트 */
  font-family: "Arial", sans-serif;
}

/* 헤더 스타일 */
header {
  background-color: #000000; /* 헤더 어두운 배경 */
  padding: 20px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.5); /* 헤더 그림자 */
}

.navbar {
  display: flex;
  justify-content: space-between; /* 양 끝으로 배치 */
  align-items: center;
}

.navbar .nav-link {
  font-size: 1.2rem; /* 글자 크기 키우기 */
  font-weight: bold; /* 글자 굵게 */
  color: #ffffff; /* 흰색 텍스트 */
  text-decoration: none; /* 밑줄 제거 */
  padding: 10px 15px; /* 여백 추가 */
  transition: color 0.3s, transform 0.2s;
}

.navbar .nav-link:hover {
  color: #4caf50; /* 초록색 강조 */
}

.auth-links,
.user-links {
  display: flex;
  gap: 20px; /* 링크 간격 넓히기 */
}

/* 사용자 링크 스타일 */
.user-link {
  font-weight: bold;
}

/* 로그아웃 버튼 스타일 */
.logout-button {
  background-color: #f44336; /* 빨간색 배경 */
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
}

.logout-button:hover {
  background-color: #d32f2f; /* 더 어두운 빨간색으로 변경 */
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column; /* 작은 화면에서는 세로로 배치 */
    gap: 15px;
    text-align: center;
    padding-bottom: 10px;
    border-bottom: solid thin rgba(255, 255, 255, 0.2);
  }
}
</style>
