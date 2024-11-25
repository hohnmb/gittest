from django.core.management.base import BaseCommand
import requests
import json
import os
from dotenv import load_dotenv

class Command(BaseCommand):
    help = 'TMDB API에서 해외 영화 데이터를 가져와 fixtures로 저장합니다.'

    def handle(self, *args, **options):
        load_dotenv()
        TMDB_API_KEY = os.getenv('TMDB_API_KEY')
        total_data = []
        print(TMDB_API_KEY)
        # 한국어가 아닌 영화 중 평점 높은 순으로 필터링
        for i in range(1, 16):  # 20개씩 15페이지 = 약 300개
            request_url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=ko-KR&sort_by=vote_average.desc&page={i}&vote_count.gte=500&without_original_language=ko"
            movies = requests.get(request_url).json()
            print(movies)
            for movie in movies['results']:
                if movie.get('release_date', ''):
                    movie_detail_url = f"https://api.themoviedb.org/3/movie/{movie['id']}?api_key={TMDB_API_KEY}&language=ko-KR"
                    movie_detail = requests.get(movie_detail_url).json()
                    
                    # 한국 영화가 아닌 것을 확인
                    if movie['original_language'] != 'ko' and 'KR' not in [country['iso_3166_1'] for country in movie_detail.get('production_countries', [])]:
                        fields = {
                            'title': movie['title'],
                            'released_date': movie['release_date'],
                            'popularity': movie['popularity'],
                            'vote_avg': movie['vote_average'],
                            'overview': movie['overview'],
                            'poster_path': movie['poster_path'],
                            'genres': movie['genre_ids'],
                            'original_language': movie['original_language'],
                            'production_countries': [country['iso_3166_1'] for country in movie_detail.get('production_countries', [])]
                        }
                        
                        data = {
                            "model": "movies.movie",
                            "pk": movie['id'],
                            "fields": fields
                        }
                        total_data.append(data)
                        
                        self.stdout.write(f"해외 영화 '{movie['title']}' (평점: {movie['vote_average']}, 언어: {movie['original_language']}) 데이터 추가 완료")
        
        with open("movies/fixtures/not_korean_movie_data.json", "w", encoding="utf-8") as w:
            json.dump(total_data, w, indent="\t", ensure_ascii=False)
            
        self.stdout.write(self.style.SUCCESS(f'총 {len(total_data)}개의 해외 영화 데이터 저장이 완료되었습니다.'))