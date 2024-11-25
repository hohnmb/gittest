from rest_framework.decorators import api_view, permission_classes  
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment
from .serializers import PostSerializer,PostListSerializer, CommentSerializer

# Create your views here.
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])  # 로그인한 사용자만 접근 가능
def post_list(request):
    if request.method =='GET':
        posts = Post.objects.all()
        serializer = PostListSerializer(posts,many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    
@api_view(['GET','DELETE','PUT'])
def post_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            

@api_view(['GET'])
def comment_list(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments,many=True)
    return Response(serializer.data)

@api_view(['GET','DELETE','PUT'])
def comment_detail(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.method=='GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method=='PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 로그인한 사용자만 댓글 작성 가능
def comment_create(request, post_pk):
    post = Post.objects.get(pk=post_pk)

    # 댓글 내용만 받아오기
    serializer = CommentSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        # 댓글 작성자(user)는 현재 로그인한 사용자로 자동 설정
        serializer.save(user=request.user, post=post)

        # 댓글 작성 후 게시글 상세 조회 API 응답으로 댓글 리스트를 포함시키는 방식
        post_serializer = PostSerializer(post)
        return Response(post_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_article(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    
    if post.like_users.filter(id=request.user.id).exists():
        post.like_users.remove(request.user)
        liked = False
    else:
        post.like_users.add(request.user)
        liked = True
    
    return Response({'liked': liked, 'like_count': post.like_users.count()})