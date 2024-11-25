<template>
  <div>
    <div v-if="pageUser" class="user-content">
      <h1>
        <template v-if="isOwnProfile"> 안녕하세요, {{ pageUser }}님! </template>
        <template v-else> {{ pageUser }}님의 페이지입니다 </template>
      </h1>

      <!-- 프로필 섹션 -->
      <div class="profile-section">
        <div class="profile-header">
          <div class="profile-image">
            <img
              :src="getProfileImageUrl"
              :alt="`${pageUser}의 프로필 이미지`"
            />
            <div v-if="isOwnProfile" class="image-edit-overlay">
              <label for="imageInput" class="edit-image-btn">
                <i class="fas fa-camera"></i>
                이미지 변경
              </label>
              <input
                id="imageInput"
                type="file"
                accept="image/*"
                @change="handleImageChange"
                class="hidden"
              />
            </div>
          </div>

          <div class="profile-info">
            <div v-if="isEditing && isOwnProfile" class="bio-edit">
              <textarea
                v-model="editBio"
                class="bio-textarea"
                placeholder="자기소개를 입력하세요"
              ></textarea>
              <div class="bio-buttons">
                <button @click="saveBio" class="save-button">저장</button>
                <button @click="cancelEdit" class="cancel-button">취소</button>
              </div>
            </div>
            <div v-else class="bio">
              {{ profile?.bio || "자기소개가 없습니다." }}
              <button
                v-if="isOwnProfile"
                @click="startEdit"
                class="edit-button"
              >
                수정
              </button>
            </div>
            <div class="follow-stats">
              <span>팔로워: {{ profile?.followers_count || 0 }}</span>
              <span>팔로잉: {{ profile?.following_count || 0 }}</span>
            </div>
            <button
              v-if="!isOwnProfile"
              @click="handleFollow"
              :class="{ following: isFollowing }"
              class="follow-button"
            >
              {{ isFollowing ? "팔로잉" : "팔로우" }}
            </button>
          </div>
        </div>
      </div>

      <!-- 선호 장르 섹션 -->
      <div class="preferred-genres">
        <h2>선호하는 장르</h2>
        <div class="genre-tags">
          <span
            v-for="genre in movieStore.selectedGenres"
            :key="genre.id"
            class="genre-tag"
          >
            {{ getGenreName(genre.id) }}
          </span>
        </div>
      </div>

      <!-- 좋아요한 영화 섹션 -->
      <div class="liked-movies-section">
        <h2>좋아요한 영화</h2>
        <div class="movie-grid" v-if="movieStore.likedMovies?.length">
          <MovieCard
            v-for="movie in movieStore.likedMovies"
            :key="movie.id"
            :movie="movie"
            :showLikeButton="false"
          />
        </div>
        <p v-else class="no-movies">아직 좋아요한 영화가 없습니다.</p>
      </div>

      <!-- 작성한 리뷰 섹션 -->
      <div class="liked-movies-section">
        <h2>
          {{
            isOwnProfile ? "내가 작성한 리뷰" : `${pageUser}님이 작성한 리뷰`
          }}
          ({{ movieStore.myReviews?.length || 0 }})
        </h2>
        <div class="reviews-grid">
          <MyReviewCard
            v-for="review in movieStore.myReviews"
            :key="review.id"
            :review="review"
          />
        </div>
      </div>
    </div>

    <div v-else>
      <p class="login-prompt">사용자를 찾을 수 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import MyReviewCard from "@/components/MyReviewCard.vue";
import { storeToRefs } from "pinia";
import { useCounterStore } from "@/stores/counter";
import { useMovieStore } from "@/stores/movie";
import { onMounted, ref, computed } from "vue";
import { useRoute } from "vue-router";
import MovieCard from "@/components/MovieCard.vue";

const route = useRoute();
const store = useCounterStore();
const movieStore = useMovieStore();
const { username } = storeToRefs(store);

const profile = ref(null);
const isFollowing = ref(false);

const isEditing = ref(false);
const editBio = ref("");
const loadUserData = async () => {
  if (pageUser.value) {
    const userData = await movieStore.fetchUserProfile(pageUser.value);
    if (userData?.profile) {
      profile.value = {
        ...userData.profile,
        profile_image: `${store.API_URL}${userData.profile.profile_image}`,
      };
    }
    isFollowing.value = userData?.is_following || false;
  }
};
const startEdit = () => {
  editBio.value = profile.value?.bio || "";
  isEditing.value = true;
};

const cancelEdit = () => {
  isEditing.value = false;
  editBio.value = "";
};

const getProfileImageUrl = computed(() => {
  if (profile.value?.profile_image) {
    // 이미 전체 URL이 포함되어 있는지 확인
    if (profile.value.profile_image.startsWith("http")) {
      return profile.value.profile_image;
    }
    return `${store.API_URL}${profile.value.profile_image}`;
  }
  return "/default-profile.jpg";
});

const handleImageChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("profile_image", file);

  try {
    const response = await axios.put(
      `${store.API_URL}/api/v1/accounts/profile/update/`,
      formData,
      {
        headers: {
          Authorization: `Token ${store.token}`,
          "Content-Type": "multipart/form-data",
        },
      }
    );

    // 프로필 정보 업데이트 및 이미지 경로 저장
    profile.value = {
      ...profile.value,
      profile_image: `${store.API_URL}${response.data.profile_image}`,
    };

    // 프로필 정보 새로고침
    await loadUserData();
  } catch (error) {
    console.error("이미지 업로드 실패:", error);
  }
};

const saveBio = async () => {
  try {
    const response = await axios.put(
      `${store.API_URL}/api/v1/accounts/profile/update/`,
      { bio: editBio.value },
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    profile.value = {
      ...profile.value,
      bio: response.data.bio,
    };
    isEditing.value = false;
  } catch (error) {
    console.error("자기소개 수정 실패:", error);
  }
};

// 현재 페이지의 사용자 정보
const pageUser = computed(() => route.params.username || username.value);
const isOwnProfile = computed(() => pageUser.value === username.value);

const handleFollow = async () => {
  try {
    const response = await axios.post(
      `${store.API_URL}/api/v1/accounts/users/${pageUser.value}/follow/`,
      {},
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    isFollowing.value = response.data.is_following;

    // 프로필 정보 업데이트
    profile.value = {
      ...profile.value,
      followers_count: response.data.followers_count,
      following_count: profile.value?.following_count || 0, // 기존 following_count 유지
    };
  } catch (error) {
    console.error("팔로우 처리 실패:", error);
  }
};

const getGenreName = (genreId) => {
  const genres = {
    28: "액션",
    12: "모험",
    16: "애니메이션",
    35: "코미디",
    80: "범죄",
    99: "다큐멘터리",
    18: "드라마",
    10751: "가족",
    14: "판타지",
    36: "역사",
    27: "공포",
    10402: "음악",
    9648: "미스터리",
    10749: "로맨스",
    878: "SF",
    10770: "TV 영화",
    53: "스릴러",
    10752: "전쟁",
    37: "서부",
  };
  return genres[genreId] || "";
};
onMounted(() => {
  loadUserData();
});
</script>

<style scoped>
.user-content {
  margin: 30px auto;
  max-width: 900px;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
}

.profile-section {
  margin-bottom: 30px;
}

.profile-header {
  display: flex;
  gap: 20px;
  align-items: center;
}

.profile-image img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}

.profile-info {
  flex: 1;
}

.bio {
  margin-bottom: 10px;
  color: #666;
}

.follow-stats {
  display: flex;
  gap: 20px;
  margin: 10px 0;
  color: #444;
}

.follow-button {
  padding: 8px 16px;
  border-radius: 20px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.follow-button.following {
  background-color: #6c757d;
}

.follow-button:hover {
  opacity: 0.9;
}

/* 기존 스타일 유지 */
h1 {
  color: #333;
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 20px;
}

.preferred-genres {
  margin-top: 30px;
  padding: 20px;
  background-color: #f7f7f7;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.genre-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.genre-tag {
  padding: 8px 18px;
  font-size: 1rem;
  color: #fff;
  background-color: #007bff;
  border-radius: 20px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.genre-tag:hover {
  background-color: #0056b3;
  transform: translateY(-3px);
}

.liked-movies-section {
  margin-top: 40px;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
  padding-top: 15px;
}

.reviews-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding-top: 15px;
}

.no-movies {
  text-align: center;
  color: #999;
  font-size: 1rem;
  margin-top: 20px;
}

.login-prompt {
  font-size: 1.2rem;
  color: #666;
  text-align: center;
  margin-top: 30px;
  font-weight: 500;
}

.bio-edit {
  margin-bottom: 10px;
}

.bio-textarea {
  width: 100%;
  min-height: 80px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 8px;
  resize: vertical;
}

.bio-buttons {
  display: flex;
  gap: 8px;
}

.save-button,
.cancel-button {
  padding: 6px 12px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.save-button {
  background-color: #28a745;
  color: white;
}

.cancel-button {
  background-color: #dc3545;
  color: white;
}

.edit-button {
  margin-left: 8px;
  padding: 4px 8px;
  border: none;
  background-color: #6c757d;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.profile-image {
  position: relative;
  width: 100px;
  height: 100px;
}

.image-edit-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.6);
  padding: 5px;
  text-align: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.profile-image:hover .image-edit-overlay {
  opacity: 1;
}

.edit-image-btn {
  color: white;
  cursor: pointer;
  font-size: 0.8rem;
}

.hidden {
  display: none;
}
</style>
