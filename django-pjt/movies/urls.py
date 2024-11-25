# movies/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 영화 관련 URL
    path('', views.movie_list, name='movie-list'),  # 영화 목록
    path('<int:movie_pk>/', views.movie_detail, name='movie-detail'),  # 영화 상세 정보
    path('main/', views.movie_main, name='movie-main'),
    path('<int:movie_pk>/like/', views.movie_like, name='movie-like'),  # 좋아요 누르기
    path('likes/', views.liked_movies, name='liked-movies'),  # 좋아요 누른 영화들 가져오기

    # TMDB 관련 URL 추가
    path('<int:tmdb_movie_id>/save/', views.save_tmdb_movie, name='save-tmdb-movie'),  # TMDB 영화 저장

    # 리뷰 관련 URL
    path('<int:movie_pk>/reviews/', views.review_list, name='review-list'),  # 리뷰 목록, 리뷰 작성
    path('reviews/<int:review_pk>/', views.review_detail, name='review-detail'),  # 리뷰 수정, 삭제
    path('reviews/<int:review_pk>/like/', views.review_like, name='review-like'),  # 리뷰 좋아요
    path('reviews/user/', views.user_reviews, name='user-reviews'),

    # 사용자 선호도 관련 URL 추가
    path('users/preferences/', views.user_preferences, name='user-preferences'),
    path('users/preferences/clear/', views.clear_preferences, name='clear-preferences'),

    # 유저 페이지 
    path('users/<str:username>/profile/', views.user_profile, name='user-profile'),
]