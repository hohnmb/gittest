<template>
  <div class="signup-container">
    <div class="signup-box">
      <h1 class="title">CREATE ACCOUNT</h1>
      <form @submit.prevent="signUp" class="signup-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input 
            type="text" 
            id="username" 
            v-model.trim="username"
            placeholder="Enter your username"
          >
        </div>

        <div class="form-group">
          <label for="password1">Password</label>
          <input 
            type="password" 
            id="password1" 
            v-model.trim="password1"
            placeholder="Enter your password"
          >
        </div>

        <div class="form-group">
          <label for="password2">Confirm Password</label>
          <input 
            type="password" 
            id="password2" 
            v-model.trim="password2"
            placeholder="Confirm your password"
          >
        </div>
        
        <button type="submit">Sign Up</button>
      </form>
    </div>
  </div>
</template>


<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from 'vue-router'; // 라우터 import 추가

const username = ref(null);
const password1 = ref(null);
const password2 = ref(null);
const router = useRouter(); // 라우터 설정
const store = useCounterStore();

const signUp = async function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
  };
  
  try {
    await store.signUp(payload);
    // 회원가입 성공 후 영화 목록 페이지로 리다이렉트
    router.push({ name: 'MovieView' });
  } catch (error) {
    console.error('회원가입 실패:', error);
  }
};
</script>
<style scoped>
.signup-container {
  display: flex;

  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #1e3a8a;
}

.signup-box {
   
  background: white;
  padding: 40px;
  border-radius: 20px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}
.signup-box {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.title {
  color: #1e3a8a;
  text-align: center;
  font-size: 28px;
  margin-bottom: 30px;
  font-weight: bold;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  color: #1e3a8a;
  margin-bottom: 8px;
  font-weight: 500;
}

input {

  width: 100%;
  padding: 12px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s;
}

input:focus {
  outline: none;
  border-color: #1e3a8a;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #1e3a8a;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #1e4b8a;
}

::placeholder {
  color: #9ca3af;
}

</style>