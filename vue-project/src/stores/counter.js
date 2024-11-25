import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useMovieStore } from './movie'

export const useCounterStore = defineStore('counter', () => {
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const likeMovies = ref({})  // { movieId: { is_liked: boolean, like_count: number } }
  const username = ref(null)
  const isLogin = computed(() => token.value !== null)
  const router = useRouter()

  const getArticles = function () {
    const config = {
      method: "get",
      url: `${API_URL}/api/v1/community/`,
      headers: {
        Authorization: token.value ? `Token ${token.value}` : null,
      },
    }

    axios(config)
      .then((res) => {
        articles.value = res.data
      })
      .catch((err) => {
        console.log("Full error:", err)
        if (err.response?.status === 404) {
          console.error("API 경로를 찾을 수 없습니다")
        } else if (err.response?.status === 401) {
          console.error("인증에 실패했습니다")
        }
      })
  }

  const signUp = function (payload) {
    const { username, password1, password2 } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2
      }
    })
      .then((res) => {
        const password = password1
        logIn({ username, password })
      })
      .catch((err) => {
        console.log(err.response?.data || err.message)
      })
  }

  const logIn = async (payload) => {
    const { username: loginUsername, password } = payload
    const movieStore = useMovieStore()

    try {
      const response = await axios.post(`${API_URL}/accounts/login/`, {
        username: loginUsername,
        password,
      })
      token.value = response.data.key
      username.value = loginUsername
      await fetchUserLikes()
      movieStore.loadUserPreferences()
      router.push({ name: "MovieRecommendView" })
    } catch (error) {
      console.error("Login error:", error)
    }
  }

  const logOut = async () => {
    const movieStore = useMovieStore()
    
    try {
      await axios.post(
        `${API_URL}/accounts/logout/`,
        {},
        { headers: { Authorization: `Token ${token.value}` } }
      )
      Object.keys(likeMovies.value).forEach((movieId) => {
        const currentCount = likeMovies.value[movieId].like_count
        likeMovies.value[movieId] = {
          is_liked: false,
          like_count: currentCount,
        }
      })
      movieStore.clearSelections()
      clearUserData()
      router.push({ name: "MovieView" })
    } catch (error) {
      console.error("Logout error:", error)
    }
  }

  const clearUserData = () => {
    token.value = null
    username.value = null
    localStorage.clear()
  }

  const toggleMovieLike = async (movieId) => {
    if (!isLogin.value) {
      alert("로그인 후 좋아요를 누를 수 있습니다.");
      return;
    }
  
    try {
      // TMDB 영화를 백엔드에 저장
      const saveResponse = await axios.post(
        `http://127.0.0.1:8000/api/v1/movies/${movieId}/save/`,
        {},
        { headers: { Authorization: `Token ${token.value}` } }
      );
  
      console.log("TMDB 영화 저장 응답:", saveResponse.data);
  
      // 좋아요 상태 토글
      const likeResponse = await axios.post(
        `http://127.0.0.1:8000/api/v1/movies/${movieId}/like/`,
        {},
        { headers: { Authorization: `Token ${token.value}` } }
      );
  
      const { is_liked, like_count } = likeResponse.data.likes_info;
      likeMovies.value[movieId] = { is_liked, like_count };
    } catch (error) {
      console.error("좋아요 상태 변경 중 오류 발생:", error.response?.data || error.message);
    }
  };

  const fetchUserLikes = async () => {
    if (!token.value) return

    try {
      const response = await axios.get(`${API_URL}/api/v1/movies/likes/`, {
        headers: { Authorization: `Token ${token.value}` },
      })

      response.data.forEach((like) => {
        const { movie_id, like_count, is_liked } = like
        likeMovies.value[movie_id] = {
          like_count: likeMovies.value[movie_id]?.like_count || like_count,
          is_liked: is_liked,
        }
      })
    } catch (error) {
      console.error("Error fetching user likes:", error)
    }
  }

  return {
    articles,
    API_URL,
    getArticles,
    signUp,
    logIn,
    username,
    token,
    isLogin,
    logOut,
    toggleMovieLike,
    likeMovies,
    fetchUserLikes,
  }
},
{ persist: true }
)