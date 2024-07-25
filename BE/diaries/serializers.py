from rest_framework import serializers
from auths.serializers import UserSerializer
from .models import Diary, Image

class DiraySerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)
    imgfile = serializers.ImageField(required=False)

    class Meta:
        model = Diary
        fields = "__all__"
        exclude = ['id']

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, source="url")

    class Meta:
        model = Image
        fields = "__all__"


