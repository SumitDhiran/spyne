from django.contrib import admin
from post.models import Post, PostLike, Comment, CommentLike, HashTag
# Register your models here.
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(HashTag)