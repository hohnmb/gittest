<template>
  <div class="community-container">
    <div class="header-section">
      <h3>커뮤니티 게시판</h3>
     
    </div>
     <!-- 칼럼 헤더 추가 -->
     <div class="board-header">
      <div class="column id-column">NO</div>
      <div class="column title-column">
        <span class="title-text">제목</span>
      </div>
      <div class="column author-column">작성자</div>
      <div class="column date-column">작성일</div>
    </div>
    <!--v-for="article in store.articles"-->
    <ArticleListItem
      v-for="article in sortedArticles"  
      :key="article.id"
      :article="article"
    />
    <button 
      v-if="store.isLogin" 
      @click="goToCreateView" 
      class="create-button"
    >
      글쓰기
    </button>
  </div>
  
</template>

<script setup>
import { onMounted } from "vue";
import { useRouter } from 'vue-router';
import ArticleListItem from "@/components/ArticleListItem.vue";
import { useCounterStore } from "@/stores/counter";
import { storeToRefs } from 'pinia';
import { computed } from 'vue';

const sortedArticles = computed(() => {
  return [...store.articles].sort((a, b) => {
    return new Date(b.created_at) - new Date(a.created_at);
  });
});
const router = useRouter();
const store = useCounterStore();
const { articles } = storeToRefs(store);

const goToCreateView= () => {
  router.push({ name: 'CreateView' });
};

onMounted(() => {
  console.log('Current token:', store.token);
  console.log('Is logged in:', store.isLogin);
  store.getArticles();
});
</script>

<style scoped>
/* 칼럼 헤더 스타일 추가 */
.board-header {
  display: flex;
  background-color: #f8f9fa;
  padding: 15px 10px;
  border-top: 2px solid #4c66af;
  border-bottom: 1px solid #dee2e6;
  font-weight: bold;
  color: #495057;
  margin-bottom: 10px;
}

.column {
  text-align: center;
}

.id-column {
  width: 8%;
}

.title-column {
  width: 50%;
  display: flex;         /* Flexbox 추가 */
  justify-content: center; /* 가로 중앙 정렬 */
  align-items: center;    /* 세로 중앙 정렬 */
}
.title-text {
  display: inline-block;
  text-align: center;
}
.author-column {
  width: 20%;
}

.date-column {
  width: 22%;
}

.community-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 50px auto;
  margin-bottom: 30px;
}

h3 {
  font-size: 1.8rem;
  color: #333;
  margin: 0;
}

.create-button {
  padding: 12px 25px;
  background-color: #4c66af;
  color: white;
  font-size: 1.1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 3rem;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.create-button:hover {
  background-color: #455da0;
  transform: scale(1.05);
}

.create-button:active {
  transform: scale(1);
}

@media (max-width: 600px) {
  .board-header {
    padding: 10px 5px;
    font-size: 0.9rem;
  }
  
  .author-column,
  .date-column {
    font-size: 0.8rem;
  }

  .community-container {
    padding: 15px;
  }

  h3 {
    font-size: 1.5rem;
  }

  .create-button {
    font-size: 1rem;
    padding: 10px 20px;
  }
}
</style>


