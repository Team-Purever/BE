from rest_framework import serializers
from .models import Pet, PetImg

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'user', 'name', 'age', 'url']
        read_only_fields = ['user']


class PetImgSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, source="url")
    
    class Meta:
        model = PetImg
        fields = "__all__"


"""
class PetImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['url']
"""