### 로그인 직후 보낼 곳 정하기

페이지가 이상하게 버벅거렸다가 사용할 수 있게 되는 것 같음

```javascript
# stores/counter.js
const logIn = function (payload) {
    const { username: loginUsername, password: password } = payload
    const movieStore = useMovieStore()

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username: loginUsername,
        password,
      }
    })
      .then((res) => {
        token.value = res.data.key
        username.value = loginUsername
        movieStore.loadUserPreferences()  // loadUserSelections 대신 loadUserPreferences 사용
        router.push({ name: "MovieView" })
      })
      .catch((err) => {
        console.log(err)
      })
  }
```

### MovieCard에서 원하는 부분만 출력하는 방법

```javascript
<template>
  <div class="movie-card">
    <img
      v-if="showPoster"
      :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
      :alt="movie.title"
      class="movie-poster"
      @click="showDetail ? goToDetail() : null"
    />
    <div>
      <div class="movie-info" @click="showDetail ? goToDetail() : null">
        <h3 v-if="showTitle">{{ movie.title }}</h3>
        <p v-if="showOverview" class="movie-overview">{{ movie.overview }}</p>
        <div v-if="showDetails" class="movie-details">
          <span v-if="showRating">평점: {{ movie.vote_avg }}</span>
          <span v-if="showReleaseDate">개봉일: {{ movie.released_date }}</span>
        </div>
      </div>
      <div v-if="showLikeButton" class="like-section">
        <movie-like-button :movie="movie" />
      </div>
    </div>
  </div>
</template>
```

```javascript
const props = defineProps({
  movie: {
    type: Object,
    required: true,
  },
  showPoster: {
    type: Boolean,
    default: true
  },
  showTitle: {
    type: Boolean,
    default: true
  },
  showOverview: {
    type: Boolean,
    default: true
  },
  showDetails: {
    type: Boolean,
    default: true
  },
  showRating: {
    type: Boolean,
    default: true
  },
  showReleaseDate: {
    type: Boolean,
    default: true
  },
  showLikeButton: {
    type: Boolean,
    default: true
  },
  showDetail: {
    type: Boolean,
    default: true
  },
  isLiked: {
    type: Boolean,
    default: true
  }
});
```

# 수정 해야 할 것

> ~~댓글 작성하기 출력하기 댓글 문제 아직 있음 = > 완료~~
> 
> ~~게시글 수정하기 창은 뜨는데 수정 완료가 안 됨 => 완료~~
> 
> ~~로그인일 때 => 회원가입, 로그인 창 띄우지 않기 => 완료~~
> 
> ~~로그아웃은 제대로 됐다고 뜨는데 전혀 그게 반영이 안 되는 것 같음. => 완료~~
> 
> ~~게시글 작성하기 버튼은 로그인 상태일 떄만 보여줘야 함~~
> 
> ~~로그인 아닐 때도 게시판, 댓글은 볼 수 있게 하기.~~
> 
> ~~게시글 좋아요 만들기 -> 완료~~
> 
> ~~LOGOUT버튼은 로그인상태일때만 보여주기~~

# 게시글 출력시

### urls.py

```python
path('api/v1/community/', include('community.urls')),
path('api/v1/movies/', include('movies.urls')),
```

### 경로 제대로 넣기

```javascript
// counter.js
const getArticles = function () {
      const config = {
        method: "get",
        url: `${API_URL}/api/v1/community/`, // 경로 제대로 하기 ㅠㅠ
        headers: {
          Authorization: token.value ? `Token ${token.value}` : null,
        },
      };
```

#### 유저 이름 출력하기

```javascript
// App.vue
<script setup>
import { storeToRefs } from 'pinia'
import { RouterView, RouterLink } from "vue-router";
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
const { username } = storeToRefs(store)
```

### HMR 관련 설정 추가 : vite.config.js

```javascript
   // HMR 관련 설정 추가
  server: {
    hmr: true,
    watch: {
      usePolling: true
    }
  }
})
```

### axios 주요 메서드들

