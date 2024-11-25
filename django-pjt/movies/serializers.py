from rest_framework import serializers
from .models import Movie, MovieLike, Genre, MovieReview, UserPreference

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'released_date', 
            'popularity', 'vote_avg', 'overview', 
            'poster_path', 'genres', 'original_language',
            'production_countries']

# 리뷰 출력하는 것
class MovieReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    class Meta:
        model = MovieReview
        fields = [
            'id', 'user', 'movie', 'content',
            'rating', 'created_at', 'updated_at',
            'like_count', 'is_liked'
        ]
        read_only_fields = ('user', 'created_at', 'updated_at')

    def get_like_count(self, obj):
        return obj.like_users.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(id=request.user.id).exists()
        return False

class MovieLikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = MovieLike
        fields = ('id','username','created_at')
        read_only_fields = ('user','movie')

# 사용자 선호도 시리얼라이저 추가
class UserPreferenceSerializer(serializers.ModelSerializer):
    selected_genres = GenreSerializer(many=True, read_only=True)
    selected_genre_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = UserPreference
        fields = ['selected_region', 'selected_genres', 'selected_genre_ids']

    def create(self, validated_data):
        genre_ids = validated_data.pop('selected_genre_ids', [])
        preference = UserPreference.objects.create(**validated_data)
        if genre_ids:
            preference.selected_genres.set(genre_ids)
        return preference

    def update(self, instance, validated_data):
        genre_ids = validated_data.pop('selected_genre_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if genre_ids is not None:
            instance.selected_genres.set(genre_ids)
        instance.save()
        return instance
    
class MovieDetailSerializer(serializers.ModelSerializer):
    likes_info = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'released_date', 'popularity', 'vote_avg',
            'overview', 'poster_path', 'genres', 'original_language',
            'production_countries', 'likes_info'
        )

    def get_likes_info(self, obj):
        request = self.context.get('request')
        is_liked = False
        if request and request.user.is_authenticated:
            is_liked = obj.likes.filter(user=request.user).exists()
        
        return {
            'like_count': obj.likes.count(),
            'is_liked': is_liked
        }

class LikedMovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 
            'title', 
            'poster_path',
            'vote_avg',
            'genres',
            'like_count',
            'is_liked',
            'released_date'
        ]

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
class MyPageReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    movie_poster = serializers.CharField(source='movie.poster_path', read_only=True)
    movie_id = serializers.IntegerField(source='movie.id', read_only=True)

    class Meta:
        model = MovieReview
        fields = [
            'id', 'content', 'rating',
            'movie_id', 'movie_title', 'movie_poster','created_at', 'updated_at'
        ]