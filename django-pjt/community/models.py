# Create your models here.
from django.db import models
from django.conf import settings


# Create your models here.
class Post(models.Model): # 커뮤니티 글쓰기 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    upload_files = models.FileField(null=True, blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name = 'liked_post', blank=True )
    def __str__(self):
        return self.title  # 제목을 반환하여 관리자 페이지에서 제목을 표시하도록 함

class Comment(models.Model): # 커뮤니티 댓글 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.content
    
    