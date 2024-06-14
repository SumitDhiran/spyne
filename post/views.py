from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from post.serializers import PostSerializer, CommentSerializer, PostLikeSerializer, CommentLikeSerializer, HashTagSerializer
from post.permissions import PostPermission, CommentPermission, PostLikePermission, CommentLikePermission
from post.models import Post, Comment, PostLike, CommentLike, HashTag
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
# Create your views here.


class PostViewset(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, PostPermission,)
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
    
    @action(detail=False, methods=['GET'], url_path="search/(?P<tag_id>[^/.]+)", url_name='search')
    def search(self, request, tag_id):
        queyset = self.get_queryset().filter(hash_tag__id=tag_id)
        serializer = PostSerializer(queyset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, CommentPermission,)
    # queryset = Comment.objects.all()

    def get_queryset(self):
        if self.action == "list":
            queryset = Comment.objects.filter(comment=None)
        else:
            queryset = Comment.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
    
    @action(detail=True, methods=['GET'])
    def replies(self, request, *args, **kwargs):
        comment_id = self.kwargs.get("pk")
        queyset = self.get_queryset().filter(comment_id=comment_id)
        serializer = CommentSerializer(queyset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class PostLikeViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    serializer_class = PostLikeSerializer
    permission_classes = (permissions.IsAuthenticated, PostLikePermission,)


    queryset = PostLike.objects.all()


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as e:
            raise ValidationError("UNIQUE constraint failed: post_postlike.liked_by_id, post_postlike.post_id")
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(liked_by=self.request.user)
        return super().perform_create(serializer)
    
    def destroy(self, request, *args, **kwargs):
        id = self.kwargs.get("pk")
        instance = self.queryset.filter(post__id=id)
        if not instance:
            raise ValidationError("you have already unliked the POST")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentLikeViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    serializer_class = CommentLikeSerializer
    permission_classes = (permissions.IsAuthenticated, CommentLikePermission,)

    queryset = CommentLike.objects.all()


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as e:
            raise ValidationError("UNIQUE constraint failed: post_commentlike.liked_by_id, post_commentlike.comment_id")
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(liked_by=self.request.user)
        return super().perform_create(serializer)
    
    def destroy(self, request, *args, **kwargs):
        id = self.kwargs.get("pk")
        instance = self.queryset.filter(comment__id=id)
        if not instance:
            raise ValidationError("you have already unliked the Comment")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)



class HashTagViewset(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = HashTagSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            self.permission_classes = (permissions.IsAdminUser,)
        else:
            self.permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

        return super(self.__class__, self).get_permissions()
    
    queryset = HashTag.objects.all()
    
