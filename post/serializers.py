from rest_framework import serializers
from post.models import Post, PostLike, Comment, CommentLike, HashTag


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'text', 'image', 'hash_tag', 'total_likes']
        read_only_fields = ('created','view_count', 'total_likes')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'comment', 'post', 'total_likes']
        read_only_fields = ('created', 'total_likes')

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['id','post']
        read_only_fields = ('created',)

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['id','comment']
        read_only_fields = ('created',)

class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = '__all__'
        read_only_fields = ('created',)