from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Q
from .models import Movie, Genre, MovieReview, MovieLike
from .serializers import MovieSerializer, GenreSerializer, MovieReviewSerializer,MovieDetailSerializer
from .models import UserPreference
from .serializers import MyPageReviewSerializer,UserPreferenceSerializer,LikedMovieSerializer
from django.contrib.auth import get_user_model
import requests
import os

from dotenv import load_dotenv
load_dotenv(verbose=True)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def movie_list(request):
    """영화 목록 조회 및 필터링"""
    movies = Movie.objects.all()
    
    # 국내/해외 영화 필터링
    is_korean = request.query_params.get('is_korean')
    if is_korean is not None:
        is_korean = is_korean.lower() == 'true'
        if is_korean:
            movies = movies.filter(
                Q(original_language='ko') | 
                Q(production_countries__contains='KR')
            )
        else:
            movies = movies.exclude(
                Q(original_language='ko') | 
                Q(production_countries__contains='KR')
            )
    
    # 장르 필터링
    genre_id = request.query_params.get('genre')
    if genre_id:
        movies = movies.filter(genres=genre_id)
    
    # 정렬
    sort_by = request.query_params.get('sort')
    order = request.query_params.get('order', 'desc')
    if sort_by:
        order_prefix = '-' if order == 'desc' else ''
        movies = movies.order_by(f'{order_prefix}{sort_by}')
    
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def movie_like(request, movie_pk):
    """영화 좋아요 토글"""
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user
    
    if movie.likes.filter(user=user).exists():
        movie.likes.filter(user=user).delete()
        is_liked = False
    else:
        MovieLike.objects.create(user=user, movie=movie)
        is_liked = True
    
    # MovieDetailSerializer의 형식과 동일하게 응답
    context = {
        'likes_info': {
            'like_count': movie.likes.count(),
            'is_liked': is_liked
        }
    }
    
    return Response(context)

@api_view(['GET'])
def movie_detail(request, movie_pk):
    """영화 상세 정보"""
    try:
        movie = Movie.objects.get(pk=movie_pk)
    except Movie.DoesNotExist:
        return Response({"error": "영화를 찾을 수 없습니다."}, status=404)

    user = request.user
    is_liked = movie.likes.filter(user=user).exists() if user.is_authenticated else False
    like_count = movie.likes.count()

    serializer = MovieDetailSerializer(movie, context={"request": request})
    return Response({
        **serializer.data,
        "likes_info": {
            "like_count": like_count,
            "is_liked": is_liked,
        }
    })


