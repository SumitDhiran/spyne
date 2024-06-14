from django.shortcuts import render
from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response
from user.serializers import UserSerializer, UserUpdateSerializer, GenericFollowSerializer
from user.models import CustomUser, Follow
from django.db.models import Q
from user.permissions import UserPermission
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
# Create your views here.


class UserViewset(viewsets.ModelViewSet) :
    """
    User
    """
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'create':
            self.serializer_class = UserSerializer
        elif self.action == 'update' or self.action=='partial_update':
            self.serializer_class = UserUpdateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'create':
            self.permission_classes = (permissions.AllowAny,)
        else:
            self.permission_classes = (permissions.IsAuthenticated, UserPermission,)
        return super(self.__class__, self).get_permissions()
    
    
    queryset = CustomUser.objects.all()
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='name', description='search user by name', type=str),
    ]
)
class SearchViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny,]

    def get_queryset(self):
        search_key = self.request.GET.get("name","")
        return CustomUser.objects.filter(name__icontains=search_key)
    

class FollowViewset(viewsets.GenericViewSet, 
                    mixins.CreateModelMixin, 
                    mixins.ListModelMixin, 
                ):
    serializer_class = GenericFollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Follow.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = Follow.objects.filter(follower=request.user, follows=serializer.validated_data.get("follows")).first()
        if instance:
            instance.delete()
            return Response({"message": "successfully unfollowed"}, status=status.HTTP_200_OK)
        else:
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "successfully followed"}, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)
        return super().perform_create(serializer)
    

    @action(detail=False, methods=['GET'])
    def followers(self, request):
        queyset = self.get_queryset().filter(follows=request.user)
        serializer = GenericFollowSerializer(queyset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'])
    def follows(self, request):
        queyset = self.get_queryset().filter(follower=request.user)
        serializer = GenericFollowSerializer(queyset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    


    
    