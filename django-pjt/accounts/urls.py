from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('users/<str:username>/follow/', views.follow_user, name='follow-user'),
    path('profile/update/', views.update_profile, name='profile-update'),
    ] 