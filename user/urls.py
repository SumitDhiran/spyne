from django.urls import path, include
from user.views import UserViewset, SearchViewset, FollowViewset
from rest_framework.routers import DefaultRouter


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE4Mzk2NDIzLCJpYXQiOjE3MTgzNzQ4MjMsImp0aSI6IjBkNzYwOWYyZTQzNzRlYTY5ZGFkYzc2MDdkMGZkOWZiIiwidXNlcl9pZCI6N30.CKEKJvkI6NWuuaDuoF4BBPLCOTuiTVlREkzHXyV2WIc
router = DefaultRouter()
router.register(r'user', UserViewset, basename="user")
router.register(r'search', SearchViewset, basename="search")
router.register(r'follow', FollowViewset, basename="follow")

app_name = 'user'
urlpatterns = [
    path('', include(router.urls)),
]