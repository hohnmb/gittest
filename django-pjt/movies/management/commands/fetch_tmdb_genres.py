import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
def fetch_tmdb_genres():
    """
    TMDB API에서 영화 장르 정보를 가져와서 Django fixture 형식의 JSON으로 변환
    """

    load_dotenv()
    # TMDB API 설정
    TMDB_API_KEY='eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxOGQ1YjJmNWJmYTkyMTlkN2NkZjY4NzYwM2JkYjlhNCIsIm5iZiI6MTczMjA5MjkzNy43ODA5NjM0LCJzdWIiOiI2NzM2YjQ3YjcxZWY2Njk3OGNmYWZhMWIiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.EYavodAll94WNjskua5l0U9nhkctyhIiGXfUBwGyhtU'
    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY 환경변수가 설정되지 않았습니다.")
    
    # TMDB API 엔드포인트
    url = "https://api.themoviedb.org/3/genre/movie/list"
    
    # API 요청 헤더
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}"
    }
    
    try:
        # API 요청
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 에러 체크
        
        # JSON 응답 파싱
        data = response.json()
        genres = data.get('genres', [])
        
        # Django fixture 형식으로 변환
        fixture_data = []
        for genre in genres:
            fixture_data.append({
                "model": "movies.genre",  # 앱이름.모델이름
                "pk": genre['id'],
                "fields": {
                    "name": genre['name']
                }
            })
        
        # 현재 날짜로 파일명 생성
        current_date = datetime.now().strftime('%Y%m%d')
        filename = f'genre_fixture_{current_date}.json'
        
        # JSON 파일 생성
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(fixture_data, f, ensure_ascii=False, indent=2)
        
        print(f"장르 데이터가 {filename}에 성공적으로 저장되었습니다.")
        return filename
        
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 에러 발생: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 중 에러 발생: {e}")
        return None
    except Exception as e:
        print(f"예상치 못한 에러 발생: {e}")
        return None

if __name__ == "__main__":
    fetch_tmdb_genres()