@api_view(['GET'])
def movie_main(request):
    """메인 페이지 데이터"""
    latest = Movie.objects.order_by('-released_date')[:10]
    popular = Movie.objects.order_by('-vote_avg')[:10]
    
    data = {
        'latest': MovieSerializer(latest, many=True).data,
        'popular': MovieSerializer(popular, many=True).data,
    }
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_like(request, movie_pk):
    """TMDB 영화 및 기존 영화에 대한 좋아요 토글"""
    try:
        # 영화가 백엔드 DB에 없는 경우 TMDB API에서 가져와 저장
        movie = Movie.objects.get(pk=movie_pk)
    except Movie.DoesNotExist:
        # TMDB API에서 영화를 가져와 저장
        save_tmdb_movie(request, tmdb_movie_id=movie_pk)  # 위에서 정의한 save_tmdb_movie 호출
        movie = get_object_or_404(Movie, pk=movie_pk)

    user = request.user
    
    # 좋아요 상태 토글
    like_instance = MovieLike.objects.filter(user=user, movie=movie)
    
    if like_instance.exists():
        like_instance.delete()
        is_liked = False
    else:
        MovieLike.objects.create(user=user, movie=movie)
        is_liked = True
    
    # 좋아요 수 계산 및 응답 반환
    like_count = MovieLike.objects.filter(movie=movie).count()
    
    context = {
        'likes_info': {
            'like_count': like_count,
            'is_liked': is_liked
        }
    }
    return Response(context)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_movies(request):
    """사용자가 좋아요한 영화 목록 조회"""
    liked_movies = Movie.objects.filter(
        likes__user=request.user
    ).prefetch_related(
        'genres'  # ManyToMany 관계는 prefetch_related 사용
    ).order_by('-likes__created_at')
    
    serializer = LikedMovieSerializer(
        liked_movies, 
        many=True,
        context={'request': request}
    )
    return Response(serializer.data)
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def movie_like(request, movie_pk):
#     """영화 좋아요/취소"""
#     movie = get_object_or_404(Movie, pk=movie_pk)
#     if request.user in movie.like_users.all():
#         movie.like_users.remove(request.user)
#         return Response({'status': 'unliked'})
#     movie.like_users.add(request.user)
#     return Response({'status': 'liked'})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def review_list(request, movie_pk):
    """리뷰 목록 조회 및 작성"""
    movie = get_object_or_404(Movie, pk=movie_pk)
    
    if request.method == 'GET':
        reviews = MovieReview.objects.filter(movie=movie)
        serializer = MovieReviewSerializer(
            reviews, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if MovieReview.objects.filter(user=request.user, movie=movie).exists():
            return Response(
                {'error': '이미 리뷰를 작성했습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = MovieReviewSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def review_detail(request, review_pk):
    """리뷰 수정 및 삭제"""
    review = get_object_or_404(MovieReview, pk=review_pk)
    
    if request.user != review.user:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'PUT':
        serializer = MovieReviewSerializer(
            review, 
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_like(request, review_pk):
    review = get_object_or_404(MovieReview, pk=review_pk)
    user = request.user
    
    if review.like_users.filter(id=user.id).exists():
        review.like_users.remove(user)
        is_liked = False
    else:
        review.like_users.add(user)
        is_liked = True
    
    return Response({
        'is_liked': is_liked,
        'like_count': review.like_users.count()
    })

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_preferences(request):
    """사용자 선호도 조회 및 저장"""
    try:
        preference = UserPreference.objects.get(user=request.user)
    except UserPreference.DoesNotExist:
        preference = None

    if request.method == 'GET':
        if preference:
            serializer = UserPreferenceSerializer(preference)
            return Response(serializer.data)
        return Response({})

    elif request.method == 'POST':
        if preference:
            serializer = UserPreferenceSerializer(preference, data=request.data, partial=True)
        else:
            serializer = UserPreferenceSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_preferences(request):
    """사용자 선호도 초기화"""
    try:
        preference = UserPreference.objects.get(user=request.user)
        preference.selected_genres.clear()
        preference.selected_region = None
        preference.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except UserPreference.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
def review_create(request):
    pass

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def user_reviews(request):
#     reviews = MovieReview.objects.filter(user=request.user)
#     serializer = MovieReviewSerializer(reviews, many=True)
#     return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_reviews(request):
    reviews = MovieReview.objects.filter(user=request.user)
    serializer = MyPageReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def user_profile(request, username):
    """특정 사용자의 프로필 정보 조회"""
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    
    # 해당 유저의 리뷰, 좋아요한 영화, 선호도 정보 조회
    reviews = MovieReview.objects.filter(user=user)
    liked_movies = Movie.objects.filter(likes__user=user)
    preferences = UserPreference.objects.filter(user=user).first()
    
    data = {
        'username': user.username,
        'reviews': MyPageReviewSerializer(reviews, many=True).data,
        'liked_movies': LikedMovieSerializer(
            liked_movies, 
            many=True, 
            context={'request': request}
        ).data,
        'preferences': UserPreferenceSerializer(preferences).data if preferences else None,
    }
    
    return Response(data)


@api_view(['POST'])
def save_tmdb_movie(request, tmdb_movie_id):
    """TMDB API 데이터를 백엔드 DB에 저장"""
    api_key = os.getenv("TMDB_API_KEY")  # 환경 변수에서 API 키 로드

    if not api_key:
        return Response({"error": "TMDB_API_KEY 환경 변수가 설정되지 않았습니다."}, status=500)

    tmdb_url = f"https://api.themoviedb.org/3/movie/{tmdb_movie_id}"
    response = requests.get(tmdb_url, params={"api_key": api_key, "language": "ko-KR"})

    if response.status_code != 200:
        return Response({"error": f"TMDB API 호출 실패 (상태 코드: {response.status_code})"}, status=400)

    data = response.json()

    # 장르 처리
    genres = []
    for genre_data in data.get("genres", []):
        genre, created = Genre.objects.get_or_create(name=genre_data["name"])
        genres.append(genre)

    # 영화 저장
    movie, created = Movie.objects.get_or_create(
        id=data["id"],  # TMDB의 영화 ID를 사용
        defaults={
            "title": data["title"],
            "released_date": data.get("release_date"),
            "popularity": data.get("popularity"),
            "vote_avg": data.get("vote_average"),
            "overview": data.get("overview"),
            "poster_path": data.get("poster_path"),
            "original_language": data.get("original_language"),
            "production_countries": data.get("production_countries", []),
        },
    )

    if created:
        movie.genres.set(genres)  # Many-to-Many 관계 설정

    # 좋아요 상태 및 좋아요 수 계산
    user = request.user
    is_liked = movie.likes.filter(user=user).exists() if user.is_authenticated else False
    like_count = movie.likes.count()

    return Response({
        "message": "영화가 성공적으로 저장되었습니다.",
        "movie_id": movie.id,
        "likes_info": {
            "like_count": like_count,
            "is_liked": is_liked,
        }
    }, status=201)