```javascript
axios의 주요 HTTP 메서드들:
axios.get(): 데이터 조회
axios.post(): 데이터 생성
axios.put(): 데이터 전체 수정
axios.patch(): 데이터 일부 수정
axios.delete(): 데이터 삭제
```

### 로그인 / 비로그인

```javascript
 <!-- 로그인하지 않은 경우에만 회원가입, 로그인 링크를 표시 -->
      <div class="auth-links" v-if="!username">
        <RouterLink :to="{ name: 'SignUpView' }" class="nav-link"
          >회원가입</RouterLink
        >
        <RouterLink :to="{ name: 'LogInView' }" class="nav-link"
          >로그인</RouterLink
        >
      </div>
```

```javascript
 <!-- 로그인한 경우에는 마이페이지와 로그아웃 링크를 표시 -->
      <div class="user-links" v-if="username">
        <RouterLink :to="{ name: 'MyPageView' }" class="nav-link user-link">{{
          store.username
        }}</RouterLink>
        <form @submit.prevent="logOut" class="logout-form">
          <input type="submit" value="Logout" class="logout-button" />
        </form>
      </div>
    </nav>
    <!-- 로그인 상태에 따른 환영 메시지 -->
    <h1 v-if="username" class="welcome-msg">
      영화 사이트입니다. {{ username }}님, 환영합니다!
    </h1>
    <h1 v-else class="welcome-msg">영화 사이트입니다. 로그인 후 사용하세요!</h1>
```

### 로그인 모달창 적용하기

로그인이 필요한 모든 기능에 로그인 모달을 적용할 수 있습니다. 로그아웃 상태는 Pinia store의 token과 isLogin 상태로 판단할 수 있습니다.

```javascript
const isLogin = computed(() => {
  if (token.value === null) {
    return false
  } else {
    return true
  }
})
```

따라서 기능 사용 전에 다음과 같이 체크할 수 있습니다:

```javascript
const handleAction = () => {
  if (!store.isLogin) {  // 또는 !store.token
    loginModal.value.show()
    return
  }
  // 실제 기능 수행
}
```

로그인이 필요한 주요 기능들:

1. 댓글 작성 : O
2. 게시글 작성/수정/삭제
3. 좋아요 기능
4. 마이페이지 접근

각 컴포넌트에서:

1. LoginModal 컴포넌트 import
2. ref로 모달 참조 생성
3. 기능 실행 전 로그인 상태 체크
4. 비로그인 시 모달 표시

이렇게 하면 일관된 로그인 경험을 제공할 수 있습니다.

### 로그아웃 상태 정확하게 하기

```javascript
const logOut = function () {
      axios({
        method: "post",
        url: `${API_URL}/accounts/logout/`,
        headers: {
          Authorization: `Token ${token.value}`, // 토큰 추가
        },
      })
        .then((res) => {
          console.log(res.data);
          clearUserData();
          // token.value = null;
          // username.value = null; // username도 null로 초기화
          router.push({ name: "ArticleView" });
        })
        .catch((err) => {
          console.log(err);
        });
    };
    const clearUserData = function () {
      token.value = null;
      username.value = null;
      localStorage.clear(); // localStorage 완전 초기화
    };
```

### 좋아요 페이지 벗어나면 하트 빈하트 되어있음

다시 좋아요 눌러서 색이 입혀지나? 했지만 좋아요 카운트 하나 줄어들 뿐

색이 변경된 채로 유지 되지 않는 것 같다. 데이터는 잘 들어가 있어도...

### 비로그인 좋아요 누르기 => 로그인 모달창

```javascript
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
```

```javascript
  <!-- 로그인 모달 추가 -->
  <LoginModal ref="loginModal" @login-success="handleLoginSuccess" />
</template>
```

```javascript
import LoginModal from "./LoginModal.vue";  // 로그인 모달 import 추가

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
```

### 회원 가입 후 영화 목록 페이지로 보내기 설정

영화 목록을 보거나 게시판을 보다가 회원가입을 누르고

회원가입을 하고 나면 다시 보던 페이지로 보내주는건?

```javascript
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
```
