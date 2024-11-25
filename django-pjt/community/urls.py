from django.urls import path
from . import views
urlpatterns = [
   path('', views.post_list),
   path('<int:post_pk>/', views.post_detail),
   path('<int:post_pk>/like/', views.like_article),
   path('<int:post_pk>/comments/', views.comment_create),
   path('comments/', views.comment_list),
   path('comments/<int:comment_pk>/', views.comment_detail),
]
#const response = await axios.post(
      #`${store.API_URL}/api/v1/community/${route.params.id}/like/`,
     # {},
# comments/ 댓글 아하 
#     url: `${store.API_URL}/api/v1/community/`,
#  path('api/v1/community/', include('community.urls')),