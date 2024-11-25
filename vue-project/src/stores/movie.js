import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useCounterStore } from './counter'

export const useMovieStore = defineStore('movie', () => {
  const movies = ref([])
  const likedMovies = ref([]) 
  const router = useRouter()
  const counterStore = useCounterStore()
  const selectedRegion = ref(null)
  const selectedGenres = ref([])  // 빈 배열로 초기화
  const myReviews = ref([])

  const followUser = async (username) => {
    try {
      const response = await axios.post(
        `${counterStore.API_URL}/api/v1/users/${username}/follow/`,
        {},
        {
          headers: {
            Authorization: counterStore.token ? `Token ${counterStore.token}` : null
          }
        }
      )
      return response.data
    } catch (error) {
      console.error('팔로우 처리 실패:', error)
      return null
    }
  }
  
  const fetchUserProfile = async (username) => {
    try {
      const response = await axios.get(
        `${counterStore.API_URL}/api/v1/movies/users/${username}/profile/`,
        {
          headers: {
            Authorization: counterStore.token ? `Token ${counterStore.token}` : null
          }
        }
      )
      // 프로필 데이터 저장
      selectedGenres.value = response.data.preferences?.selected_genres || []
      likedMovies.value = response.data.liked_movies
      myReviews.value = response.data.reviews
      return response.data
    } catch (error) {
      console.error('프로필 정보 로딩 실패:', error)
      return null
    }
  }
  
  const fetchMyReviews = async () => {
    try {
      const response = await axios.get(
        'http://127.0.0.1:8000/api/v1/movies/reviews/user/',
        {
          headers: {
            Authorization: `Token ${counterStore.token}`
          }
        }
      )
      myReviews.value = response.data
    } catch (error) {
      console.error('내 리뷰 가져오기 실패:', error)
      myReviews.value = []
    }
  }
  
  const fetchMovies = () => {
    axios.get('http://127.0.0.1:8000/api/v1/movies/')
      .then(response => {
        movies.value = response.data
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  const saveUserPreferences = async () => {
    try {
        const data = {
            selected_region: selectedRegion.value,
            selected_genre_ids: selectedGenres.value.map(genre => genre.id)
        };
        console.log('Sending data:', data);
        console.log('selected_genre_ids : ' , selectedGenres.value.map(genre => genre.id))
        
        await axios.post('http://127.0.0.1:8000/api/v1/movies/users/preferences/', 
            data,
            {
                headers: {
                    Authorization: `Token ${counterStore.token}`
                }
            }
        );
    } catch (error) {
        console.error('선호도 저장 실패:', error.response?.data || error);
    }
  }
// 좋아요한 영화 목록 가져오기 함수 추가
const fetchLikedMovies = async () => {
  try {
    const response = await axios.get(
      'http://127.0.0.1:8000/api/v1/movies/likes/',
      {
        headers: {
          Authorization: `Token ${counterStore.token}`
        }
      }
    )
    likedMovies.value = response.data
  } catch (error) {
    console.error('좋아요한 영화 목록 가져오기 실패:', error)
    likedMovies.value = []
  }
}
  const loadUserPreferences = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/v1/movies/users/preferences/', {
        headers: {
          Authorization: `Token ${counterStore.token}`
        }
      })
      const preferences = response.data
      selectedRegion.value = preferences.selected_region
      selectedGenres.value = preferences.selected_genres || []  // 기본값 추가
    } catch (error) {
      console.error('선호도 불러오기 실패:', error)
      selectedRegion.value = null
      selectedGenres.value = []  // 에러 시 빈 배열로 초기화
    }
  }

  const setSelectedRegion = (region) => {
    selectedRegion.value = region
    saveUserPreferences()
  }

  const setSelectedGenre = (genreId) => {
    console.log(genreId)
    const index = selectedGenres.value.findIndex((genre) => genre.id === genreId)
    console.log(index)
    if (index === -1) {
      selectedGenres.value.push({id: genreId})
    } else {
      selectedGenres.value.splice(index, 1)
    }
    saveUserPreferences()
  }

  const clearSelections = () => {
    selectedRegion.value = null
    selectedGenres.value = []
  }

  const filteredMovies = computed(() => {
    if (!selectedRegion.value || !selectedGenres.value.length) {
      return movies.value
    }

    return movies.value.filter(movie => {
      const regionMatch = selectedRegion.value === 'domestic'
        ? (movie.original_language === 'ko' && movie.production_countries.includes('KR'))
        : !(movie.original_language === 'ko' && movie.production_countries.includes('KR'))
      
      const genreMatch = selectedGenres.value.length === 0 || 
        movie.genres.some(movieGenre => 
          selectedGenres.value.some(selectedGenre => selectedGenre.id === movieGenre.id)
        )
      
      return regionMatch && genreMatch
    })
  })

  return {
    movies,
    selectedRegion,
    selectedGenres,
    filteredMovies,
    fetchMovies,
    setSelectedRegion,
    setSelectedGenre,
    loadUserPreferences,
    clearSelections,
    likedMovies,
    fetchLikedMovies,
    fetchMyReviews,
    myReviews,
    fetchUserProfile,
    followUser,

  }
})