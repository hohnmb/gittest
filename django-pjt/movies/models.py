from django.db import models
from django.conf import settings

class Genre(models.Model):  # 장르
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    released_date = models.DateField()
    popularity = models.FloatField()
    vote_avg = models.FloatField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, blank=True)
    original_language = models.CharField(max_length=10)
    production_countries = models.JSONField(default=list)

    def is_korean(self):
        return self.original_language == "ko" or "KR" in self.production_countries

class MovieReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name = 'liked_reviews', blank=True )
    class Meta:
        unique_together = ("user", "movie")

    def __str__(self):
        return f"{self.user.username}'s review for {self.movie.title}"

# 사용자 선호도 모델 추가
class UserPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='preferences'
    )
    selected_region = models.CharField(max_length=20, null=True, blank=True)
    selected_genres = models.ManyToManyField(Genre, blank=True)

    def __str__(self):
        return f"{self.user.username}'s preferences"
    
    
class MovieLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='movie_likes'
    )
    movie = models.ForeignKey(
        'Movie',  
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} likes {self.movie.title}"
