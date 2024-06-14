from django.db import models
from user.models import CustomUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(_("text"))
    image = models.ImageField(blank=True, null=True, upload_to = 'posts/', default = 'posts/default.png')
    hash_tag = models.ManyToManyField('HashTag')
    view_count = models.BigIntegerField(_("view count"), default=0)
    created = models.DateTimeField(auto_now_add= True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def total_likes(self):
        return int(self.postlike_set.all().count())


class HashTag(models.Model):
    name = models.CharField(max_length=200,)
    created = models.DateTimeField(auto_now_add= True)
    # id = models.UUIDField(default= uuid.uuid4,unique=True,primary_key= True,editable= False)

    def __str__(self):
        return self.name
    
    

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='post_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(_("text"))
    created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.text
    
    def total_likes(self):
        return int(self.commentlike_set.all().count())
    

class PostLike(models.Model):
    liked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add= True)

    class Meta:
        unique_together = [['liked_by','post']]

class CommentLike(models.Model):
    liked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add= True)

    class Meta:
        unique_together = [['liked_by','comment']]