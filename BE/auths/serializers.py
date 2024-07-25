from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'email']
        extra_kwargs = {
            'id': {'read_only': True}  # 'id' 필드를 읽기 전용으로 설정
        }