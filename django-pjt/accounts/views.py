from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer
from django.shortcuts import get_object_or_404, get_list_or_404

from django.contrib.auth import get_user_model

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
@api_view(['GET'])
def user_profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    profile = user.profile
    serializer = ProfileSerializer(profile, context={'request': request})
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_detail(request):
    profile = request.user.profile
    
    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, username):
    User = get_user_model()
    user_to_follow = get_object_or_404(User, username=username)
    
    if request.user == user_to_follow:
        return Response({'error': '자신을 팔로우할 수 없습니다.'}, status=400)
    else:
        my_profile = request.user.profile
        user_to_follow_profile = user_to_follow.profile
        
        if my_profile in user_to_follow_profile.followers.all():
            user_to_follow_profile.followers.remove(my_profile)
            is_following = False
        else:
            user_to_follow_profile.followers.add(my_profile)  # remove를 add로 수정
            is_following = True
        
        return Response({
            'is_following': is_following,
            'followers_count': user_to_follow_profile.followers.count()
        })
        
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    profile = request.user.profile
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)