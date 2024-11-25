// stores/userPreferences.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";

// stores/userPreferences.js
export const useUserPreferencesStore = defineStore(
  "userPreferences",
  () => {
    const selectedRegion = ref(null);
    const selectedGenres = ref([]);

    // 선호도가 설정되어 있는지 확인하는 computed 속성
    const hasPreferences = computed(() => {
      return (
        selectedRegion.value !== null &&
        selectedRegion.value !== undefined &&
        Array.isArray(selectedGenres.value) &&
        selectedGenres.value.length > 0
      );
    });

    // 선호도 저장
    const savePreferences = (region, genres) => {
      selectedRegion.value = region;
      selectedGenres.value = genres;
    };

    // 선호도 초기화
    const clearPreferences = () => {
      selectedRegion.value = null;
      selectedGenres.value = [];
    };

    return {
      selectedRegion,
      selectedGenres,
      hasPreferences,
      savePreferences,
      clearPreferences,
    };
  },
  { persist: true }
); // persist 옵션으로 브라우저 새로고침해도 데이터 유지
