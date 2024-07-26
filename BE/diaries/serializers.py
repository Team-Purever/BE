from rest_framework import serializers
from auths.serializers import UserSerializer
from .models import Diary, Image

class DiraySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Diary
        exclude = ['id']

class DiraySerializer2(serializers.ModelSerializer):

    class Meta:
        model = Diary
        exclude = ['id', 'user']

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, source="url")

    class Meta:
        model = Image
        fields = "__all__"


