from rest_framework import serializers
from .models import AccuknoxUsers,FriendRequest
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccuknoxUsers
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = AccuknoxUsers.objects.create_user(**validated_data)
        return user
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs['email'] = attrs['email'].lower()
        return super().validate(attrs)


class SearchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccuknoxUsers
        fields = ['id', 'email', 'first_name', 'last_name']

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'timestamp', 'is_accepted', 'is_rejected']
        read_only_fields = ['from_user']

    def validate(self, attrs):
        request = self.context['request']
        attrs['from_user'] = request.user
        return super().validate(attrs)

