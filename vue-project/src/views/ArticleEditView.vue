<template>
  <div class="edit-form">
    <h1>게시글 수정</h1>
    <form @submit.prevent="updateArticle">
      <div class="form-group">
        <label for="title">제목</label>
        <input type="text" id="title" v-model="form.title" required />
      </div>

      <div class="form-group">
        <label for="content">내용</label>
        <textarea
          id="content"
          v-model="form.content"
          rows="10"
          required
        ></textarea>
      </div>

      <div class="button-group">
        <button type="submit" class="submit-btn">수정하기</button>
        <button type="button" @click="cancel" class="cancel-btn">취소</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";

const store = useCounterStore();
const route = useRoute();
const router = useRouter();

const form = ref({
  title: "",
  content: "",
});

// 기존 게시글 정보 가져오기
const getArticle = async () => {
  try {
    const response = await axios({
      method: "get",
      url: `${store.API_URL}/api/v1/community/${route.params.id}/`,
    });
    form.value = {
      title: response.data.title,
      content: response.data.content,
    };
  } catch (err) {
    console.error(err);
    alert("게시글을 불러오는데 실패했습니다.");
    router.push({ name: "ArticleView" });
  }
};

// 게시글 수정
const updateArticle = async () => {
  try {
    await axios({
      method: "put",
      url: `${store.API_URL}/api/v1/community/${route.params.id}/`,
      data: form.value,
      headers: {
        Authorization: `Token ${store.token}`,
        "Content-Type": "application/json",
      },
    });

    alert("게시글이 수정되었습니다.");
    router.push({
      name: "DetailView",
      params: { id: route.params.id },
    });
  } catch (err) {
    console.error(err);
    if (err.response?.status === 401) {
      alert("권한이 없습니다.");
    } else {
      alert("게시글 수정 중 오류가 발생했습니다.");
    }
  }
};

const cancel = () => {
  if (confirm("수정을 취소하시겠습니까?")) {
    router.back();
  }
};

onMounted(() => {
  getArticle();
});
</script>

<style scoped>
.edit-form {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.button-group {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.submit-btn {
  background-color: #4caf50;
}

.cancel-btn {
  background-color: #9e9e9e;
}

button {
  padding: 8px 16px;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  opacity: 0.9;
}
</style>
