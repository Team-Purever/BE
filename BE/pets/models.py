from django.db import models
from auths.models import User

class Pet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets', null=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    url = models.ImageField(upload_to='pet_photos/')

    def __str__(self):
        return self.name


class PetImg(models.Model):
    url = models.ImageField(upload_to='pet_photos')

    def __str__(self):
        return self.url