from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    nickname = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=500, blank=True)  # 한줄소개
    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True
    )
    followings = models.ManyToManyField(
    'self', 
    symmetrical=False, 
    related_name='followers'
)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()