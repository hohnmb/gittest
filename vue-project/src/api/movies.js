import axios from "axios";

export const fetchMovies = async () => {
  const apiKey = process.env.VUE_APP_TMDB_API_KEY;
  const apiUrl = process.env.VUE_APP_API_URL;

  try {
    const response = await axios.get(`${apiUrl}/movie/now_playing`, {
      params: {
        api_key: apiKey,
        language: "ko-KR", // 한국어 데이터 요청
        page: 1,
      },
    });
    return response.data.results; // 영화 데이터 반환
  } catch (error) {
    console.error("영화 데이터를 불러오는 중 오류 발생:", error);
    return [];
  }
};