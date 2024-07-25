from rest_framework import serializers
from auths.serializers import UserSerializer
from .models import Diary, Image

class DiraySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Diary
        exclude = ['id']

    def update(self, instance, validated_data):

        instance.content = validated_data.get('content', instance.content)
        instance.url = validated_data.get('url', instance.url)
        return super().update(instance, validated_data) 

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, source="url")

    class Meta:
        model = Image
        fields = "__all__"


