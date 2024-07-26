from rest_framework import serializers
from .models import Pet, PetImg

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'user', 'name', 'age', 'url']
        read_only_fields = ['user']


class PetImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetImg
        fields = ['id', 'url']


"""
class PetImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['url']
"""