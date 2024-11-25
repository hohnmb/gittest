<template>
  <div class="article-item">
    <table>
      <tbody>  <!-- tbody 태그 추가 -->
        <tr>
          <td class="article-id">{{ article.id }}</td>
          <td class="article-title">
            <RouterLink :to="{ name: 'DetailView', params: { id: article.id } }">
              {{ article.title }}
            </RouterLink>
          </td>
          <td class="article-author">{{ article.username }}</td>
          <td class="article-date">{{ formatDate(article.created_at) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";

const props = defineProps({
  article: {
    type: Object,
    required: true,
    default: () => ({
      id: null,
      username: "",
      title: "",
      created_at: null,
    }),
    validator(article) {
      return article && typeof article.id === "number";
    },
  },
});

const formatDate = (dateString) => {
  if (!dateString) return "";
  try {
    return new Date(dateString).toLocaleDateString("ko-KR", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    });
  } catch (error) {
    console.error("날짜 변환 오류:", error);
    return dateString;
  }
};
</script>

<style scoped>
.article-item {
  width: 100%;
  border-bottom: 1px solid #eee;
}

table {
  width: 100%;
  border-collapse: collapse;
}

tr {
  height: 50px;
}

td {
  padding: 10px;
  vertical-align: middle;
}

.article-id {
  width: 8%;
  text-align: center;
  color: #666;
}

.article-title {
  width: 50%;
  text-align: left;
}

.article-title a {
  color: #333;
  text-decoration: none;
}

.article-title a:hover {
  color: #007bff;
  text-decoration: underline;
}

.article-author {
  width: 20%;
  text-align: center;
  color: #666;
}

.article-date {
  width: 22%;
  text-align: center;
  color: #888;
  font-size: 0.9em;
}

tr:hover {
  background-color: #f8f9fa;
}
</style>
