from django.urls import path, include
from post.views import PostViewset, CommentViewset, PostLikeViewset, CommentLikeViewset, HashTagViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'post', PostViewset, basename="post")
router.register(r'comment', CommentViewset, basename="comment")
router.register(r'post-like', PostLikeViewset, basename="post_like")
router.register(r'comment-like', CommentLikeViewset, basename="comment_like")
router.register(r'hashtag', HashTagViewset, basename="hashtag")

app_name = 'post'

urlpatterns = [
    path('', include(router.urls)),
]