from django.core.management.base import BaseCommand
import requests
import json
import os
from dotenv import load_dotenv
# from dotenv import load_dotenv
class Command(BaseCommand):
    help = 'TMDB API에서 평점 높은 한국 영화 데이터를 가져와 fixtures로 저장합니다.'

    def handle(self, *args, **options):
        load_dotenv()
        # load_dotenv()
        TMDB_API_KEY = os.getenv('TMDB_API_KEY')
        total_data = []
        
        # vote_average.desc로 정렬하고 최소 투표 수를 설정하여 신뢰도 높은 평점 필터링
        for i in range(1, 6):  # 20개씩 5페이지 = 약 100개
            request_url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=ko-KR&sort_by=vote_average.desc&page={i}&with_original_language=ko&vote_count.gte=100"
            movies = requests.get(request_url).json()
            
            for movie in movies['results']:
                if movie.get('release_date', ''):
                    movie_detail_url = f"https://api.themoviedb.org/3/movie/{movie['id']}?api_key={TMDB_API_KEY}&language=ko-KR"
                    movie_detail = requests.get(movie_detail_url).json()
                    
                    if movie['original_language'] == 'ko' or 'KR' in [country['iso_3166_1'] for country in movie_detail.get('production_countries', [])]:
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
                        
                        self.stdout.write(f"한국 영화 '{movie['title']}' (평점: {movie['vote_average']}) 데이터 추가 완료")
        
        with open("movies/fixtures/korean_movie_data.json", "w", encoding="utf-8") as w:
            json.dump(total_data, w, indent="\t", ensure_ascii=False)
            
        self.stdout.write(self.style.SUCCESS(f'총 {len(total_data)}개의 한국 영화 데이터 저장이 완료되었습니다.'))