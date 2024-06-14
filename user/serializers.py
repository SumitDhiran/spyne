from rest_framework import serializers
from user.models import CustomUser, Follow



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model= CustomUser
        fields = ['id', 'name', 'email', 'phone', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        # Adding the below line made it work for me.
        instance.is_active = True
        if password is not None:
            # Set password does the hash, so you don't need to call make_password 
            instance.set_password(password)
        instance.save()
        return instance
    
class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'phone']


class GenericFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follows', 'follower']
        read_only_fields = ('follower', )


# class FollowerSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()

#     def get_user(self, obj):
#         return UserUpdateSerializer(obj.follower)

#     class Meta:
#         model = Follow
#         fields = ['id', 'follows', 'follower', 'user']


# class FollowSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()

#     def get_user(self, obj):
#         return UserUpdateSerializer(obj.follows)

#     class Meta:
#         model = Follow
#         fields = ['id', 'follows', 'follower', 'user']


