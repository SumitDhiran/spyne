from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from user.managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    name = models.CharField(_("full name"), max_length=25)
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(_("phone number"), unique=True, max_length=10)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.name +" | "+ self.email


class Follow(models.Model):
    follower = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='follower')
    follows = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='follows')
    created = models.DateTimeField(auto_now_add= True)

    class Meta:
        unique_together = [['follower','follows']]