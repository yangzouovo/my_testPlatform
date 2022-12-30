from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    扩展用户 信息序列化
    """
    user = UserSerializer()
    name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_name(self, obj):
        return obj.user.username
    


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        # token['username'] = user.username
        # token['code'] = 20000
        # print(token)
        # ... 官方示例中上面的部分没有生效
        return token

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            data['username'] = attrs['username']
            re_data = {'data': data, 'code': 20000, 'message': 'success'}
            return re_data

        except Exception as e:
            return {'data': None, 'code': 40004, 'message': 'invalid username or password'}


if __name__ == '__main__':
    pass