from django.contrib import admin
from .models import Post , Comment # Post 모델을 가져옵니다.

admin.site.register(Post) 
admin.site.register(Comment)  # 모델을 관리 페이지에 등록
