from django.contrib import admin
from user.models import CustomUser, Follow

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Follow)
