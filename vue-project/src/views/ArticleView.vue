<template>
  <div class="article-form-container">
    <h1 class="form-title">게시글 작성</h1>
    <form @submit.prevent="createArticle" class="article-form">
      <div class="form-group">
        <label for="title">제목</label>
        <input
          type="text"
          id="title"
          v-model.trim="title"
          required
          placeholder="게시글 제목을 입력하세요"
          class="form-input"
        />
      </div>
      <div class="form-group">
        <label for="content">내용</label>
        <textarea
          id="content"
          v-model.trim="content"
          required
          placeholder="게시글 내용을 입력하세요"
          class="form-textarea"
        ></textarea>
      </div>
      <div class="button-group">
        <input type="submit" value="작성하기" class="submit-button" />
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";
import { useRouter } from "vue-router";

const title = ref(null);
const content = ref(null);
const store = useCounterStore();
const router = useRouter();

// DRF로 게시글 생성 요청을 보내는 함수
const createArticle = function () {
  if (!title.value || !content.value) {
    alert("제목과 내용을 모두 입력해주세요.");
    return;
  }

  axios({
    method: "post",
    url: `${store.API_URL}/api/v1/community/`,
    data: {
      title: title.value,
      content: content.value,
      user: store.userId,
    },
    headers: {
      Authorization: `Token ${store.token}`,
      "Content-Type": "application/json",
    },
  })
    .then((res) => {
      // console.log('게시글 작성 성공!')
      router.push({ name: "ArticleView" });
    })
    .catch((err) => {
      console.log(err.response?.data || err.message);
      alert("게시글 작성에 실패했습니다.");
    });
};
</script>

<style scoped>
.article-form-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 40px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.form-title {
  text-align: center;
  font-size: 2rem;
  color: #333;
  margin-bottom: 30px;
}

.article-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

label {
  font-size: 1.1rem;
  font-weight: bold;
  color: #444;
}

.form-input,
.form-textarea {
  padding: 12px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  background-color: #fff;
  transition: all 0.3s ease-in-out;
}

.form-input:focus,
.form-textarea:focus {
  border-color: #4caf50;
  outline: none;
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.5);
}

.form-textarea {
  resize: vertical;
  min-height: 150px;
}

.placeholder {
  color: #888;
}

.submit-button {
  padding: 12px 25px;
  background-color: #4caf50;
  color: white;
  font-size: 1.1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.submit-button:hover {
  background-color: #45a049;
  transform: scale(1.05);
}

.submit-button:active {
  transform: scale(1);
}

.submit-button:focus {
  outline: none;
}

.button-group {
  display: flex;
  justify-content: center;
}

@media (max-width: 600px) {
  .article-form-container {
    padding: 20px;
  }

  .form-title {
    font-size: 1.8rem;
  }

  .form-input,
  .form-textarea {
    font-size: 1rem;
  }

  .submit-button {
    font-size: 1rem;
    padding: 10px 20px;
  }
}
</style>
