from rest_framework import serializers
from .models import Pet

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'age', 'photo']

class PetImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['photo']