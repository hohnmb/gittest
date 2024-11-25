# Vue에서 전달한 데이터를 Django 모델에 맞게 변환할 수 있도록 직렬화.


from rest_framework import serializers
from .models import Post, Comment




# # community POST# 게시글 상세 조회용 Serializer
# class PostSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user.username', read_only=True)
#     class CommentDetailSerializer(serializers.ModelSerializer):
#           # 댓글 작성자 이름 추가
        
#         class Meta:
#             model = Comment
#             fields = ('id', 'content', 'user', 'username', 'created_at', 'updated_at', )
#             read_only_fields = ('user',)

#     comment_set = CommentDetailSerializer(many=True, read_only=True)
#     comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)
#     username = serializers.CharField(source='user.username', read_only=True)  # 게시글 작성자 이름 추가
    
#     class Meta:
#         model = Post
#         fields = ('id', 'title', 'content', 'created_at', 'updated_at', 
#                  'user', 'username', 'comment_set', 'comment_count', 
#                  'upload_files', 'like_users')
#         read_only_fields = ('user', )
# community GET 
class PostListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta : 
        model = Post
        fields = ['id', 'user', 'username','title', 'content', 'created_at', 'updated_at','like_users',]
        


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    post_id = serializers.IntegerField(source='post.id', write_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'user', 'created_at', 'updated_at', 'post_id')
        read_only_fields = ('user', 'created_at', 'updated_at')

# class CommentSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user.username', read_only=True)
#     # 댓글 조회 시 게시글 출력 내역 변경
#     # class PostTitleSerializer(serializers.ModelSerializer):
#     #     class Meta:
#     #         model = Post
#     #         fields=('title',)
#     class Meta:
#         model = Comment
#         fields = ('id', 'content', 'user', 'username', 'created_at', 'updated_at', 'post')
#         read_only_fields = ('user', 'post')

class PostdSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'username', 'comment_set', 'comment_count')
        read_only_fields = ('user', )

class PostSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(id=request.user.id).exists()
        return False
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'username', 'comment_set', 'comment_count','like_count', 'is_liked')
        read_only_fields = ('user', )